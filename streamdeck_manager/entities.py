import os
import logging

import typing
import pydantic

class Margin(pydantic.BaseModel):
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0


class Button(pydantic.BaseModel):
    name: str = ""
    label: str = ""
    label_pressed: str = ""
    background: str = "black"
    icon: str = ""
    icon_pressed: str = ""
    margin: Margin = Margin()
    hidden: bool = False
    callback: typing.Callable = None

    def key_change_callback(self):
        if self.callback:
            self.callback()
    
    def get_margins(self):
        return [self.margin.top, self.margin.right, self.margin.bottom, self.margin.left]
