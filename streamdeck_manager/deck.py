import os
import threading
import logging

from streamdeck_manager.button import Button
from streamdeck_manager.utils import (
    create_full_deck_sized_image,
    crop_key_image_from_deck_sized_image
)

logger = logging.getLogger(__name__) 

class Deck():
    def __init__(self, deck, asset_path, font):
        """
        deck: Deck device
        asset_path: Absolute root path for relative assets
        font: Absolute path with a valid ttf font (not relative to asset)
        """
        self._asset_path = asset_path
        self._font = font
        self._deck = deck

        self._deck.open()
        self._deck.reset()
        self._deck.set_brightness(30)

        self._buttons = dict()
        for key in range(deck.key_count()):
            self._buttons[key] = Button(self._deck, key, name='',
                                        font=self._font, label='',
                                        label_pressed='', background='black')

        self._deck.set_key_callback(self._key_change_callback)

        logger.info(f"Opened {self.type} device with id {self.id})")
        return
    
    def __del__(self):
        """
        Avoid error when kill with a signal
        """
        for t in threading.enumerate():
            if t is threading.currentThread():
                t.is_alive()

    def _key_change_callback(self, deck, key, state):
        logging.debug(f"Button callback in deck: {deck.id()} key: {key} state: {state}")
        if key in self._buttons:
            self._buttons[key].key_change_callback(state)

    def close(self):
        with self._deck:
            logger.debug(f"Closing deck with index: {self.id}")
            self._deck.reset()
            self._deck.close()
    
    def update_button(self, key, name, label="", label_pressed="", icon="", icon_pressed="", background="black", render=True):
        if key > self.last_key:
            logger.warning(f"Key {key} is too high")
            return
        
        if key < 0:
            logger.warning(f"Key {key} is too low")
            return

        self._buttons[key].set_name(name)
        self._buttons[key].set_label(label)
        self._buttons[key].set_label_pressed(label_pressed)
        self._buttons[key].set_background(background)
        if icon != "":
            self._buttons[key].set_icon(os.path.join(self._asset_path, icon))
        if icon_pressed != "":
            self._buttons[key].set_icon_pressed(os.path.join(self._asset_path, icon_pressed))
        if render:
            self._buttons[key].render()

    def reset(self):
        self._deck.reset()

    def render(self):
        for button in self._buttons.values():
            button.render()

    def run(self):
        """
        Wait until all application threads have terminated (for this example,
        this is when all deck handles are closed).
        """
        logger.debug(f"Running deck {self.id}")

        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
    
    def info(self):
        flip_description = {
            (False, False): "not mirrored",
            (True, False): "mirrored horizontally",
            (False, True): "mirrored vertically",
            (True, True): "mirrored horizontally/vertically",
        }

        logger.info("")
        logger.info("Device info:")
        logger.info("------------")
        logger.info(f"\t - Is connected?:\t{self._deck.connected()}")
        logger.info(f"\t - Id:\t\t\t{self.id}")
        logger.info(f"\t - Type:\t\t{self.type}")
        logger.info(f"\t - Key in total:\t{self._deck.key_count()}")
        logger.info(f"\t - Rows:\t\t{self.rows}")
        logger.info(f"\t - Cols:\t\t{self.cols}")
        logger.info(f"\t - Image size:\t\t{self.image_size}")
        logger.info(f"\t - Image format:\t{self.image_format}")
        logger.info(f"\t - Image flip:\t\t{flip_description[self.image_flip]}")
        logger.info(f"\t - Image rotation:\t{self.image_rotation}")
        #logger.info(f"\t - Serial number:\t{self.serialno}")   # Randomly freeze the device
        logger.info("")
        return
    
    @property
    def id(self):
        return self._deck.id()

    @property
    def type(self):
        return self._deck.deck_type()
    
    @property
    def serialno(self):
        return self._deck.get_serial_number()

    @property
    def last_key(self):
        return self._deck.key_count() - 1
    
    @property
    def center_key(self):
        return int(self._deck.key_count() / 2)

    @property
    def top_left_key(self):
        return self.get_row_range(0)[0]

    @property
    def top_right_key(self):
        return self.get_row_range(0)[-1]

    @property
    def bottom_left_key(self):
        return self.get_row_range(self.rows - 1)[0]

    @property
    def bottom_right_key(self):
        return self.get_row_range(self.rows - 1)[-1]
    
    @property
    def rows(self):
        return self._deck.key_layout()[0]
    
    @property
    def cols(self):
        return self._deck.key_layout()[1]
    
    @property
    def key_states(self):
        return self._deck.key_states()
    
    @property
    def image_size(self):
        return self._deck.key_image_format()["size"]
    
    @property
    def image_format(self):
        return self._deck.key_image_format()["format"]
    
    @property
    def image_flip(self):
        return self._deck.key_image_format()["flip"]
    
    @property
    def image_rotation(self):
        return self._deck.key_image_format()["rotation"]

    @property
    def range_buttons(self):
        """
        Return enumerator with all buttons
        """
        return range(0, self.last_key)
    
    def get_row_range(self, i):
        """
        Return enumerator with i-th row buttons. This iterator is empty if out of range.
        """
        value = iter([])
        if i >= 0 and i < self.rows:
            start = i * self.cols
            end = start + self.cols
            value = range(start, end)
        return value
    
    def get_col_range(self, j):
        """
        Return enumerator with j-th col buttons. This iterator is empty if out of range.
        """
        value = iter([])
        if j >= 0 and j < self.cols:
            start = j
            end = start + self.cols * self.rows
            value = range(start, end, self.cols)
        return value
    
    def get_button(self, key):
        if not key in self._buttons:
            logger.warning(f"Button {key} do not exist")
            return None
        return self._buttons[key]
    
    def set_background(self, photo_path, callback, render=True):
        # Approximate number of (non-visible) pixels between each key, so we can
        # take those into account when cutting up the image to show on the keys.
        key_spacing = (36, 36)

        image = create_full_deck_sized_image(self._deck, key_spacing, os.path.join(self._asset_path, photo_path))

        logging.info("Created full deck image size of {}x{} pixels.".format(image.width, image.height))

        key_images = dict()
        for k in range(self._deck.key_count()):
            key_images[k] = crop_key_image_from_deck_sized_image(self._deck, image, key_spacing, k)
            button = self.get_button(k)
            button.set_icon_from_image(key_images[k])
            button.set_callback(callback)
            button.autopadding_center()

        if render:
            self.render()