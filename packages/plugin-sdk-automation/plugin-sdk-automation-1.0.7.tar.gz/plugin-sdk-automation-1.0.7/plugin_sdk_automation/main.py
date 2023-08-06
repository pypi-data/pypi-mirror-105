import logging

import click
from plugin_sdk_automation.handlers import DockerHandler
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

install()

console = Console()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
st = RichHandler()
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s")
st.setFormatter(fmt)
log.addHandler(st)


@click.group(invoke_without_command=True)
@click.option("--debug", default=False, is_flag=True)
@click.pass_context
def cli(ctx, debug):
    console.log(f"Debug is: {debug}")
    if debug:
        log.setLevel(logging.DEBUG)
    if ctx.invoked_subcommand is None:
        console.log("No subcommand provided, executing build")
        ctx.invoke(build)


@cli.command()
@click.option("--directory", "-d")
def build(directory: str):
    d = DockerHandler(log=log, directory=directory)
    d.build()


def main():

    cli()


if __name__ == "__main__":
    main()
