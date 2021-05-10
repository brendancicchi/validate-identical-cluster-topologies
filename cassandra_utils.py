import itertools

from cassandra.cluster import Cluster, ExecutionProfile
from cassandra.policies import WhiteListRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from collections import defaultdict
from hashlib import sha256
from ssl import SSLContext, PROTOCOL_TLS

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

        def concat_hash(tokens):
            return sha256(''.join(str(token) for token in tokens).encode('utf-8')).hexdigest()

        host_token_pairs = [(host, token.value) for token, host in token_map.token_to_host_owner.items()]
        host_tokens_groups = itertools.groupby(host_token_pairs, key=lambda x: x[0])
        host_tokens_pairs = [(host, sorted(list(map(lambda x: x[1], tokens)))) for host, tokens in host_tokens_groups]
        topology_dict = {'cluster_topology': {}, 'hashes': {'datacenters': [], 'racks': [], 'nodes': []}}
        # Create the human readable and referenceable topology dict
        for host, tokens in host_tokens_pairs:
            topology_dict['cluster_topology'].setdefault(host.datacenter, {}).setdefault(host.rack, {}).setdefault(host.address, tokens)
            topology_dict['hashes']['nodes'].append((concat_hash(tokens), host.address))
        
        # Create the SHA256 hashes for cluster level, dc level, rack level, and node level
        dc_hashes = []
        for datacenter, rack_dict in topology_dict['cluster_topology'].items():
            dc_rack_hashes = []
            for rack, node_dict in rack_dict.items():
                rack_node_hashes = []
                for node, tokens in node_dict.items():
                    node_token_hash = concat_hash(tokens) # The tokens are already sorted
                    rack_node_hashes.append(node_token_hash)
                    topology_dict['hashes']['nodes'].append((node_token_hash, host.address))
                rack_token_hash = concat_hash(sorted(rack_node_hashes))
                dc_rack_hashes.append(rack_token_hash)
                topology_dict['hashes']['racks'].append((rack_token_hash, f'{datacenter},{rack}'))
            dc_rack_token_hash = concat_hash(sorted(dc_rack_hashes))
            dc_hashes.append(dc_rack_token_hash)
            topology_dict['hashes']['datacenters'].append((dc_rack_token_hash, datacenter))
        topology_dict['hashes']['cluster'] = concat_hash(sorted(dc_hashes))
        return topology_dict



