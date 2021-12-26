import os
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.fsm.navigator import Navigator


def main(device_id: int=0,
         root_path: str=os.path.join(os.path.dirname(__file__), "..", "assets"),
         asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets")
         ):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit(1)

    deck = core.initialize_deck(device_id, asset_path=asset_path, font=os.path.join(asset_path, "Roboto-Regular.ttf"))
    if not deck:
        raise typer.Exit(2)

    navigator = Navigator(deck, root_path, None)
    navigator.wait()


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
