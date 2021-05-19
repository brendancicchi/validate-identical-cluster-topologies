import ipaddress
import itertools

from cassandra.cluster import Cluster, ExecutionProfile
from cassandra.policies import WhiteListRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from hashlib import sha256
from ssl import SSLContext, PROTOCOL_TLS

def is_ip (str):
    try:
        ipaddress.ip_address(str)
    except ValueError:
        return False
    return True

# Take an array of numbers and concatentate all them prior to hashing
def concat_hash(tokens):
    return sha256(''.join(str(token) for token in tokens).encode('utf-8')).hexdigest()

# Create the SHA256 hashes for cluster level, dc level, rack level, and node level
def hash_topology_dict(topology_dict):
    topology_dict.setdefault('hashes', {'datacenters': [], 'racks': [], 'nodes': []})
    dc_hashes = []
    for datacenter, rack_dict in topology_dict['cluster_topology'].items():
        dc_rack_hashes = []
        for rack, node_dict in rack_dict.items():
            rack_node_hashes = []
            for address, tokens in node_dict.items():
                node_token_hash = concat_hash(tokens) # The tokens are already sorted
                rack_node_hashes.append(node_token_hash)
                topology_dict['hashes']['nodes'].append((node_token_hash, address))
            rack_token_hash = concat_hash(sorted(rack_node_hashes))
            dc_rack_hashes.append(rack_token_hash)
            topology_dict['hashes']['racks'].append((rack_token_hash, f'{datacenter},{rack}'))
        dc_rack_token_hash = concat_hash(sorted(dc_rack_hashes))
        dc_hashes.append(dc_rack_token_hash)
        topology_dict['hashes']['datacenters'].append((dc_rack_token_hash, datacenter))
    topology_dict['hashes']['cluster'] = concat_hash(sorted(dc_hashes))
    return topology_dict

class CqlSessionProvider(object):

    def __init__(self, ip_addresses, port, username, password, client_private_key, client_public_cert, server_cert):
        self._ip_addresses = ip_addresses
        self._port = port
        self._auth_provider = None
        self._ssl_context = None

        if username != None and password != None:
            self.auth_provider = PlainTextAuthProvider(username, password)
        
        if server_cert != None:
            ssl_context = SSLContext(PROTOCOL_TLS)
            ssl_context.load_verify_locations(server_cert)
            if client_private_key != None and client_public_cert != None:
                ssl_context.load_cert_chain(
                  certfile=client_public_cert,
                  keyfile=client_private_key
                )

            self._ssl_context = ssl_context

        load_balancing_policy = WhiteListRoundRobinPolicy(ip_addresses)
        self._execution_profiles = {
            'local': ExecutionProfile(load_balancing_policy=load_balancing_policy)
        }

    def new_session(self):
        cluster = Cluster(
          contact_points=self._ip_addresses,
          port=self._port,
          auth_provider=self._auth_provider,
          execution_profiles=self._execution_profiles,
          ssl_context=self._ssl_context
        )

        session = cluster.connect()
        return CqlSession(session)


class CqlSession(object):
    def __init__(self, session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        self.session.shutdown()
        self.cluster.shutdown()

    @property
    def cluster(self):
        return self._session.cluster

    @property
    def session(self):
        return self._session

    def topology_hashes(self):
        token_map = self.cluster.metadata.token_map
        host_token_pairs = [(host, token.value) for token, host in token_map.token_to_host_owner.items()]
        host_tokens_groups = itertools.groupby(host_token_pairs, key=lambda x: x[0])
        host_tokens_pairs = [(host, sorted(list(map(lambda x: x[1], tokens)))) for host, tokens in host_tokens_groups]
        topology_dict = {'cluster_topology': {}, 'hashes': {'datacenters': [], 'racks': [], 'nodes': []}}
        # Create the human readable and referenceable topology dict
        for host, tokens in host_tokens_pairs:
            topology_dict['cluster_topology'].setdefault(host.datacenter, {}).setdefault(host.rack, {}).setdefault(host.address, tokens)        
        return hash_topology_dict(topology_dict)


class NodetoolRingObject:
    def __init__(self, nodetool_ring_file):
        self.nodetool_ring_file = nodetool_ring_file
    
    def parse_topology(self):
        with open(self.nodetool_ring_file, 'r') as fh:
            dc = ""
            topology_dict = {'cluster_topology': {}, 'hashes': {'datacenters': [], 'racks': [], 'nodes': []}}
            for line in fh:
                line_tokens = line.split()      
                if line.startswith("Datacenter:", 0, 11):
                    dc = line_tokens[1]
                    topology_dict['cluster_topology'].setdefault(dc, {})
                if len(line_tokens) > 0 and is_ip(line_tokens[0]):
                    rack = line_tokens[1]
                    address = line_tokens[0]
                    token = line_tokens[7]
                    # Nodetool ring output is actually already sorted, so no need to sort tokens after the fact
                    topology_dict['cluster_topology'][dc].setdefault(rack, {}).setdefault(address, []).append(token)
        return hash_topology_dict(topology_dict)