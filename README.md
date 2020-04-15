# Unlock SESAME Smart Lock by NFC Tag

Confirmed on:

- Raspberry Pi
- Sony RC-S380
- NFC Type3 (FeliCa／FeliCa Lite-S)
  - Suica
  - PASMO
  - Apple Pay

## Deploy

### Raspberry Pi

- Install Raspbian via `dd`
- ssh
- Wi-Fi
- `ssh-copy-id`
- `useradd foobar`
- `userdel pi`
- `raspi-config —expand-rootfs`

At this point, you can test if USB device works well.

```bash
$ lsusb
Bus 001 Device 002: ID 054c:06c3 Sony Corp. RC-S380
```

### Runtime

- Use Preinstalled Python 3.7
  - Don’t bother
- Install Pip
  - `sudo apt-get -y install python3-pip`
- Install Poetry
  - `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3`

### Application

- `sudo apt-get install git`
- Create Deploy Key
  - `ssh-keygen -t ed25519 -C 'Github Deploy key' -f id_rsa`
- Register to GitHub Repository
- `git clone git@github.com:shrkw/unlock_sesame_by_nfc.git`
- `cd unlock_sesame_by_nfc`
- `python3 -m venv .venv && ~/.poetry/bin/poetry install --no-dev`

### Allow USB Device

USB Device allows just for root user. So you need a few steps to permit for normal users.

```bash
$ ~/.poetry/bin/poetry run python -m nfc
This is the 1.0.3 version of nfcpy run in Python 3.7.3
on Linux-4.19.97+-armv6l-with-debian-10.2
I'm now searching your system for contactless devices
** found usb:054c:06c3 at usb:001:002 but access is denied
-- the device is owned by 'root' but you are ‘foobar’
-- also members of the 'root' group would be permitted
-- you could use 'sudo' but this is not recommended
-- better assign the device to the 'plugdev' group
   sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"054c\", ATTRS{idProduct}==\"06c3\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'
   sudo udevadm control -R # then re-attach device
I'm not trying serial devices because you haven't told me
-- add the option '--search-tty' to have me looking
-- but beware that this may break other serial devs
Sorry, but I couldn't find any contactless device
```

Follow the above instructions.

## Run

Required env vars:

```bash
SESAME_DEVICE_UUID
SESAME_APIKEY
```

So, you can run as following:
`SESAME_DEVICE_UUID=aaaa SESAME_APIKEY=xxxx ~/.poetry/bin/poetry run python main.py`

## Supervisord

You can use `conf/supervisor/unlock_sesame_by_nfc.conf`.

```bash
sudo apt-get install supervisor
sudo nano /etc/supervisor/conf.d/unlock_sesame_by_nfc.conf
```
