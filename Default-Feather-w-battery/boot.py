# SPDX-FileCopyrightText: 2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
CircuitPython Essentials Storage CP Filesystem boot.py file
"""
import board
import digitalio
import storage

button = digitalio.DigitalInOut(board.D4)
button.switch_to_input(pull=digitalio.Pull.UP)

# If the OBJECT_NAME is connected to ground, the filesystem is writable by CircuitPython
storage.remount("/", readonly=button.value)
