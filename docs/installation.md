# How install O.S dependencies

## Install Usb dependencies

### Fedora 34

```bash
sudo dnf install -y hidapi-devel.x86_64
```

### Ubuntu 20.04

```bash
sudo apt install -y libhidapi-dev
```

## Add rules to USB

```bash
sudo tee /etc/udev/rules.d/10-streamdeck.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", TAG+="uaccess"
EOF
```

And reload udev rules to ensure the new permissions take effect. To check if the device is found you can run `lsusb` command.

### Fedora

```bash
sudo udevadm control --reload-rules
```

### Ubuntu

```bash
sudo /etc/init.d/udev restart
```

## Install the library

Create a tox environment following main `README.md`

## Test if works

Reconnect the Stream Deck if was connected and try to find it:

```bash
python streamdeck_manager/samples/device_info.py
```