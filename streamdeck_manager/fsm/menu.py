import logging

from streamdeck_manager.fsm.base import FSMBase
from streamdeck_manager.entities import Button


logger = logging.getLogger(__name__) 

class Menu(FSMBase):
    """
    Menu is a finite state machine to manage automatically a list of
    buttons. This class update the panel automatically and provide a navigation
    FSM using its buttons. The back button set the FSM to the end
    state and release the control with a thread called wait function.
    """
    def __init__(self, deck, back_icon_path, next_icon_path, previous_icon_path, end_callback=None):
        self._set_up_fsm(end_callback)
        
        self._deck = deck
        self._label_back = "back"
        self._label_next = "next"
        self._label_prev = "prev"
        self._icon_back = back_icon_path
        self._icon_next = next_icon_path
        self._icon_prev = previous_icon_path
        self._buttons = []
        self._current_page = 0
        self._menu_button_index = self._deck.panel.get_col_range(self._deck.panel.cols - 1)[-3:]
        self._create_menu_buttons()

    def _set_up_fsm(self, end_callback):
        super().__init__()
        states = [ 
            "in_page_current",
        ]
        self._append_states(states)
        self._create_fsm(model=self, initial="in_page_current",
                         before_start=None, after_start=self._update,
                         before_end=end_callback)
        self._machine.add_transition(
            trigger='press_back',
            source='in_page_current',
            dest='end',
            before=end_callback,    # Don't forget end_ballback in dest end states always
            after=self._release
        )
        self._machine.add_transition(
            trigger='press_next',
            source='in_page_current',
            dest='in_page_current',
            conditions=[self._next_page],
            before=self._update
        )
        self._machine.add_transition(
            trigger='press_prev',
            source='in_page_current',
            dest='in_page_current',
            conditions=[self._prev_page],
            before=self._update
        )

    def _create_menu_buttons(self):
        self._deck.panel.set_button(self._menu_button_index[0],
                              Button(name=self._label_back,
                                     label=self._label_back, label_pressed="",
                                     icon=self._icon_back,
                                     callback = self.press_back)
        )
        self._deck.panel.set_button(self._menu_button_index[2],
                              Button(name=self._label_next,
                                     label=self._label_next, label_pressed="",
                                     icon=self._icon_next,
                                     callback = self.press_next)
        )
        self._deck.panel.set_button(self._menu_button_index[1],
                              Button(name=self._label_prev,
                                     label=self._label_prev, label_pressed="",
                                     icon=self._icon_prev,
                                     callback = self.press_prev)
        )

    def _next_page(self, **kwargs):
        """
        Move to next page unless is the last one
        """
        if self._current_page < len(self._buttons)/(self._deck.panel.key_count - 3) - 1:
            self._current_page += 1
            return True
        return False
    
    def _prev_page(self, **kwargs):
        """
        Move to previous page unless is the first one
        """
        if self._current_page > 0:
            self._current_page -= 1
            return True
        return False

    def _update_buttons(self):
        """
        Set up all buttons except menu
        """
        element_index_in_page = 0
        elements_per_page = self._deck.panel.key_count - len(self._menu_button_index)
        start_index = elements_per_page * self._current_page

        for k in range(self._deck.panel.key_count):
            if k in self._menu_button_index:
                continue

            current_index = start_index + element_index_in_page

            if current_index > len(self._buttons) - 1:
                continue

            self._deck.panel.set_button(k, self._buttons[current_index])
            element_index_in_page += 1

    def _reset_elements(self):
        """
        Set black buttons in page
        """
        for k in range(self._deck.panel.key_count):
            if not k in self._menu_button_index:
                self._deck.panel.set_button(k, Button(background="black"))

    def set_buttons(self, buttons):
        self._current_page = 0
        self._buttons = buttons

    def _update(self, **kwargs):
        self._reset_elements()
        self._update_buttons()
        self._deck.render()
