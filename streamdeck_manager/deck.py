import os
import threading
import logging

from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont

from streamdeck_manager.panel import Panel
from streamdeck_manager.entities import (
    Button,
    Size2D
)
from streamdeck_manager.utils import (
    create_full_deck_sized_image,
    crop_key_image_from_deck_sized_image
)

logger = logging.getLogger(__name__) 

class Deck():
    def __init__(self, deck, asset_path, font):
        """
        This class manage all calls related with a physical deck
        and manage its properties like panel buttons and
        its framebuffers.

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

        self._font_size = 14
        self._font = ImageFont.truetype(font, self._font_size)

        self._panel = Panel(rows=self._deck.key_layout()[0],
                            cols=self._deck.key_layout()[1],
                            key_count=self._deck.key_count(),
                            image_size=Size2D(width=self.image_size[0], height=self.image_size[1]))

        self._deck.set_key_callback(self._invoke_callback)

        logger.info(f"Opened {self.type} device with id {self.id})")
        return
    
    def __del__(self):
        """
        Avoid error when kill with a signal. TBR
        """
        for t in threading.enumerate():
            if t is threading.currentThread():
                t.is_alive()

    def _invoke_callback(self, deck, key, state):
        logging.debug(f"Button callback in deck: {deck.id()} key: {key} state: {state}")
        buttons = self._panel.get_buttons()
        if key in buttons:
            if buttons[key] != None:
                if state:
                    buttons[key].invoke_callback()
                self._render_button(key, buttons[key], state)

    def close(self):
        with self._deck:
            logger.debug(f"Closing deck with index: {self.id}")
            self._deck.reset()
            self._deck.close()


    def _draw_image(self, key, image):
        """
        Create drawable from PIL Image and send to stream deck key framebuffer
        """
        drawable = PILHelper.to_native_format(self._deck, image)
        self._deck.set_key_image(key, drawable)

    def _render_button(self, key, button, state):
        """
        Create image from file using PIL depending of the button status
        """
        if not state:
            icon = button.icon
            label = button.label
        else:
            icon = button.icon_pressed
            label = button.label_pressed

        if icon == '':
            image = PILHelper.create_image(self._deck, background=button.background)
        else:
            pre_image = Image.open(icon)
            margin = button.margin
            image = PILHelper.create_scaled_image(self._deck,
                        pre_image,
                        margins=[margin.top, margin.right, margin.bottom, margin.left])

        image_with_text = ImageDraw.Draw(image)
        label_positions = [button.label_pos.x, button.label_pos.y] 
        image_with_text.text(label_positions, text=label, font=self._font, anchor="ms", fill="white")

        self._draw_image(key, image)
        

    def render(self):
        states = self._deck.key_states()
        for key, button in self._panel.get_buttons().items():
            state = states[key]
            if button == None:
                continue
            if not button.hidden:
                self._render_button(key, button, state)  

    
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
        logger.info(f"\t - Rows:\t\t{self._panel.rows}")
        logger.info(f"\t - Cols:\t\t{self._panel.cols}")
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
    def font_size(self):
        return self._font_size
    
    @property
    def panel(self):
        return self._panel

    def set_font_size(self, font_size):
        self._font_size = font_size


    def set_background(self, photo_path, callback):
        """
        Set a image using all buttons and set up a callback. The image will be lost if
        use function render.
        """
        # Approximate number of (non-visible) pixels between each key, so we can
        # take those into account when cutting up the image to show on the keys.
        key_spacing = (36, 36)

        image = create_full_deck_sized_image(self._deck, key_spacing, os.path.join(self._asset_path, photo_path))

        logging.info("Created full deck image size of {}x{} pixels.".format(image.width, image.height))

        key_images = dict()
        for key in range(self._deck.key_count()):
            key_images[key] = crop_key_image_from_deck_sized_image(self._deck, image, key_spacing, key)

            # Use hidden button to have callback
            button = Button(hidden=True)
            button.callback = callback
            self._panel.set_button(key, button)

            # Manual draw the images
            self._draw_image(key, key_images[key])

        self._panel.autopadding_center()

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