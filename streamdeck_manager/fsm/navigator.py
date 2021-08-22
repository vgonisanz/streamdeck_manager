import os
import logging
import threading

from streamdeck_manager.fsm.base import FSMBase
from streamdeck_manager.fsm.menu import Menu
from streamdeck_manager.entities import Button, Point2D, Margin

logger = logging.getLogger(__name__) 

class Navigator(FSMBase):
    """
    Navigator is a finite state machine to manage automatically navigate
    through folders using enus. When a button with a folder is pressed,
    automatically enter in that folder showing files and folders. You can
    navigate back pressing back button. If back is pushed in root folder,
    the FSM go to end state.
    """
    def __init__(self, deck, root_path, end_callback=None):
        self._set_up_fsm(end_callback)
        
        self._deck = deck
        self._root_path = root_path
        self._relative_path = ''
        self._menu = Menu(deck,
                back_icon_path=os.path.join(deck.asset_path, "eject.png"),
                next_icon_path=os.path.join(deck.asset_path, "next.png"),
                previous_icon_path=os.path.join(deck.asset_path, "back.png"),
                end_callback=self.press_back
        )
        self._back_button_index = 0
        

    def _set_up_fsm(self, end_callback):
        super().__init__()
        states = [ 
            "root_folder",
            "childen_folder"
        ]
        self._append_states(states)
        self._create_fsm(model=self, initial="root_folder",
                         after_start=self._update_level,
                         before_end=end_callback)
        self._machine.add_transition(
            trigger='press_back',
            source='root_folder',
            dest='end',
            before=self._reset_elements,
            after=self._release
        )
        self._machine.add_transition(
            trigger='press_back',
            source='childen_folder',
            dest='childen_folder',
            conditions=[self._is_not_root_folder],
            before=self._go_down,
            after=self._update_level
        )
        self._machine.add_transition(
            trigger='press_back',
            source='childen_folder',
            dest='root_folder',
            conditions=[self._is_target_folder_root],
            before=self._go_down,
            after=self._update_level
        )
        self._machine.add_transition(
            trigger='press_folder',
            source='root_folder',
            dest='childen_folder',
            before=None,
            after=self._update_level
        )
        self._machine.add_transition(
            trigger='press_folder',
            source='childen_folder',
            dest='childen_folder',
            before=None,
            after=self._update_level
        )

    def _is_target_folder_root(self):
        if os.path.split(self._relative_path)[0] == '':
            return True
        return False

    def _is_not_root_folder(self):
        return not self._is_target_folder_root()

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
                previous_icon_path=os.path.join(asset_path, "back.png"),
                end_callback=self.press_back
        )
        file_tuple = next(os.walk(path))
        for dir in file_tuple[1]:
            buttons.append(self._create_dir_button(dir))
        for filename in file_tuple[2]:
            buttons.append(self._create_file_button(filename))
        menu.set_buttons(buttons)
        menu.run()

    def _go_up(self, filename):
        logger.debug(f"Go up to folder {filename}")
        self._relative_path = os.path.join(self._relative_path, filename)

    def _go_down(self):
        self._relative_path = os.path.split(self._relative_path)[0]
        logger.debug(f"Go down to folder {self._relative_path}")

    def _on_click(self, **kwargs):
        filename = kwargs["name"]
        logger.debug(f"_on_click {filename}")
        abspath = os.path.join(self._root_path, self._relative_path, filename)
        if self._is_folder(abspath):
            self._go_up(filename)
            self.press_folder()
        
    def _reset_elements(self):
        """
        Set black buttons in page
        """
        for k in range(self._deck.panel.key_count):
            self._deck.panel.set_button(k, Button(background="black"))
    
    def _ext_from_file(self, filename):
        return os.path.splitext(filename)[-1].replace(".", "")

    def _create_dir_button(self, dir):
        return Button(name=f"{dir}",
                      label=f"{dir}", label_pressed="go up",
                      icon=os.path.join(self._deck.asset_path, "folder.png"),
                      label_pos=Point2D(x=self._deck.panel.image_size.width/2, y=self._deck.panel.image_size.height*2/3),
                      callback=self._on_click,
                      kwargs=dict(name=dir))
    
    def _create_file_button(self, filename):
        ext = self._ext_from_file(filename)
        return Button(name=f"{filename}",
                      label=f"{filename}", label_pressed="",
                      label_pos=Point2D(x=self._deck.panel.image_size.width/2, y=self._deck.panel.image_size.height - 5),
                      icon=os.path.join(self._deck.asset_path, "files", f"{ext}.png"),
                      margin=Margin(top=0, right=0, bottom=20, left=0),
                      callback=self._on_click,
                      kwargs=dict(name=filename))
