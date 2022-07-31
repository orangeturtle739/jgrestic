import subprocess
import typing as t

import click

from jgrestic import config
from jgrestic.commands import restic


@click.command()
@click.argument("config_json", type=click.File("r"))
def init(config_json: t.TextIO) -> None:
    """
    Creates a new restic respository using the given CONFIG_JSON.

    The new repository uses the key file from the CONFIG_JSON, but also has
    a password as an additional key.
    """
    c = config.load(config_json)
    subprocess.run(
        [str(restic), "init"],
        check=True,
        env=c.extend_env(),
    )
    subprocess.run(
        [str(restic), "key", "add"],
        check=True,
        env=c.extend_env(),
    )
    click.secho(f"Done!", fg="green")
