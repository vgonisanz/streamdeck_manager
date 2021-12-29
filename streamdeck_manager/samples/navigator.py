import os
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.fsm.navigator import Navigator


def main(device_id: int=0,
         root_path: str=None,
         asset_path: str=None,
         font_path: str=None):

    core = Core()

    if len(core.streamdecks) <= 0:
        typer.echo("Not Stream deck found")
        raise typer.Exit(1)

    deck = core.initialize_deck(index=device_id, asset_path=asset_path, font=font_path)

    if not deck:
        raise typer.Exit(2)

    if not root_path:
        root_path = core.asset_path
        typer.echo(f"Not root path provided, assigning default path: {root_path}")
    
    navigator = Navigator(deck, root_path, None)
    navigator.wait()


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
