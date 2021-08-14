# Streamdeck speed of light

This is a proof of concept to make a game using the elgato Stream Deck.

Stream deck model used have 3x5 buttons with 72x72 pixels of resolution each one.

## Installation

```bash
sudo dnf install -y hidapi-devel.x86_64
```

```bash
sudo tee /etc/udev/rules.d/10-streamdeck.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", TAG+="uaccess"
EOF
```

And reload udev rules to ensure the new permissions take effect

```bash
sudo udevadm control --reload-rules
```

```bash
pip install streamdeck_manager
```

Reconnect the Stream Deck if was connected and try to find it:

*TODO* Check with installable

```bash
streamdeck_manager-info
```

## Development

Follow installation instruction and instead install streamdeck_manager:

```bash
make env-create                                 # Only first time
source .tox/streamdeck_manager/bin/activate     # All bash session
```

## Samples

In a development bash, use `--help` to customize parameters:

```bash
python streamdeck_manager/samples/device_info.py
python streamdeck_manager/samples/basic_usage.py
python streamdeck_manager/samples/buttons_types.py
python streamdeck_manager/samples/tiled_image.py
```

## Credits

- vgonisanz
- streamdeck library base from `https://github.com/abcminiuser/python-elgato-streamdeck`
