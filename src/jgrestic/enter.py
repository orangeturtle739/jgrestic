import os
import typing as t

import click

from jgrestic import config
from jgrestic.commands import restic


@click.command()
@click.argument("config_json", type=click.File("r"))
@click.argument("cmd", nargs=-1, required=True)
def enter(config_json: t.TextIO, cmd: t.Tuple[str]) -> None:
    """
    Runs a given CMD in the restic enviroment located defined by CONFIG_JSON.

    Executes (using exec, replacing the current process)
    the specified command with the restic environment
    variables set.

    This can be used to run manual restic commands:

    jgrestic enter config.json restic snapshots
    """
    c = config.load(config_json)
    if cmd[0] == "restic":
        cmd = (str(restic), *cmd[1:])
    os.execvpe(cmd[0], cmd, c.extend_env())
