import os
import logging

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper

logger = logging.getLogger(__name__) 


class Button():
    def __init__(self, deck, key, name, font, label='', label_pressed='', background='black'):
        """
        deck: Needed to generate image compatibles
        name: Name id for the image
        font: Text font
        label: Text of the label
        background: Color background if not image provided as icon
        """
        self._deck = deck
        self._key = key
        self._name = name
        self._top = 0
        self._right = 0
        self._bottom = 20
        self._left = 0
        self._font_size = 14
        self._font = ImageFont.truetype(font, self._font_size)
        self._label = label
        self._label_pressed = label_pressed
        self._background = background
        self._icon = None
        self._icon_pressed = None
        self._callback = None
        image = PILHelper.create_image(self._deck, background=self._background)
        self._image_width = image.width
        self._image_height = image.height
        self.autopadding_bottom()
        return
    
    def autopadding_bottom(self):
        """
        Set padding with text in the botton automatically
        """
        self._label_x = self._image_width / 2
        self._label_y = self._image_height - 5
        self.set_margins(top=0, right=0, bottom=20, left=0)
        return

    def autopadding_top(self):
        """
        Set padding with text in the top automatically
        """
        self._label_x = self._image_width / 2
        self._label_y = 15
        self.set_margins(top=20, right=0, bottom=0, left=0)
        return
    
    def autopadding_center(self):
        """
        Set padding with text in the center automatically
        """
        self._label_x = self._image_width / 2
        self._label_y = self._image_height / 2
        self.set_margins(top=0, right=0, bottom=0, left=0)
        return
    
    def set_callback(self, callback):
        self._callback = callback

    def key_change_callback(self, state):
        if state:
            if self._callback:
                self._callback()
        self.render(state)

    @property
    def font_size(self):
        return self._font_size
    
    def set_font_size(self, font_size):
        self._font_size = font_size

    @property
    def name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    @property
    def label(self):
        return self._label
    
    def set_label(self, label):
        self._label = label

    @property
    def label_pressed(self):
        return self._label_pressed
    
    def set_label_pressed(self, label_pressed):
        self._label_pressed = label_pressed

    @property
    def background(self):
        return self._background
    
    def set_background(self, background):
        self._background = background

    def set_key(self, key):
        self._key = key

    @property
    def margins(self):
        return [self._top, self._right, self._bottom, self._left]
    
    def set_margins(self, top, right, bottom, left):
        self._top = top
        self._right = right
        self._bottom = bottom
        self._left = left

    def set_icon(self, path):
        """
        Generate a Image object from a Image file
        """
        self._icon = Image.open(path)
    
    def set_icon_from_image(self, image):
        """
        Set the image directly
        """
        self._icon = image

    def set_icon_pressed(self, path):
        self._icon_pressed = Image.open(path)

    def set_icon_pressed_from_image(self, image):
        """
        Set the image directly
        """
        self._icon_pressed = image

    def _render_image(self, icon, label):
        if icon:
            image = PILHelper.create_scaled_image(self._deck, icon, margins=self.margins)
        else:
            image = PILHelper.create_image(self._deck, background=self._background)

        draw = ImageDraw.Draw(image)
        draw.text((self._label_x, self._label_y), text=label, font=self._font, anchor="ms", fill="white")

        return PILHelper.to_native_format(self._deck, image)

    def _render_pressed(self):
        render = self._render_image(self._icon_pressed, self._label_pressed)
        self._deck.set_key_image(self._key, render)

    def _render_released(self):
        render = self._render_image(self._icon, self._label)
        self._deck.set_key_image(self._key, render)

    def render(self, state=False):
        if state:
            self._render_pressed()
        else:
            self._render_released()
