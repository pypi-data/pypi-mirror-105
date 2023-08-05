from collections import OrderedDict
import random
import shlex
import sys
from typing import Any, Dict, Optional

import click
from coolname import generate_slug

from grid.cli.grid_credentials import print_creds_table
from grid.cli.utilities import read_config
from grid.cli.utilities import validate_config
from grid.cli.utilities import validate_disk_size_callback
from grid.client import Grid
import grid.globals as env
from grid.tracking import Segment
from grid.tracking import TrackingEvents
from grid.types import WorkflowType
from grid.utilities import check_description_isnt_too_long


def get_credentials(client: Grid, grid_credential: Optional[str] = None) -> Dict[str, str]:
    """
    Get credentials based on either grid credential or default credential

    Returns
    -------
    Dict[str, str]
        Credential auth
    """
    _default_credential = None
    creds = client.get_credentials()['getUserCredentials']
    if grid_credential:
        if creds:
            for credential in creds:
                if credential['credentialId'] == grid_credential:
                    return credential

        raise click.ClickException(f'Credential {grid_credential} does not exist. ' +
                                   'Use grid credentials to see available credential IDs.')

    _url = client.url.replace('/graphql', '')
    no_credentials_message = f"""
    No cloud credentials available! Visit {_url}/#/settings to
    add new cloud credentials.
    """
    if not creds:
        raise click.ClickException(no_credentials_message)

    if len(creds) == 1:
        cred = creds[0]
        return cred

    for credential in creds:
        if credential['defaultCredential']:
            click.echo(f"Using default cloud credentials {credential['credentialId']} "
                       f"to run on {credential['provider'].upper()}.")
            return credential

    # If no default credentials are available, raise an exception.
    m = """
    Detected multiple credentials. Which would you like to use?
    """
    print_creds_table(creds)
    raise click.ClickException(m)


def _check_run_name_is_valid(_ctx, _param, value):
    """Click callback that checks if a Run contains reserved names."""
    if value is not None:
        fail = False

        #  Check if the input is alphanumeric.
        _run_name = value.replace('-', '')
        if not _run_name.isalnum():
            fail = True

        #  Check if the allowed `-` character is not used
        #  at the end of the string.
        elif value.endswith('-') or value.startswith('-'):
            fail = True

        #  Check that the run name does not contain any
        #  uppercase characters.
        elif any(x.isupper() for x in value):
            fail = True

        if fail:
            raise click.BadParameter(f"""

            Invalid Run name: {value} the Run name must be lower case
            alphanumeric characters or '-', start with an alphabetic
            character, and end with an alphanumeric character (e.g. 'my-name',
            or 'abc-123').

                """)

    return value


def _check_ignore_warnings_flag(ctx, _param, value):
    """
    Click callback that assigns the value of the ignore warnigns callback
    to a global variable.
    """
    if value is not None:
        env.IGNORE_WARNINGS = value

    return value


def _generate_default_grid_config(client: Grid,
                                  grid_credential: str,
                                  instance_type: str,
                                  use_spot: Optional[bool] = None,
                                  distributed: Optional[bool] = False,
                                  grid_strategy: Optional[str] = None,
                                  grid_trials: Optional[int] = None,
                                  gpus: Optional[int] = None,
                                  max_nodes: Optional[int] = None,
                                  disk_size: Optional[int] = None,
                                  memory: str = None,
                                  cpus: Optional[int] = None,
                                  datastore_name: Optional[str] = None,
                                  datastore_version: Optional[int] = None,
                                  datastore_mount_dir: Optional[str] = None,
                                  framework: Optional[str] = None):
    """
    Generates a new default config file for user if user hasn't
    submitted one.
    """
    _default_credential = get_credentials(client=client, grid_credential=grid_credential)

    #  Relevant defaults for user.
    #  TODO: Pull from user profile when we have
    #  that information collected.
    defaults = {'region': 'us-east-1'}

    _grid_config = {
        'compute': {
            'provider': {
                'vendor': _default_credential['provider'],
                'credentials': _default_credential['credentialId'],
                'region': defaults['region']
            },
            'train': {
                'framework': framework,
                'distributed': distributed,
                'datastore_name': datastore_name,
                'datastore_version': datastore_version,
                'datastore_mount_dir': datastore_mount_dir,
                'instance': instance_type,
                'use_spot': use_spot or False,
                'nodes': 0,  # How many nodes are created at first.
                'max_nodes': max_nodes,
                'gpus': gpus,
                'scale_down_seconds': 30 * 60,  # 30 minutes before scaling down.
                'disk_size': disk_size,
                'memory': memory,
                'cpus': cpus
            }
        }
    }

    #  We add a `hyper_params` key to the default config
    #  if the user has passed the `grid_strategy` argument.
    if grid_strategy:
        if not _grid_config.get('hyper_params'):
            _grid_config['hyper_params'] = {}

        _grid_config['hyper_params'] = {'settings': {'strategy': grid_strategy}, 'params': {}}

        #  We also add the key trials if that has been
        #  passed. trials is only valid when doing a `random_search`
        #  at the moment. Our parser will not be bothered by its
        #  presence if we pass it by default.
        if grid_trials:
            _grid_config['hyper_params']['settings']['trials'] = grid_trials

    if env.DEBUG:
        click.echo('Grid Config used:')
        click.echo(_grid_config)

    return _grid_config


