import os
import logging

from PIL import Image

logger = logging.getLogger(__name__) 


class Button():
    def __init__(self, name='', label='', label_pressed='', background='black'):
        """
        deck: Needed to generate image compatibles
        name: Name id for the image
        font: Text font
        label: Text of the label
        background: Color background if not image provided as icon
        """
        self._name = name
        self._label = label
        self._label_pressed = label_pressed
        self._background = background
        self._icon = None
        self._icon_pressed = None
        self._callback = None
        return
    
    def set_callback(self, callback):
        self._callback = callback

    def key_change_callback(self):
        if self._callback:
            self._callback()

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

    def get_background(self):
        return self._background

    def get_icon(self):
        return self._icon

    def get_icon_pressed(self):
        return self._icon_pressed

    def get_label(self):
        return self._label

    def get_label_pressed(self):
        return self._label_pressed

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
        Set the image directly, Needed? TODO remove if not
        """
        self._icon_pressed = image
