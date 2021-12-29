import os
import typer

from streamdeck_manager.core import Core


def end_sample_callback(**kwargs):
    exit(0)


def main(asset_path: str = None,
         font_path: str = None,
         photo: str = None):

    core = Core()

    if not photo:
        photo = os.path.join(core.asset_path, "Harold.jpg")
        typer.echo(f"Using default image {photo}")

    if len(core.streamdecks) <= 0:
        typer.echo("Not Stream deck found")
        raise typer.Exit(1)

    for index in core.device_ids:
        core.initialize_deck(index, asset_path=asset_path, font=font_path)

    for deck in core.decks:
        deck.set_background(photo_path=photo, callback=end_sample_callback)

    core.run()


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
