import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload

from micropython import const

_UNIQUE_UUID_FOR_REMOTES = "49fe"
_TTL_FOR_AD = 5 # Countdown for the number of bounces for the message before it's discarded

class BLERemoteTransmitter:
    def __init__(self, ble, name="mpy-uart", interval_ms = 500):
        self._ble = ble
        self._ble.active(True)
        self._connections = set()
        self._write_callback = None
        self._ad_interval_ms = interval_ms
        self._ad_name = name

    def advertise(self, selected_button_x, selected_button_y):
        print("Starting advertising")
        uuids_to_advertise = [bluetooth.UUID(_UNIQUE_UUID_FOR_REMOTES), # Unique ID
              bluetooth.UUID(selected_button_x), # x axis of selected button
              bluetooth.UUID(selected_button_y), # y axis of selected button
              bluetooth.UUID(_TTL_FOR_AD)] # TTL for message
        self._payload = advertising_payload(name=self._ad_name, services=uuids_to_advertise)
        self._ble.gap_advertise(self._ad_interval_ms * 1000, adv_data=self._payload)
