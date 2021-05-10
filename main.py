import cassandra_utils
import click

# Starting code derived from https://stackoverflow.com/a/44349292/10156762
# Have some options that require other optional arguments to be set
class RequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.required_if = kwargs.pop('required_if').split(',')
        assert self.required_if, "'required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
          ' NOTE: This argument is is required with %s' %
          ','.join(self.required_if)
        ).strip()
        super(RequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        for other in self.required_if:
            other_present = other in opts
            if we_are_present:
                if not other_present:
                    print(other_present)
                    raise click.UsageError(
                      "Illegal usage: `%s` must be used with `%s`" % (self.name, self.required_if)
                    )
                else:
                    self.prompt = None

        return super(RequiredIf, self).handle_parse_result(
            ctx, opts, args)

@click.command()
# Source cluster connection options
@click.option('--source-hosts', '-sh', default='127.0.0.1', required=True, help='Initial contact points for source cluster')
@click.option('--source-port', '-sp', default=9042, help='Source cluster native transport port')
@click.option('--source-username', '-su', help='Username to authenticate source cluster', cls=RequiredIf, required_if='source_password')
@click.option('--source-password', '-spw', help='Password to authenticate source cluster', cls=RequiredIf, required_if='source_username')
@click.option('--source-client-private-key', '-spk', help='Path to PEM-format private key for 2-way SSL', cls=RequiredIf, required_if='source_client_public_cert,source_server_public_cert')
@click.option('--source-client-public-cert', '-spc', help='Path to PEM-format public certificate for 2-way SSL', cls=RequiredIf, required_if='source_client_private_key,source_server_public_cert')
@click.option('--source-server-public-cert', '-sc', help='Path to PEM-format public certificate of source cluster')
# Target cluster connection options
@click.option('--target-hosts', '-th', default='127.0.0.1', required=True, help='Initial contact points for the target cluster')
@click.option('--target-port', '-tp', default=9042, help='Target cluster native transport port')
@click.option('--target-username', '-tu', help='Username to authenticate target cluster', cls=RequiredIf, required_if='target_password')
@click.option('--target-password', '-tpw', help='Password to authenticate target cluster', cls=RequiredIf, required_if='target_username')
@click.option('--target-client-private-key', '-tpk', help='Path to PEM-format private key for 2-way SSL', cls=RequiredIf, required_if='target_client_public_cert,target_server_public_cert')
@click.option('--target-client-public-cert', '-tpc', help='Path to PEM-format public certificate for 2-way SSL', cls=RequiredIf, required_if='target_client_private_key,target_server_public_cert')
@click.option('--target-server-public-cert', '-tc', help='Path to PEM-format public certificate of target cluster')
# Output options
@click.option('--verbose', '-v', is_flag=True, help='Print the cluster topology maps for each cluster')
def validate_identical_topology(
  source_hosts, source_port, source_username, source_password,
  source_client_private_key, source_client_public_cert, source_server_public_cert,
  target_hosts, target_port, target_username, target_password,
  target_client_private_key, target_client_public_cert, target_server_public_cert,
  verbose
):
    source_session = cassandra_utils.CqlSessionProvider(
      ip_addresses=source_hosts.split(','),
      port=source_port,
      username=source_username,
      password=source_password,
      client_private_key=source_client_private_key,
      client_public_cert=source_client_public_cert,
      server_cert=source_server_public_cert
    ).new_session()
    target_session = cassandra_utils.CqlSessionProvider(
      ip_addresses=target_hosts.split(','),
      port=target_port,
      username=target_username,
      password=target_password,
      client_private_key=target_client_private_key,
      client_public_cert=target_client_public_cert,
      server_cert=target_server_public_cert
    ).new_session()
    source_topology = source_session.topology_hashes()
    target_topology = target_session.topology_hashes()

    if source_topology['hashes']['cluster'] == target_topology['hashes']['cluster']:
        click.echo('These two cluster topologies are the same')
    else:
        msg = 'These two cluster topologies are different'
        if verbose:
            msg = f'{msg}\n\nSource Topology:\n{source_topology}\n\nTarget Topology:\n{target_topology}'
        else:
            msg = f'{msg} (Run with -v for the full topologies)'
        click.echo(msg)