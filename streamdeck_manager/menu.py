import os
import logging

from streamdeck_manager.entities import Button

logger = logging.getLogger(__name__) 

class Menu():
    def __init__(self, deck, back_icon_path, next_icon_path, previous_icon_path):
        self._deck = deck
        self._label_back = "back"
        self._label_next = "next"
        self._label_prev = "prev"
        self._icon_back = back_icon_path
        self._icon_next = next_icon_path
        self._icon_prev = previous_icon_path
        self._buttons = []
        self._current_page = 0
        self._menu_button_index = self._deck.get_col_range(self._deck.cols - 1)[-3:]
        self._create_menu_buttons()
    
    def _create_menu_buttons(self):
        self._deck.set_button(self._menu_button_index[0],
                              Button(name=self._label_back,
                                     label=self._label_back, label_pressed="",
                                     icon=self._icon_back)
        )
        self._deck.set_button(self._menu_button_index[1],
                              Button(name=self._label_next,
                                     label=self._label_next, label_pressed="",
                                     icon=self._icon_next,
                                     callback = self._next_cb)
        )
        self._deck.set_button(self._menu_button_index[2],
                              Button(name=self._label_prev,
                                     label=self._label_prev, label_pressed="",
                                     icon=self._icon_prev,
                                     callback = self._prev_cb)
        )

    def _next_cb(self):
        if self._current_page < len(self._buttons)/(self._deck.key_count - 3) - 1:
            self._current_page += 1
            self.update()
    
    def _prev_cb(self):
        if self._current_page > 0:
            self._current_page -= 1
            self.update()

    def _update_buttons(self):
        """
        Set up all buttons except menu
        """
        element_index_in_page = 0
        elements_per_page = self._deck.key_count - len(self._menu_button_index)
        start_index = elements_per_page * self._current_page

        for k in range(self._deck.key_count):
            if k in self._menu_button_index:
                continue

            current_index = start_index + element_index_in_page

            if current_index > len(self._buttons) - 1:
                continue

            self._deck.set_button(k, self._buttons[current_index])
            element_index_in_page += 1
            

    def set_back_callback(self, callback):
        back_button = self._deck.get_button(self._menu_button_index[0])
        back_button.callback = callback

    def set_buttons(self, buttons):
        self._current_page = 0
        self._buttons = buttons

    def _reset_elements(self):
        """
        Set black buttons in page
        """
        for k in range(self._deck.key_count):
            if not k in self._menu_button_index:
                self._deck.set_button(k, Button(background="black"))

    def update(self):
        self._reset_elements()
        self._update_buttons()
        self._deck.render()
