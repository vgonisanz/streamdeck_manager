"""
Print in stdout info about all stream connected
"""
import os
import typer

from streamdeck_manager.core import Core


def main(asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets")):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit(1)

    for index in core.device_ids:
        core.initialize_deck(index, asset_path=asset_path, font=os.path.join(asset_path, 'Roboto-Regular.ttf'))

    for deck in core.decks:
        deck.info()


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
