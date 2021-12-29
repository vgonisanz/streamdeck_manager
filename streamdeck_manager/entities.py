import os
import logging

import typing
import pydantic

class Margin(pydantic.BaseModel):
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0


class Point2D(pydantic.BaseModel):
    x: int = 0
    y: int = 0


class Size2D(pydantic.BaseModel):
    width: int = 0
    height: int = 0


class Button(pydantic.BaseModel):
    name: str = ""
    label: str = ""
    label_pressed: str = ""
    background: str = "black"
    icon: str = ""
    icon_pressed: str = ""
    margin: Margin = Margin()
    label_pos: Point2D = Point2D()
    hidden: bool = False
    callback: typing.Callable = None
    kwargs: typing.Any = dict()

    def invoke_callback(self):
        if self.callback:
            full_kwargs = self.kwargs
            full_kwargs.update(dict(name=self.name, is_hidden=self.hidden))
            self.callback(**full_kwargs)
