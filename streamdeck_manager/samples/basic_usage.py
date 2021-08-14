import os
import logging
import typer

from streamdeck_manager.core import Core


def custom_callback():
    logging.info("callback called!")


def end_sample_callback():
    exit(0)


def set_buttons(deck):
    for key in deck.range_buttons:
        deck.update_button(
            key=key,
            name=f"key{key}", 
            label=f"key{key}",
            label_pressed="pressed",
            icon="released.png",
            icon_pressed="pressed.png"
        )
        deck.get_button(key).set_callback(custom_callback)

def set_exit_button(deck):
    deck.update_button(
        key=deck.last_key,
        name="exit", 
        label="exit",
        label_pressed="bye",
        icon="stop.png"
    )
    deck.get_button(deck.last_key).set_callback(end_sample_callback)


def main(device_id: int=0,
         asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets")
         ):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit()

    core.initialize_deck(device_id, asset_path=asset_path, font=os.path.join(asset_path, "Roboto-Regular.ttf"))

    for deck in core.decks:
        set_buttons(deck)
        set_exit_button(deck)
        deck.render()
    
    core.run()


if __name__ == "__main__":
    typer.run(main)
