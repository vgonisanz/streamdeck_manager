import os
import logging

logger = logging.getLogger(__name__) 

class Menu():
    def __init__(self, deck):
        self._deck = deck
        self._label_back = "back"
        self._label_next = "next"
        self._label_prev = "prev"
        self._icon_back = "eject.png"
        self._icon_next = "next.png"
        self._icon_prev = "back.png"
        self._buttons = []
        self._current_page = 0
        self._back_cb_ext = None
    
    def _back_cb(self):
        if self._back_cb_ext:
            self._back_cb_ext()
    
    def _next_cb(self):
        if self._current_page < len(self._buttons)/(self._deck.key_count - 3) - 1:
            self._current_page += 1
            self.update()
    
    def _prev_cb(self):
        if self._current_page > 0:
            self._current_page -= 1
            self.update()

    def _update_icons(self):
        menu_button = self._deck.get_col_range(self._deck.cols - 1)[-3:]
        self._deck.update_button(key=menu_button[0],
                                 name=self._label_back,
                                 label=self._label_back, label_pressed="",
                                 icon=self._icon_back)
        self._deck.update_button(key=menu_button[1],
                                 name=self._label_next,
                                 label=self._label_next, label_pressed="",
                                 icon=self._icon_next)
        self._deck.update_button(key=menu_button[2],
                                 name=self._label_prev,
                                 label=self._label_prev, label_pressed="",
                                 icon=self._icon_prev)
        
        self._deck.get_button(menu_button[0]).set_callback(self._back_cb)
        self._deck.get_button(menu_button[1]).set_callback(self._next_cb)
        self._deck.get_button(menu_button[2]).set_callback(self._prev_cb)

        elements_per_page = self._deck.key_count - len(menu_button)
        start_index = elements_per_page * self._current_page

        index = 0
        remove = False

        for k in range(self._deck.key_count):
            if k in menu_button:
                continue

            current_index = start_index + index

            if current_index > len(self._buttons) - 1:
                remove = True

            if not remove:
                self._deck.set_button(k, self._buttons[current_index])
                index += 1
            else:
                self._deck.set_button(k, None)
        


    def set_back_callback(self, callback):
        self._back_cb_ext = callback

    def set_buttons(self, buttons):
        self._current_page = 0
        self._buttons = buttons

    def update(self):
        self._deck.reset()
        self._update_icons()
        self._deck.render()
