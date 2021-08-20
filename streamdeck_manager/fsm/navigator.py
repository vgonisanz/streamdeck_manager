import os
import logging

from streamdeck_manager.fsm.base import FSMBase
from streamdeck_manager.fsm.menu import Menu
from streamdeck_manager.entities import Button, Point2D

logger = logging.getLogger(__name__) 

class Navigator(FSMBase):
    """
    Navigator is a finite state machine to manage automatically navigate
    through folders using enus. When a button with a folder is pressed,
    automatically enter in that folder showing files and folders. You can
    navigate back pressing back button. If back is pushed in root folder,
    the FSM go to end state.
    """
    def __init__(self, deck, root_path):
        self._set_up_fsm()
        
        self._deck = deck
        self._root_path = root_path
        self._relative_path = ''
        self._menu = Menu(deck,
                back_icon_path=os.path.join(deck.asset_path, "eject.png"),
                next_icon_path=os.path.join(deck.asset_path, "next.png"),
                previous_icon_path=os.path.join(deck.asset_path, "back.png")
        )
        self._back_button_index = 0
        

    def _set_up_fsm(self):
        super().__init__()
        states = [ 
            "root_folder",
            "childen_folder"
        ]
        self._append_states(states)
        self._create_fsm(model=self, initial="root_folder", before=self._update_level)#, after=self._update)
        self._machine.add_transition(
            trigger='press_back',
            source='root_folder',
            dest='end',
            before=self._update_level,
            after=self._release
        )
        self._machine.add_transition(
            trigger='press_back',
            source='childen_folder',
            dest='childen_folder',
            conditions=[not self._is_root_folder],
            before=self._update_level
        )
        self._machine.add_transition(
            trigger='press_back',
            source='childen_folder',
            dest='root_folder',
            conditions=[self._is_root_folder],
            before=self._update_level
        )
        self._machine.add_transition(
            trigger='press_folder',
            source='*',
            dest='childen_folder',
            before=self._update_level
        )
        # Press folder any got new one


    def _is_root_folder(self):
        if self._relative_path == '':
            return True
        return False

    def _is_folder(self, path):
        return os.path.isdir(path)
    
    def _get_folder_elements(self, path):
        return os.listdir(path)

    def _update_level(self):
        path = os.path.join(self._root_path, self._relative_path)
        logger.debug(f"Update path {path}")
        buttons = []
        asset_path = self._deck.asset_path
        menu = Menu(self._deck, back_icon_path=os.path.join(asset_path, "eject.png"),
                next_icon_path=os.path.join(asset_path, "next.png"),
                previous_icon_path=os.path.join(asset_path, "back.png")
        )
        buttons = []
        file_list = os.listdir(path)
        for file in file_list:
            # Check folder / file to set icon and callback
            print(file)
            button = Button(name="..",
                            label=f"{file}", label_pressed="",
                            label_pos=Point2D(x=self._deck.image_size[0]/2, y=self._deck.image_size[1]/2),
                            callback=self._pressed_element)
            buttons.append(button)
        menu.set_buttons(buttons)
        print("prewait")
        menu.wait()
        print("wait")
        #menu.reset()

    def _pressed_element(self):
        print("_pressed_element")
