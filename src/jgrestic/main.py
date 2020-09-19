import click

from jgrestic.backup import backup
from jgrestic.enter import enter


@click.group()
@click.version_option()
def main() -> None:
    """
    Restic backup tool.
    """
    pass


main.add_command(backup)
main.add_command(enter)
