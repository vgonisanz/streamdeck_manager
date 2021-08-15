import os
import typer

from streamdeck_manager.core import Core


def end_sample_callback():
    exit(0)


def main(asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets"),
         photo: str="Harold.jpg"):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit()

    for index in core.device_ids:
        core.initialize_deck(index, asset_path=asset_path, font=os.path.join(asset_path, 'Roboto-Regular.ttf'))

    for deck in core.decks:
        deck.set_background(photo_path=photo, callback=end_sample_callback)
        deck.render()   # It is not needed, buttons are hidden, do not delete the image anymore
    
    core.run()


if __name__ == "__main__":
    typer.run(main)
