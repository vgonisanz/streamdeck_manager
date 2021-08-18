import os
import coloredlogs
import logging

from streamdeck_manager.deck import Deck
from StreamDeck.DeviceManager import DeviceManager

logger = logging.getLogger(__name__) 

class Core():
    def __init__(self, log_level=logging.DEBUG, log_level_transitions=logging.ERROR):
        self._initialize_logs(log_level, log_level_transitions)

        self._cleanup_done = False
        self._streamdecks = DeviceManager().enumerate()
        self._decks = dict()

        logger.info(f"Found {len(self.streamdecks)} Stream Deck(s).")

    def __del__(self):
        if not self._cleanup_done:
            self.terminate()

    def _initialize_logs(self, log_level, log_level_transitions):
        coloredlogs.install(level=log_level)
        logging.getLogger("PIL.PngImagePlugin").setLevel(logging.INFO)
        logging.getLogger("transitions").setLevel(log_level_transitions)

    def initialize_deck(self, index, asset_path, font):
        if index >= len(self.streamdecks):
            logger.warning(f"Deck index {index} is too high")
            return None
        
        if index < 0:
            logger.warning(f"Deck index {index} is too low")
            return None

        logger.debug(f"Creating deck with index: {index}")
        self._decks[index] = Deck(self.streamdecks[index], asset_path=asset_path, font=font)
        return self.get_deck(index)

    @property
    def streamdecks(self):
        """
        A Stream deck is an object for the HW device from streamdeck library
        """
        self._streamdecks = DeviceManager().enumerate()
        return self._streamdecks
    
    @property
    def device_ids(self):
        """
        A list with device ids.
        """
        return list(range(len(self._streamdecks)))

    @property
    def decks(self):
        """
        A deck is our abstraction of a device to ease management. Naming can be confusing.
        """
        return self._decks.values()

    def get_deck(self, index):
        if index in self._decks:
            return self._decks[index]
        return None

    def run(self):
        for deck in self.decks:
            deck.run()

    def terminate(self):
        """
        Graceful close of the devices
        """
        for deck in self.decks:
            deck.close()
        self._cleanup_done = True