"""
Basic sample to manage a deck and its panel manually.

core.run() function will run all decks initialized (in this case
only one) until send signal KILL or push the quit button.
"""
import os
import sys
import logging
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.entities import Button


def custom_callback():
    logging.info("callback called!")


def end_sample_callback():
    exit(0)


def set_buttons(deck, asset_path):
    for key in deck.panel.range_buttons:
        button = Button(name=f"key{key}", 
            label=f"key{key}",
            label_pressed="pressed")
        button.icon = os.path.join(asset_path, "released.png")
        button.icon_pressed = os.path.join(asset_path, "pressed.png")
        button.callback = custom_callback
        deck.panel.set_button(key, button)


def set_exit_button(deck, asset_path):
    button = Button(name="quit", 
        label=f"quit",
        label_pressed="bye!")
    button.icon = os.path.join(asset_path, "stop.png")
    button.callback = end_sample_callback
    deck.panel.set_button(deck.panel.last_key, button)


def main(device_id: int=0,
         asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets")
         ):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit(1)

    deck = core.initialize_deck(device_id, asset_path=asset_path, font=os.path.join(asset_path, "Roboto-Regular.ttf"))
    if not deck:
        raise typer.Exit(2)

    deck = core.get_deck(device_id)
    set_buttons(deck, asset_path)
    set_exit_button(deck, asset_path)
    deck.panel.autopadding_bottom()
    deck.render()
    core.run()


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
