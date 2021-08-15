import os
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.menu import Menu
from streamdeck_manager.entities import Button


def end_sample_callback():
    exit(0)


def main(device_id: int=0,
         asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets")
         ):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit()

    font = os.path.join(asset_path, "Roboto-Regular.ttf")
    core.initialize_deck(device_id, asset_path=asset_path, font=font)

    for deck in core.decks:
        buttons = []
        for index in range(0, 30):
            # TODO check we can be refactored:
            # - Require a streamdeck obj private ¬¬
            # - Key is senseless in this context, not good idea put a button in a deck directly. Set key 0 in everybutton.
            # - font is absolute path, weird too. 
            button_name = f"nº: {index}"
            button = Button(deck._deck, key=0, name=button_name, font=font, label=button_name, label_pressed='pressed')
            button.autopadding_center()
            buttons.append(button)

        menu = Menu(deck)
        menu.set_buttons(buttons)
        menu.set_back_callback(end_sample_callback)
        menu.update()

    core.run()


if __name__ == "__main__":
    typer.run(main)
