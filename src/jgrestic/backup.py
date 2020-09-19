import subprocess
import typing as t

import click

from jgrestic import config
from jgrestic.commands import restic


@click.command()
@click.argument("config_json", type=click.File("r"))
def backup(config_json: t.TextIO) -> None:
    """
    Initiates a backup using the given CONFIG_JSON.
    """
    c = config.load(config_json)
    click.secho(f"Running forget", fg="yellow")
    subprocess.run(
        [str(restic), "forget", "--prune"] + c.forget.args,
        check=True,
        env=c.extend_env(),
    )
    click.secho(f"Running backup", fg="yellow")
    subprocess.run(
        [str(restic), "backup"] + c.backup.args, check=True, env=c.extend_env()
    )
    click.secho(f"Done!", fg="green")
