import os
import threading
import logging

from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont

from streamdeck_manager.entities import (
    Button,
    Margin,
    Point2D,
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

        self._image_size = Size2D(width=self.image_size[0], height=self.image_size[1])

        self._buttons = dict()
        self.reset()
        self.autopadding_bottom()

        self._deck.set_key_callback(self._invoke_callback)

        logger.info(f"Opened {self.type} device with id {self.id})")
        return
    
    def __del__(self):
        """
        Avoid error when kill with a signal
        """
        for t in threading.enumerate():
            if t is threading.currentThread():
                t.is_alive()

    def _invoke_callback(self, deck, key, state):
        logging.debug(f"Button callback in deck: {deck.id()} key: {key} state: {state}")
        if key in self._buttons:
            if self._buttons[key] != None:
                if state:
                    self._buttons[key].invoke_callback()
                self._render_button(key, self._buttons[key], state)

    def close(self):
        with self._deck:
            logger.debug(f"Closing deck with index: {self.id}")
            self._deck.reset()
            self._deck.close()

    def reset(self):
        for key in range(self._deck.key_count()):
            self._buttons[key] = None

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
        for key, button in self._buttons.items():
            state = states[key]
            if button == None:
                continue
            if not button.hidden:
                self._render_button(key, button, state)  


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
    def key_count(self):
        return self._deck.key_count()

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
    def font_size(self):
        return self._font_size
    
    def set_font_size(self, font_size):
        self._font_size = font_size
    
    def set_margins(self, top, right, bottom, left):
        for _, button in self._buttons.items():
            if not button:
                continue

            button.margin = Margin(top=top, right=right, bottom=bottom, left=left)

    def set_label_pos(self, x, y):
        for _, button in self._buttons.items():
            if not button:
                continue

            button.label_pos = Point2D(x=x, y=y)

    def autopadding_bottom(self):
        """
        Set padding with text in the botton automatically
        """
        self.set_label_pos(self._image_size.width / 2, self._image_size.height - 5)
        self.set_margins(top=0, right=0, bottom=20, left=0)
        return

    def autopadding_top(self):
        """
        Set padding with text in the top automatically
        """
        self.set_label_pos(self._image_size.width / 2, 15)
        self.set_margins(top=20, right=0, bottom=0, left=0)
        return
    
    def autopadding_center(self):
        """
        Set padding with text in the center automatically
        """
        self.set_label_pos(self._image_size.width / 2, self._image_size.height / 2)
        self.set_margins(top=0, right=0, bottom=0, left=0)
        return

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
    
    def set_button(self, key, button):
        if not key in self._buttons:
            logger.warning(f"Button {key} do not exist")
            return

        self._buttons[key] = button


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
            self.set_button(key, button)

            # Manual draw the images
            self._draw_image(key, key_images[key])

        self.autopadding_center()
