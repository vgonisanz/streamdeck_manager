# Streamdeck manager POC

This is a proof of concept to make different use cases in a easy way using any model
of elgato Stream Deck.

This library have been tested with:

- Stream deck model used have 3x5 buttons with 72x72 pixels of resolution each one.

## Installation

To install library dependencies take a loog into `docs/installation.md`:

- Fedora: Working.
- Ubuntu: Working.
- WSL2: Not USB support yet.

## Development

Follow installation instruction and instead install streamdeck_manager:

```bash
make env-create                                 # Only first time
source .tox/streamdeck_manager/bin/activate     # All bash session
```

## Samples

In a development bash, use `--help` to customize parameters:

### Device info

Read the HW info and print in stdout:

```bash
python streamdeck_manager/samples/device_info.py
```

### Basic buttons

Basic panel with buttons and callbacks:

```bash
python streamdeck_manager/samples/basic_usage.py
```

### More buttons

Another panel with different type of buttons:

```bash
python streamdeck_manager/samples/buttons_types.py
```

### Background photo

Set up a background image:

```bash
python streamdeck_manager/samples/tiled_image.py
```

### Menu widget

Run a Finite state machine with all buttons to navigate in several pages, the
FSM run iterations times (reset with back button):

```bash
python streamdeck_manager/samples/menu.py --iterations 2
```

## Credits

- vgonisanz
- streamdeck library base from `https://github.com/abcminiuser/python-elgato-streamdeck`
