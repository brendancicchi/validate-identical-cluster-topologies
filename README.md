# Helper to confirm identical topologies for clones

This Python script collects the topology of two running clusters and then compares the rings
to determine if the topologies are the same. This will not only look at individual node
token allocations, but also token groupings within the logical racks and datacenters. The
output is either a match or not. The full topology dictionary can be printed with `-v`.

## Usage

```
Usage: validate_identical_topology [OPTIONS]

Options:
  -sh, --source-hosts TEXT        Initial contact points for source cluster
                                  [required]

  -sp, --source-port INTEGER      Source cluster native transport port
  -su, --source-username TEXT     Username to authenticate source cluster
                                  NOTE: This argument is is required with
                                  source_password

  -spw, --source-password TEXT    Password to authenticate source cluster
                                  NOTE: This argument is is required with
                                  source_username

  -spk, --source-client-private-key TEXT
                                  Path to PEM-format private key for 2-way SSL
                                  NOTE: This argument is is required with sour
                                  ce_client_public_cert,source_server_public_c
                                  ert

  -spc, --source-client-public-cert TEXT
                                  Path to PEM-format public certificate for
                                  2-way SSL NOTE: This argument is is required
                                  with source_client_private_key,source_server
                                  _public_cert

  -sc, --source-server-public-cert TEXT
                                  Path to PEM-format public certificate of
                                  source cluster

  -th, --target-hosts TEXT        Initial contact points for the target
                                  cluster  [required]

  -tp, --target-port INTEGER      Target cluster native transport port
  -tu, --target-username TEXT     Username to authenticate target cluster
                                  NOTE: This argument is is required with
                                  target_password

  -tpw, --target-password TEXT    Password to authenticate target cluster
                                  NOTE: This argument is is required with
                                  target_username

  -tpk, --target-client-private-key TEXT
                                  Path to PEM-format private key for 2-way SSL
                                  NOTE: This argument is is required with targ
                                  et_client_public_cert,target_server_public_c
                                  ert

  -tpc, --target-client-public-cert TEXT
                                  Path to PEM-format public certificate for
                                  2-way SSL NOTE: This argument is is required
                                  with target_client_private_key,target_server
                                  _public_cert

  -tc, --target-server-public-cert TEXT
                                  Path to PEM-format public certificate of
                                  target cluster

  -v, --verbose                   Print the cluster topology maps for each
                                  cluster

  --help                          Show this message and exit.
```

### Example Verbose Output
```
These two cluster topologies are different

Source Topology:
{'cluster_topology': {'DC1': {'rack1': {'10.101.33.161': [-9223372036854775808], '10.101.33.91': [-3074457345618258603], '10.101.32.105': [3074457345618258602], '10.101.32.90': [6148914691236517205], '10.101.33.172': [-6148914691236517206], '10.101.32.197': [0]}}}, 'hashes': {'datacenters': [('6a6bf28bee01ff3845761630e272ef4a4331f58a8f1383b5a35b45034bcfe0d5', 'DC1')], 'racks': [('fd8ba7ec2ef0e6361f0d2940fb3b79b004458dea2fbcef41adba9600efafeeb6', 'DC1,rack1')], 'nodes': [('85386477f3af47e4a0b308ee3b3a688df16e8b2228105dd7d4dcd42a9807cb78', '10.101.33.161'), ('68d98239c01742d3cd90936bce2e31e55b06f88b53a11ec132407ed306deef3b', '10.101.33.91'), ('190a5260b6e1348f18d6eb41e3e5c00c011aec13e27c0c560a54f06b7c975e59', '10.101.32.105'), ('9894d012e2ee60ec005b256c1dbea589184abdca50b22ff507850a287f69300c', '10.101.32.90'), ('7c3f0ce5edac30ad6dc8ee18edadc36ad85121c22b283e58242f7f3ca1fc071d', '10.101.33.172'), ('5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9', '10.101.32.197'), ('85386477f3af47e4a0b308ee3b3a688df16e8b2228105dd7d4dcd42a9807cb78', '10.101.32.197'), ('68d98239c01742d3cd90936bce2e31e55b06f88b53a11ec132407ed306deef3b', '10.101.32.197'), ('190a5260b6e1348f18d6eb41e3e5c00c011aec13e27c0c560a54f06b7c975e59', '10.101.32.197'), ('9894d012e2ee60ec005b256c1dbea589184abdca50b22ff507850a287f69300c', '10.101.32.197'), ('7c3f0ce5edac30ad6dc8ee18edadc36ad85121c22b283e58242f7f3ca1fc071d', '10.101.32.197'), ('5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9', '10.101.32.197')], 'cluster': '336a1b1bb46f56a9f6f8b70ab47e9d040d31fe901aebd8511ced4c7d010ae3b7'}}

Target Topology:
{'cluster_topology': {'DC1': {'rack1': {'10.101.33.82': [-9223372036854775808], '10.101.33.146': [-6148914691236517206], '10.101.32.79': [-3074457345618258603]}, 'rack2': {'10.101.32.137': [3074457345618258602], '10.101.32.255': [0], '10.101.32.156': [6148914691236517205]}}}, 'hashes': {'datacenters': [('fab47f48529fd6feee68dd22950a24a452b17cb5dfbd215026a28b8a516f620e', 'DC1')], 'racks': [('605826c45abb7062875788fc886f1db165d37b46089754fb8f2348350792f386', 'DC1,rack1'), ('acea8d55358c4d06c09f3a4959f9bd77231c6484889af3902e1eda4a47ff4af2', 'DC1,rack2')], 'nodes': [('85386477f3af47e4a0b308ee3b3a688df16e8b2228105dd7d4dcd42a9807cb78', '10.101.33.82'), ('7c3f0ce5edac30ad6dc8ee18edadc36ad85121c22b283e58242f7f3ca1fc071d', '10.101.33.146'), ('190a5260b6e1348f18d6eb41e3e5c00c011aec13e27c0c560a54f06b7c975e59', '10.101.32.137'), ('5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9', '10.101.32.255'), ('68d98239c01742d3cd90936bce2e31e55b06f88b53a11ec132407ed306deef3b', '10.101.32.79'), ('9894d012e2ee60ec005b256c1dbea589184abdca50b22ff507850a287f69300c', '10.101.32.156'), ('85386477f3af47e4a0b308ee3b3a688df16e8b2228105dd7d4dcd42a9807cb78', '10.101.32.156'), ('7c3f0ce5edac30ad6dc8ee18edadc36ad85121c22b283e58242f7f3ca1fc071d', '10.101.32.156'), ('68d98239c01742d3cd90936bce2e31e55b06f88b53a11ec132407ed306deef3b', '10.101.32.156'), ('190a5260b6e1348f18d6eb41e3e5c00c011aec13e27c0c560a54f06b7c975e59', '10.101.32.156'), ('5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9', '10.101.32.156'), ('9894d012e2ee60ec005b256c1dbea589184abdca50b22ff507850a287f69300c', '10.101.32.156')], 'cluster': 'f1919881cf35ff80dc17adda8b2b402f597c47ca7c73aa2b65ce5c8fe0ac132b'}}
```