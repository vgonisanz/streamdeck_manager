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

In a development bash, use `--help` to customize parameters. If you install the library
a default folder with assets is installed. You may give another asset path to make them work
with your custom assets.

If you install the library use the entrypoint running the command in your bash. In development
you can run them directly the script given. Both support same options.

### Device info

Read the HW info and print in stdout.

![](images/device_info.png)

```bash
python streamdeck_manager/samples/device_info.py
```

Entrypoint: `sdm-info`

### Basic buttons

Basic panel with buttons and callbacks.

![](images/basic_usage.png)

```bash
python streamdeck_manager/samples/basic_usage.py
```

Entrypoint: `sdm-basic`

### More buttons

Another panel with different type of buttons.

![](images/buttons_types.png)

```bash
python streamdeck_manager/samples/buttons_types.py
```

Entrypoint: `sdm-more-buttons`

### Background photo

Set up a background image.

![](images/tiled_image.png)

```bash
python streamdeck_manager/samples/tiled_image.py
```

Entrypoint: `sdm-background`

### Menu widget

Run a Finite state machine with all buttons to navigate in several pages, the
FSM run iterations times (reset with back button).

![](images/menu.png)

```bash
python streamdeck_manager/samples/menu.py --iterations 2
```

Entrypoint: `sdm-menu`

### Navigation widget

Run a Finite state machine with all buttons to navigate in a folder path. It
shows folders and files with icon if provided in the asset path.

![](images/navigator.png)

```bash
python streamdeck_manager/samples/navigator.py --root-path $HOME
```

Entrypoint: `sdm-navigator`

## Credits

- vgonisanz
- streamdeck library base from `https://github.com/abcminiuser/python-elgato-streamdeck`