def _check_is_valid_extension(ctx, _param, value):
    """Click callback that checks if a file is a Python script."""
    if value is not None:
        if not any(value.endswith(e) for e in ['.py', '.sh']):
            message = 'You must provide a valid script (python or shell). ' \
                      'No script detected.'
            raise click.BadParameter(message)

        ctx.params['entrypoint'] = value
        return value


def _aws_node_to_nickname():
    aws_node_to_nicknames = OrderedDict({
        'p3.16xlarge': '8_v100_16gb',
        'p3dn.24xlarge': '8_v100_32gb',
        'g4dn.metal': '8_t4_16gb',
        'p2.8xlarge': '8_k80_12gb',
        'p3.8xlarge': '4_v100_16gb',
        'g4dn.12xlarge': '4_t4_16gb',
        'g3.16xlarge': '4_m60_8gb',
        'g3.8xlarge': '2_m60_8gb',
        'p3.2xlarge': '1_v100_16gb',
        'g4dn.8xlarge': '1_t4_16gb',
        'g4dn.4xlarge': '1_t4_16gb',
        'g4dn.2xlarge': '1_t4_16gb',
        'g4dn.xlarge': '1_t4_16gb',
        'g4dn.16xlarge': '1_t4_16gb',
        'p2.xlarge': '1_k80_12gb',
        'g3s.xlarge': '1_m60_8gb',
        'g3.4xlarge': '1_m60_8gb',
        't2.large': '2_cpu_8gb',
        't2.medium': '2_cpu_4gb'
    })
    return aws_node_to_nicknames


def _nickname_to_aws_nodes():
    aws_node_to_nickname = _aws_node_to_nickname()
    aws_nickname_to_node = {v: k for k, v in aws_node_to_nickname.items()}
    return aws_nickname_to_node


def _resolve_instance_type_nickname(ctx, _param, value):
    """
    Enables instance type shortcuts like:
    2_cpu_4gb for t2.large
    """
    nickname = value.lower()

    aws_nickname_to_node = _nickname_to_aws_nodes()

    # validate potential options for the node name
    possible_values = list(aws_nickname_to_node.keys()) + list(aws_nickname_to_node.values())
    if nickname not in possible_values:
        possible_options = '\n'.join(list(aws_nickname_to_node.keys()))
        click.BadParameter(f'{nickname} is not an available instance_type\n try one of these:\n{possible_options}')

    instance_type = nickname

    # if the value has _ then it's a nickname
    if '_' in nickname:
        instance_type = aws_nickname_to_node[nickname]
    return instance_type


def _get_instance_types(ctx, args, incomplete):
    # TODO: these should be retrieved from backend
    return list(_aws_node_to_nickname().keys())


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--grid_config',
              '--g_config',
              'config',
              type=click.File('r'),
              required=False,
              callback=read_config,
              help='Path to Grid config YML')
@click.option('--grid_name',
              '--g_name',
              'name',
              type=str,
              required=False,
              help='Name for this run',
              callback=_check_run_name_is_valid)
@click.option('--grid_description',
              '--g_description',
              'description',
              type=str,
              required=False,
              help='Run description; useful for note-keeping',
              callback=check_description_isnt_too_long)
@click.option('--grid_credential', '--g_credential', 'credential', type=str, required=False, help='Cloud to run on')
@click.option('--grid_strategy',
              '--g_strategy',
              'strategy',
              type=click.Choice(['grid_search', 'random_search'], case_sensitive=False),
              required=False,
              help='Hyperparameter search strategy')
@click.option('--grid_trials',
              '--g_trials',
              'trials',
              type=int,
              required=False,
              help='Number of trials to run hyper parameter search')
@click.option('--grid_instance_type',
              '--g_instance_type',
              'instance_type',
              type=str,
              default='t2.medium',
              callback=_resolve_instance_type_nickname,
              help='Instance type to start training session in',
              autocompletion=_get_instance_types)
@click.option('--grid_gpus',
              '--g_gpus',
              'gpus',
              type=int,
              required=False,
              default=0,
              help='Number of GPUs to allocate per experiment')
@click.option(
    '--grid_cpus',
    '--g_cpus',
    'cpus',
    type=int,
    required=False,
    default=0,  # Default will be set to 1 after alerting user
    help='Number of CPUs to allocate per experiment')
@click.option('--grid_disk_size',
              '--g_disk_size',
              'disk_size',
              type=int,
              required=False,
              default=200,
              callback=validate_disk_size_callback,
              help='The disk size in GB to allocate to each node in the cluster')
@click.option('--grid_max_nodes',
              '--g_max_nodes',
              'max_nodes',
              type=int,
              required=False,
              default=10,
              help='The maximum nodes to scale cluster to')
@click.option('--grid_memory',
              '--g_memory',
              'memory',
              type=str,
              required=False,
              help='How much memory an experiment needs')
