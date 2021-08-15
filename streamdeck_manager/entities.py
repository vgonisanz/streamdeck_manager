import os
import logging

import typing
import pydantic


class Button(pydantic.BaseModel):
    name: str = ""
    label: str = ""
    label_pressed: str = ""
    background: str = "black"
    icon: str = ""
    icon_pressed: str = ""
    callback: typing.Callable = None

    def key_change_callback(self):
        if self.callback:
            self.callback()
