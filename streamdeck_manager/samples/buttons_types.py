import os
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.entities import Button, Margin, Point2D


def custom_callback():
    print("middle callback called!")


def end_sample_callback():
    exit(0)


def set_middle_row(deck, asset_path):
    for key in deck.panel.get_row_range(int(deck.panel.rows/2)):
        button = Button(name=f"key{key}",
            icon = os.path.join(asset_path, "plus.png"),
            label=f"key{key}",
            label_pressed="pressed",
            margin=Margin(top=0, right=0, bottom=20, left=0),
            label_pos=Point2D(x=deck.image_size[0]/2, y=deck.image_size[1] - 5)
        )
        deck.panel.set_button(key, button)

def set_middle_col(deck, asset_path):
    for key in deck.panel.get_col_range(int(deck.panel.cols/2)):
        button = Button(name=f"key{key}", 
            label=f"key{key}",
            label_pressed="pressed",
            icon=os.path.join(asset_path, "minus.png"),
            margin=Margin(top=20, right=0, bottom=0, left=0),
            label_pos=Point2D(x=deck.image_size[0]/2, y=15)
        )
        deck.panel.set_button(key, button)


def set_corners(deck):
    deck.panel.set_button(deck.panel.top_left_key, Button(background="white"))
    deck.panel.set_button(deck.panel.top_right_key, Button(background="red"))
    deck.panel.set_button(deck.panel.bottom_left_key, Button(background="green"))
    deck.panel.set_button(deck.panel.bottom_right_key, Button(background="blue"))


def set_center_button(deck, asset_path):
    button = Button(
        icon=os.path.join(asset_path, "warning.png"),
        icon_pressed=os.path.join(asset_path, "warning.png"),
        callback=custom_callback
    )
    deck.panel.set_button(deck.panel.center_key, button)


def set_last_button(deck, asset_path):
    button = Button(
        name="exit", 
        label="exit",
        icon=os.path.join(asset_path, "eject.png"),
        callback=end_sample_callback
    )
    deck.panel.set_button(deck.panel.last_key, button)


def main(device_id: int=0,
         asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets")
         ):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit()

    core.initialize_deck(device_id, asset_path=asset_path, font=os.path.join(asset_path, "Roboto-Regular.ttf"))

    for deck in core.decks:
        set_middle_row(deck, asset_path)
        set_middle_col(deck, asset_path)
        set_corners(deck)
        set_center_button(deck, asset_path)
        set_last_button(deck, asset_path)
        deck.render()

    core.run()

if __name__ == "__main__":
    typer.run(main)
