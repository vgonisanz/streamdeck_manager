import os
import typer

from streamdeck_manager.core import Core
from streamdeck_manager.fsm.menu import Menu
from streamdeck_manager.entities import Button, Point2D


def button_callback(**kwargs):
    typer.echo(f"Button pushed {kwargs}")
    typer.echo(kwargs)


def main(device_id: int=0,
         iterations: int=1,
         asset_path: str=None):

    core = Core()

    if len(core.streamdecks) <= 0:
        typer.echo("Not Stream deck found")
        raise typer.Exit(1)

    deck = core.initialize_deck(device_id)
    if not deck:
        raise typer.Exit(2)

    menu = Menu(deck, back_icon_path="eject.png",
                next_icon_path="next.png",
                previous_icon_path="back.png")

    buttons = []
    buttons.append(Button(label=f"exit", label_pressed='bye!', callback=menu.exit,
                          label_pos=Point2D(x=deck.image_size[0]/2, y=deck.image_size[1]/2)))
    for index in range(1, 30):
        button = Button(label=f"nº: {index}", label_pressed='pressed', callback=button_callback,
                        label_pos=Point2D(x=deck.image_size[0]/2, y=deck.image_size[1]/2))
        buttons.append(button)
       
    menu.set_buttons(buttons)

    for loop in range(0, iterations):
        typer.echo(f"loop: {loop+1}/{iterations}, press back to next one")
        menu.wait()
        menu.reset()
    typer.echo("Last menu executed")


def run():
    typer.run(main)


if __name__ == "__main__":
    run()
