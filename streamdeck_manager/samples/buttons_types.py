import os
import typer

from streamdeck_manager.core import Core


def custom_callback():
    print("callback called!")


def end_sample_callback():
    exit(0)


def set_middle_row(deck):
    for key in deck.get_row_range(int(deck.rows/2)):
        deck.update_button(
            key=key,
            name=f'key{key}', 
            label=f'key{key}',
            icon="plus.png"
        )

def set_middle_col(deck):
    for key in deck.get_col_range(int(deck.cols/2)):
        deck.update_button(
            key=key,
            name=f'key{key}', 
            label=f'key{key}',
            icon="minus.png"
        )
        deck.get_button(key).autopadding_top()


def set_corners(deck):
    deck.update_button(
        key=deck.top_left_key,
        name='top_left_key', 
        background="white"
    )
    deck.update_button(
        key=deck.top_right_key,
        name='top_right_key', 
        background="red"
    )
    deck.update_button(
        key=deck.bottom_left_key,
        name='bottom_left_key', 
        background="blue"
    )
    deck.update_button(
        key=deck.bottom_right_key,
        name='bottom_right_key', 
        background="green"
    )


def set_center_button(deck):
    deck.update_button(
        key=deck.center_key,
        name='warning', 
        label='warning',
        icon="warning.png"
    )
    button = deck.get_button(deck.center_key)
    button.set_callback(custom_callback)
    button.autopadding_center()


def set_last_button(deck):
    deck.update_button(
        key=deck.last_key,
        name='exit', 
        label='exit',
        icon="stop.png"
    )
    button = deck.get_button(deck.last_key)
    button.set_callback(end_sample_callback)
    button.autopadding_center()


def main(device_id: int=0,
         asset_path: str=os.path.join(os.path.dirname(__file__), "..", "assets")
         ):
    core = Core()

    if len(core.streamdecks) <= 0:
        print("Not Stream deck found")
        raise typer.Exit()

    core.initialize_deck(device_id, asset_path=asset_path, font=os.path.join(asset_path, "Roboto-Regular.ttf"))

    for deck in core.decks:
        set_middle_row(deck)
        set_middle_col(deck)
        set_corners(deck)
        set_center_button(deck)
        set_last_button(deck)
        deck.render()
        deck.info()
        deck.run()

    core.run()

if __name__ == "__main__":
    typer.run(main)
