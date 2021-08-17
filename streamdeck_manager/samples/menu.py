import os
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.fsm.menu import Menu
from streamdeck_manager.entities import Button, Point2D


def button_callback():
    print("Button pushed")


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
            button = Button(label=f"nº: {index}", label_pressed='pressed', callback=button_callback,
                            label_pos=Point2D(x=deck.image_size[0]/2, y=deck.image_size[1]/2))
            buttons.append(button)

        menu = Menu(deck, back_icon_path=os.path.join(asset_path, "eject.png"),
                    next_icon_path=os.path.join(asset_path, "next.png"),
                    previous_icon_path=os.path.join(asset_path, "back.png")
        )
        menu.set_buttons(buttons)
        menu.wait()
        #menu.run()
        print("no wait")

    # TODO button.autopadding_center()
    #core.run()


if __name__ == "__main__":
    typer.run(main)
