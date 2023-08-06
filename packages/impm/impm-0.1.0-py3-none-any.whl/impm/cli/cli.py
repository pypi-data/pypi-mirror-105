from logging import getLogger
from pathlib import Path

import click

from impm import __version__
from impm.cli.logging import LOG_LEVELS, setup_logging

__all__ = ("run",)


PROG_NAME = "impm"


@click.group()
@click.version_option(__version__, "-v", "--version")
@click.option(
    "-l",
    "--log",
    type=click.Choice(LOG_LEVELS, case_sensitive=False),
    default=LOG_LEVELS[2],
    help="The level of verbosity to log at.",
)
@click.option(
    "-ll",
    "--detailed-logs/--no-detailed-logs",
    default=False,
    help="Whether to use the detailed logging format.",
)
def cli(log: str, detailed_logs: bool):
    setup_logging(level=log.upper(), detailed=detailed_logs)


@cli.command("check", help="Check a data pack for a module.json file.")
@click.argument(
    "data_pack_path",
    type=click.Path(exists=True, resolve_path=True),
    callback=lambda ctx, param, value: Path(value),
)
def cli_check(data_pack_path: Path):
    log = getLogger("cli")
    module_json_path = data_pack_path / "module.json"
    if module_json_path.exists():
        log.info(f"This data pack contains a module.json file.")
    else:
        log.warning(f"This data pack DOES NOT contain a module.json file.")


def run():
    cli(prog_name=PROG_NAME)