@click.option('--grid_datastore_name',
              '--g_datastore_name',
              'datastore_name',
              type=str,
              required=False,
              help='Datastore name to be mounted in training')
@click.option('--grid_datastore_version',
              '--g_datastore_version',
              'datastore_version',
              type=str,
              required=False,
              help='Datastore version to be mounted in training')
@click.option('--grid_datastore_mount_dir',
              '--g_datastore_mount_dir',
              'datastore_mount_dir',
              type=str,
              required=False,
              help='Directory to mount Datastore in training job')
@click.option('--grid_framework',
              '--g_framework',
              'framework',
              type=str,
              required=False,
              default='lightning',
              help='Framework to use in training')
@click.option('--grid_use_spot',
              '--g_use_spot',
              'use_spot',
              is_flag=True,
              required=False,
              help='Use spot instance. The spot instances, or preemptive instance can be shut down at will')
@click.option(
    '--grid_distributed',
    '--g_distributed',
    'distributed',
    is_flag=True,
    required=False,
    default=False,
    help='Run distributed pytorch training. Only available when trying to run with more than 1 gpu and pytorch.')
@click.option('--ignore_warnings',
              is_flag=True,
              required=False,
              help='If we should ignore warning when executing commands',
              callback=_check_ignore_warnings_flag)
@click.argument('script', type=click.Path(exists=True), callback=_check_is_valid_extension)
@click.argument('script_args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def train(ctx, script: str, entrypoint: str, config: Optional[Dict], name: Optional[str], credential: Optional[str],
          strategy: Optional[str], trials: Optional[int], instance_type: str, gpus: Optional[int],
          disk_size: Optional[int], max_nodes: Optional[int], description: Optional[str], ignore_warnings: bool,
          script_args: Optional[Any], memory: Optional[str], cpus: Optional[int], datastore_name: Optional[str],
          datastore_version: Optional[str], datastore_mount_dir: Optional[str], framework: Optional[str],
          use_spot: Optional[bool], distributed: Optional[bool]) -> None:
    """Trains scripts in remote infrastructure"""
    # Captures all other user arguments that are not
    # parsed automatically.
    script_arguments = list(script_args)

    # Captures invocation command exactly as it was
    # typed in the terminal. pipe.quote maintains original
    # quotation used in the CLI. We'll replace absolute
    # grid executable path with the `grid` alias.
    sys.argv[0] = "grid"
    invocation_command = " ".join(map(shlex.quote, sys.argv))

    if env.DEBUG:
        click.echo(f"Script Arguments {script_arguments}")
        click.echo(f"Entrypoint Script: {entrypoint}")
        click.echo(f"Hyperparams Search Strategy: {strategy}")
        click.echo(f"GPUs Requested: {gpus}")

    client = Grid()
    client.check_is_blocked()

    tracker = Segment()
    tracker.send_event(event=TrackingEvents.RUN_CREATED, properties={'user_input': invocation_command})

    # make a fun random name when user does not pass in a name
    if name is None:
        name = f'{generate_slug(2)}-{random.randint(0, 1000)}'
        click.echo(f'No --grid_name passed, naming your run {name}')

    #  If the user has not passed a grid config file,
    #  then generate one with a set of default options.
    #  We'll add a default instance and the user's
    #  default credentials.
    if not config:
        _grid_config = _generate_default_grid_config(
            client=client,
            grid_credential=credential,
            grid_strategy=strategy,
            grid_trials=trials,
            instance_type=instance_type,
            gpus=gpus,
            max_nodes=max_nodes,
            disk_size=disk_size,
            memory=memory,
            cpus=cpus,
            datastore_name=datastore_name,
            datastore_version=datastore_version,
            datastore_mount_dir=datastore_mount_dir,
            framework=framework,
            distributed=distributed,
            use_spot=use_spot,
        )

    else:
        _grid_config = config

    validate_config(cfg=_grid_config)
    use_spot = _grid_config['compute']['train'].get('use_spot', False)

    client.validate_datastore_version(grid_config=_grid_config)
    datastore_version = _grid_config["compute"]["train"].get("datastore_version")

    # Warn user if they have not specified a cpu or gpu number so cpus will be set to 1
    cpus = _grid_config['compute']['train'].get('cpus')
    gpus = _grid_config['compute']['train'].get('gpus')
    if not cpus and not gpus:
        notice_str = click.style('WARNING', fg='yellow')
        cpu_warning = f"{notice_str} Neither a CPU or GPU number was specified. 1 CPU will be " + \
                      "used as a default. To use N GPUs pass in '--grid_gpus N' flag."

        _grid_config['compute']['train']['cpus'] = 1
        # We will be showing this warning to users, but not
        # issuing a prompt.
        if not env.IGNORE_WARNINGS:
            # click.confirm(cpu_warning, abort=True)
            click.echo(cpu_warning)

    #  Send to client.
    client.train(config=_grid_config,
                 kind=WorkflowType.SCRIPT,
                 run_name=name,
                 run_description=description,
                 entrypoint=entrypoint,
                 script_args=script_arguments,
                 invocation_command=invocation_command)
