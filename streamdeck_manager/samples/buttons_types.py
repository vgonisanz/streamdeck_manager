"""
Several buttons and alignement using panel attributes to manage a
deck manually.

core.run() function will run all decks initialized (in this case
only one) until send signal KILL or push the quit button.
"""
import os
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.entities import Button, Margin, Point2D


def custom_callback(**kwargs):
    print("middle callback called!")


def end_sample_callback(**kwargs):
    exit(0)


def set_middle_row(deck, asset_path):
    for key in deck.panel.get_row_range(int(deck.panel.rows/2)):
        button = Button(name=f"key{key}",
            icon = "plus.png",
            label=f"key{key}",
            label_pressed="pressed",
            margin=Margin(top=0, right=0, bottom=20, left=0),
            label_pos=Point2D(x=deck.panel.image_size.width/2, y=deck.panel.image_size.height - 5)
        )
        deck.panel.set_button(key, button)

def set_middle_col(deck, asset_path):
    for key in deck.panel.get_col_range(int(deck.panel.cols/2)):
        button = Button(name=f"key{key}", 
            label=f"key{key}",
            label_pressed="pressed",
            icon="minus.png",
            margin=Margin(top=20, right=0, bottom=0, left=0),
            label_pos=Point2D(x=deck.panel.image_size.width/2, y=15)
        )
        deck.panel.set_button(key, button)


def set_corners(deck):
    deck.panel.set_button(deck.panel.top_left_key, Button(background="white"))
    deck.panel.set_button(deck.panel.top_right_key, Button(background="red"))
    deck.panel.set_button(deck.panel.bottom_left_key, Button(background="green"))
    deck.panel.set_button(deck.panel.bottom_right_key, Button(background="blue"))


def set_center_button(deck, asset_path):
    button = Button(
        icon="warning.png",
        icon_pressed="warning.png",
        callback=custom_callback
    )
    deck.panel.set_button(deck.panel.center_key, button)


def set_last_button(deck, asset_path):
    button = Button(
        name="exit", 
        label="exit",
        icon="eject.png",
        callback=end_sample_callback
    )
    deck.panel.set_button(deck.panel.last_key, button)


def main(device_id: int=0,
         asset_path: str = None,
         font_path: str = None):

    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit(1)

    deck = core.initialize_deck(device_id, asset_path=asset_path, font=font_path)

    set_middle_row(deck, asset_path)
    set_middle_col(deck, asset_path)
    set_corners(deck)
    set_center_button(deck, asset_path)
    set_last_button(deck, asset_path)
    deck.render()
    core.run()

def run():
    typer.run(main)


if __name__ == "__main__":
    run()
