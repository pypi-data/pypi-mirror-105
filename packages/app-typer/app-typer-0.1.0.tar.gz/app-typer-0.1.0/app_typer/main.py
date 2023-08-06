from app_typer import __version__
from typing import Optional

import typer

app = typer.Typer()
state = {"verbose": False}


def version_callback(value: bool):
    if value:
        typer.secho(f"CLI Version: {__version__}", fg=typer.colors.MAGENTA)
        raise typer.Exit()


# Main command
@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None, "--version", callback=version_callback, is_eager=True
        ),
        verbose: bool = False,
):
    """
    A demo(template) for CLI app.
    """
    if verbose:
        typer.echo("set verbose output")
        state["verbose"] = True


# Add more sub-commands
@app.command()
def greeting(
        user: str = typer.Argument(..., envvar="USER", help="the user to greet"),
        greet: str = typer.Option("Hello", help="greeting word"),
):
    if state["verbose"]:
        typer.echo("About to greet user...")
    typer.echo(f"{greet}, {user}!")


if __name__ == "__main__":
    app()
