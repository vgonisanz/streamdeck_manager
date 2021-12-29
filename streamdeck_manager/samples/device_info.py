"""
Print in stdout info about all stream connected
"""
import os
import typer

from streamdeck_manager.core import Core


def main():

    core = Core()

    if len(core.streamdecks) <= 0:
        typer.echo("Not Stream deck found")
        raise typer.Exit(1)

    for index in core.device_ids:
        typer.echo(f"Initializing stream deck with id: {index}")
        core.initialize_deck(index=index)

    for deck in core.decks:
        deck.info()


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
