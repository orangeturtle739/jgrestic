import os
import typing as t
from pathlib import Path

import click

from jgrestic.restic_files import ResticFiles


@click.command()
@click.argument(
    "root", type=click.Path(file_okay=False, dir_okay=True, exists=True, writable=True)
)
@click.argument("cmd", nargs=-1, required=True)
def enter(root: str, cmd: t.List[str]) -> None:
    """
    Runs a given CMD in the restic enviroment located at ROOT.

    Executes (using exec, replacing the current process)
    the specified command with the restic environment
    variables set.

    This can be used to run manual restic commands:

    jgrestic enter restic snapshots
    """
    env = {**os.environ, **ResticFiles.from_root(Path(root)).env()}
    os.execvpe(cmd[0], cmd, env)
