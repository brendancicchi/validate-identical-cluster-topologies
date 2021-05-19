# Helper to confirm identical topologies for clones

This Python script collects the topology of two running clusters and then compares the rings
to determine if the topologies are the same. This will not only look at individual node
token allocations, but also token groupings within the logical racks and datacenters. The
output is either a match or not. The full topology dictionary can be printed with `-v`.

## Usage

```
Usage: cass_compare_topology [OPTIONS]

Options:
  -sf, --source-ring-file TEXT    Nodetool ring output for source cluster
                                  NOTE: This argument cannot be used with
                                  source_hosts

  -tf, --target-ring-file TEXT    Nodetool ring output for target cluster
                                  NOTE: This argument cannot be used with
                                  target_hosts

  -sh, --source-hosts TEXT        Initial contact points for source cluster
                                  NOTE: This argument cannot be used with
                                  source_ring_file

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
                                  cluster NOTE: This argument cannot be used
                                  with target_ring_file

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

Source DataCenter        Target DataCenter
-------------------  --  -------------------
DC1                  ==  NEW_DC3


Source Topology:
{
  "cluster_topology": {
    "DC2": {
      "rack1": {
        "10.101.33.19": [
          -9102224605420384153,
          -6171532958060517710,
          -4040629092074056914,
          1004623290016916338,
          5434985573228175252,
          7316123860976003622,
          8904503219120065615,
          9065981260293540840
        ],
        "10.101.34.3": [
          -9211342113635538874,
          -7336751969826853313,
          -6632953046016691003,
          -5411499073742532426,
          999452792521231800,
          5834579152848854593,
          6298604437473773991,
          6589568307664159758
        ],
        "10.101.32.100": [
          -9062922692108230128,
          -4426456498154921668,
          -2349627758160733810,
          -2334302717619944276,
          -891537863988787649,
          1733802573127308333,
          7306234125789390790,
          8627726301065922124
        ],
        "10.101.32.69": [
          -7072613509803120995,
          -3000937270040727904,
          -1521529191650429850,
          -714833504955882534,
          246186377616547887,
          1555501413463695730,
          4416905650740770068,
          4995632327547835506
        ]
      }
    },
    "DC1": {
      "rack1": {
        "10.101.32.137": [
          -6367604783287765724,
          -5087498425401461675,
          -3999022230037872694,
          -1951484283765042481,
          -1498250974610086005,
          1246209236126851845,
          1276389722082113031,
          5565121877685550408
        ],
        "10.101.32.14": [
          -7803521838623991824,
          -7457326552110611380,
          -7120917271215391286,
          -5718710306363938972,
          -3582201038546242025,
          2512729222552707036,
          4031802080782249736,
          7653478120880834644
        ],
        "10.101.32.20": [
          -8763760090782264517,
          -8568101242718084256,
          -4181770166012958462,
          -1748238146008291656,
          -1432819135469266282,
          372608252216691063,
          3502154028729969789,
          8385517081710569943
        ],
        "10.101.32.156": [
          -7769489913007769763,
          -4600282627799773228,
          -439174848848186967,
          1311227579067191238,
          4538969390914589289,
          7898405297151757945,
          7939294426485406075,
          8147048690454597500
        ]
      }
    }
  },
  "hashes": {
    "datacenters": [
      [
        "7c4012438e40115e0b18efc1333af16f7f3903b4a7aef6650861158ffcc84d4d",
        "DC2"
      ],
      [
        "7a445a22ffe2dbf55b3898371966f4981e8b833316aa3d2a076a34bc3742d2f8",
        "DC1"
      ]
    ],
    "racks": [
      [
        "d8324568e948c3cee68ae0158b69d4bb89f35c94a89a2ba437540266b277e6e4",
        "DC2,rack1"
      ],
      [
        "3961643c683d1fee7327218f397d3a47d93e234a3eacf447d2b3039163f53648",
        "DC1,rack1"
      ]
    ],
    "nodes": [
      [
        "4e347e7373409a163da0ceac2ba4288e76a2ec1196e0a0fb641cb0015b30afb8",
        "10.101.33.19"
      ],
      [
        "6be34b4828360f041b39cb573f50db73737736c59f0f26c77db10dd42004f7eb",
        "10.101.34.3"
      ],
      [
        "085b07928c9ff8806db3b9b040f4553a22c97f1cd80da8de65aa72741af65a6b",
        "10.101.32.100"
      ],
      [
        "8cb97e43795ff24c49853ff2cd7e4c4c3e288d541b7d04d710bc5a8d89609a0a",
        "10.101.32.69"
      ],
      [
        "1d4deb23f25032c045fedb3de036425960831828d3317427a3995302753d0c3a",
        "10.101.32.137"
      ],
      [
        "6152b6d52a73987bbdfb0c204c17e761d110dfeaf450eb7ef5718b41df0bb3eb",
        "10.101.32.14"
      ],
      [
        "ea673523e5b1408b38dd0fff6dc7558c05fdc828dbf343a4c05584788335f764",
        "10.101.32.20"
      ],
      [
        "9595ff21f865e0895a36a8f7e503af6b5442a7449ded1c4137e06a7a84315d04",
        "10.101.32.156"
      ]
    ],
    "cluster": "dd476fbf567550c8c772083615aff8ad16e150909feef7ccc29ced50d0252df9"
  }
}

Target Topology:
{
  "cluster_topology": {
    "NEW_DC3": {
      "rack1": {
        "10.101.34.66": [
          -8763760090782264517,
          -8568101242718084256,
          -4181770166012958462,
          -1748238146008291656,
          -1432819135469266282,
          372608252216691063,
          3502154028729969789,
          8385517081710569943
        ],
        "10.101.36.86": [
          -6367604783287765724,
          -5087498425401461675,
          -3999022230037872694,
          -1951484283765042481,
          -1498250974610086005,
          1246209236126851845,
          1276389722082113031,
          5565121877685550408
        ],
        "10.101.36.44": [
          -7769489913007769763,
          -4600282627799773228,
          -439174848848186967,
          1311227579067191238,
          4538969390914589289,
          7898405297151757945,
          7939294426485406075,
          8147048690454597500
        ],
        "10.101.32.197": [
          -7803521838623991824,
          -7457326552110611380,
          -7120917271215391286,
          -5718710306363938972,
          -3582201038546242025,
          2512729222552707036,
          4031802080782249736,
          7653478120880834644
        ]
      }
    },
    "DC2": {
      "rack1": {
        "10.101.32.65": [
          -9118865439420359123,
          -5997542370710579714,
          -4510574172257270150,
          -3465722742882282924,
          -1910470623548966757,
          -1855708756852217655,
          2412229710266512222,
          3026331785618743045
        ],
        "10.101.33.2": [
          -7552679084732237857,
          -3906317900187761477,
          -1481915352101991245,
          -1012864117021087007,
          129090863501504346,
          1382859881264266679,
          3996706802532830689,
          7145393404014291686
        ],
        "10.101.33.124": [
          -8869287634242112961,
          -3343430613197272348,
          -1827959686488594431,
          -376530210330586591,
          -69752312092417426,
          5719042041371934504,
          8332774865642750628,
          9178690486702775175
        ],
        "10.101.33.77": [
          -8539939367075776855,
          -7288644250999413634,
          -6136091066073797615,
          -5348341146618336510,
          -136853100370561362,
          4671427850956075721,
          5286884817039942141,
          6028597302796798755
        ]
      }
    },
    "NEW_DC1": {
      "rack1": {
        "10.101.34.200": [
          -9102224605420384153,
          -6171532958060517710,
          -4040629092074056914,
          1004623290016916338,
          5434985573228175252,
          7316123860976003622,
          8904503219120065615,
          9065981260293540840
        ],
        "10.101.32.105": [
          -9062922692108230128,
          -4426456498154921668,
          -2349627758160733810,
          -2334302717619944276,
          -891537863988787649,
          1733802573127308333,
          7306234125789390790,
          8627726301065922124
        ]
      },
      "rack2": {
        "10.101.32.79": [
          -7072613509803120995,
          -3000937270040727904,
          -1521529191650429850,
          -714833504955882534,
          246186377616547887,
          1555501413463695730,
          4416905650740770068,
          4995632327547835506
        ],
        "10.101.36.2": [
          -9211342113635538874,
          -7336751969826853313,
          -6632953046016691003,
          -5411499073742532426,
          999452792521231800,
          5834579152848854593,
          6298604437473773991,
          6589568307664159758
        ]
      }
    }
  },
  "hashes": {
    "datacenters": [
      [
        "7a445a22ffe2dbf55b3898371966f4981e8b833316aa3d2a076a34bc3742d2f8",
        "NEW_DC3"
      ],
      [
        "2f454468f23d00ff8e7851e5c2dfbaf2a593a5159f2cce7dca9bede7dc3acb95",
        "DC2"
      ],
      [
        "6335866b6d33465ff51b27cf0d0d46a91ba5b75ddf7be061515d231f2e52277f",
        "NEW_DC1"
      ]
    ],
    "racks": [
      [
        "3961643c683d1fee7327218f397d3a47d93e234a3eacf447d2b3039163f53648",
        "NEW_DC3,rack1"
      ],
      [
        "eb96fcecf593bd3f8b555c56bfa72942908e8e0245b8b68d7ccc48c2564189c4",
        "DC2,rack1"
      ],
      [
        "9287b678abdb54384bf302839ca1e86f86ab258a62be365e8b1b920211384f82",
        "NEW_DC1,rack1"
      ],
      [
        "018510cf470e45b6c9c377d7c95327963f94061a48e4e0944403de3b7d2fd8c7",
        "NEW_DC1,rack2"
      ]
    ],
    "nodes": [
      [
        "ea673523e5b1408b38dd0fff6dc7558c05fdc828dbf343a4c05584788335f764",
        "10.101.34.66"
      ],
      [
        "1d4deb23f25032c045fedb3de036425960831828d3317427a3995302753d0c3a",
        "10.101.36.86"
      ],
      [
        "9595ff21f865e0895a36a8f7e503af6b5442a7449ded1c4137e06a7a84315d04",
        "10.101.36.44"
      ],
      [
        "6152b6d52a73987bbdfb0c204c17e761d110dfeaf450eb7ef5718b41df0bb3eb",
        "10.101.32.197"
      ],
      [
        "7b21371a7df060708bace2a2ee7973574735c782d3f2bdd03b32178fb81aff87",
        "10.101.32.65"
      ],
      [
        "6229e369ae421d122f5a758d95ec00391db4aadef6b3a6116ac46402bec45ac7",
        "10.101.33.2"
      ],
      [
        "50e2d334e32f0ad0080637a0a92320801e6421e88c8a2e0b6571bfae1735019c",
        "10.101.33.124"
      ],
      [
        "404882c842c7fb0650116edcfc4c40cbbbc98abbc510fa2b8db832de3a4cec84",
        "10.101.33.77"
      ],
      [
        "4e347e7373409a163da0ceac2ba4288e76a2ec1196e0a0fb641cb0015b30afb8",
        "10.101.34.200"
      ],
      [
        "085b07928c9ff8806db3b9b040f4553a22c97f1cd80da8de65aa72741af65a6b",
        "10.101.32.105"
      ],
      [
        "8cb97e43795ff24c49853ff2cd7e4c4c3e288d541b7d04d710bc5a8d89609a0a",
        "10.101.32.79"
      ],
      [
        "6be34b4828360f041b39cb573f50db73737736c59f0f26c77db10dd42004f7eb",
        "10.101.36.2"
      ]
    ],
    "cluster": "c8cd62c6d898258c5ec77b85f042cba199c7ddc463e65b2a4548ce74db0add3a"
  }
}
```