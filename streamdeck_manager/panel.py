import logging

from streamdeck_manager.entities import (
    Margin,
    Point2D,
)

logger = logging.getLogger(__name__) 

class Panel():
    """
    Panel contain the buttons that fit in a deck and provide
    easy ways to find keys. Each deck have a unique panel
    where you can change the buttons and its callbacks
    to manage them.
    """
    def __init__(self, rows, cols, key_count, image_size):
        self._rows = rows
        self._cols = cols
        self._key_count = key_count
        self._image_size = image_size
        self._buttons = dict()
        self.reset()
        self.autopadding_bottom()
    
    def reset(self):
        for key in range(self._key_count):
            self._buttons[key] = None

    @property
    def key_count(self):
        return self._key_count

    @property
    def rows(self):
        return self._rows
    
    @property
    def cols(self):
        return self._cols
    
    @property
    def image_size(self):
        return self._image_size

    def get_button(self, key):
        if not key in self._buttons:
            logger.warning(f"Button {key} do not exist")
            return None
        return self._buttons[key]
    
    def set_button(self, key, button):
        if not key in self._buttons:
            logger.warning(f"Button {key} do not exist")
            return

        self._buttons[key] = button

    def get_buttons(self):
        return self._buttons

    @property
    def range_buttons(self):
        """
        Return enumerator with all buttons
        """
        return range(0, self.last_key)
    
    def get_row_range(self, i):
        """
        Return enumerator with i-th row buttons. This iterator is empty if out of range.
        """
        value = iter([])
        if i >= 0 and i < self.rows:
            start = i * self.cols
            end = start + self.cols
            value = range(start, end)
        return value
    
    def get_col_range(self, j):
        """
        Return enumerator with j-th col buttons. This iterator is empty if out of range.
        """
        value = iter([])
        if j >= 0 and j < self.cols:
            start = j
            end = start + self.cols * self.rows
            value = range(start, end, self.cols)
        return value
    
    @property
    def last_key(self):
        return self.key_count - 1
    
    @property
    def center_key(self):
        return int(self.key_count / 2)

    @property
    def top_left_key(self):
        return self.get_row_range(0)[0]

    @property
    def top_right_key(self):
        return self.get_row_range(0)[-1]

    @property
    def bottom_left_key(self):
        return self.get_row_range(self.rows - 1)[0]

    @property
    def bottom_right_key(self):
        return self.get_row_range(self.rows - 1)[-1]

    def set_margins(self, top, right, bottom, left):
        for _, button in self._buttons.items():
            if not button:
                continue

            button.margin = Margin(top=top, right=right, bottom=bottom, left=left)

    def set_label_pos(self, x, y):
        for _, button in self._buttons.items():
            if not button:
                continue

            button.label_pos = Point2D(x=x, y=y)
    
    def autopadding_bottom(self):
        """
        Set padding with text in the botton automatically for all attached buttons
        """
        self.set_label_pos(self._image_size.width / 2, self._image_size.height - 5)
        self.set_margins(top=0, right=0, bottom=20, left=0)
        return

    def autopadding_top(self):
        """
        Set padding with text in the top automatically for all attached buttons
        """
        self.set_label_pos(self._image_size.width / 2, 15)
        self.set_margins(top=20, right=0, bottom=0, left=0)
        return
    
    def autopadding_center(self):
        """
        Set padding with text in the center automatically for all attached buttons
        """
        self.set_label_pos(self._image_size.width / 2, self._image_size.height / 2)
        self.set_margins(top=0, right=0, bottom=0, left=0)
        return