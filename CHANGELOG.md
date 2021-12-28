# Changelog

## 0.3.0 (Unreleased)

### Added

- ...

### Changed

- Navigator fsm now accept external callbacks to ease integrations.

## 0.2.0 (2021-12-26)

### Added

Basic core to manage a stream deck and several classes to create high level logic in the stream deck.

- core: Class to manage the stream deck initialization.
- entities: Different classes - Point2D, Size2D, Margin and Button.
- panel: Class to manage a stream deck view.
- fsm: Several finite state machines based on transitions to manage stream deck behaviors.
- assets: Added several assets to be used by default, like icons and other stuff. Some of
  them included originally on [stream-deck project](https://github.com/abcminiuser/python-elgato-streamdeck)
- samples: All ready samples (some from the original project and some news with this library)
