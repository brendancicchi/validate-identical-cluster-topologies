from setuptools import setup

setup(
    name='Validate Identical Cluster Topology',
    version='0.2',
    py_modules=['clone-topo-check'],
    install_requires=[
        'click==7.1.2',
        'cassandra-driver==3.25.0'
    ],
    entry_points='''
        [console_scripts]
        cass_compare_topology=main:validate_identical_topology
    ''',
)