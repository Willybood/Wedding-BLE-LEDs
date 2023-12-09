from ubluetooth import BLE
import plasma
from plasma import plasma_stick
from math import sin
from bleRemoteScanner import startScanningForRemotes, getCurrentLedPatternGroup, getCurrentLedSubPattern
from bleBottleTransmitter import BLERemoteTransmitter
from ledController import setupLeds, playLedPattern

BLE_NAME = "wedBot"
BLE_INTERVAL_MS = 250

bt = BLE()
bleTransmitter = BLERemoteTransmitter(bt, BLE_NAME, BLE_INTERVAL_MS)

if __name__ == "__main__":
    startScanningForRemotes(bt, bleTransmitter)
    currentlyPlayingPattern = 0
    setupLeds()
    while True:
        playLedPattern(getCurrentLedPatternGroup(), getCurrentLedSubPattern())