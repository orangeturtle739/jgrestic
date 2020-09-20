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
    # Running restic unlock first allows jgrestic to automatically
    # recover from cases where the lock file wasn't cleaned up last time.
    # This normally only happens due to a network error.
    # Accoring to:
    # a) https://github.com/restic/restic/issues/1959#issuecomment-414032658
    # b) https://github.com/vmware-tanzu/velero/issues/1511#issuecomment-511958791
    # restic unlock should always be safe because of the way locks work.
    # Any long-running restic operation refreshes its lock every 5 minutes by creating
    # a new lock file in the repo with an updated timestamp and removing the old one.
    # restic unlock then only removes "stale locks", and a lock is considered stale if either:
    #   1)  It is more than 30 minutes old
    #   2)  It was created on the same host as restic unlock is currently running on,
    #       and the process that created the lock cannot be reached using a SIGHUP signal.
    click.secho(f"Running unlock", fg="yellow")
    subprocess.run(
        [str(restic), "unlock"], check=True, env=c.extend_env(),
    )
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
