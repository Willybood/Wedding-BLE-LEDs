from ubluetooth import BLE
import plasma
from plasma import plasma_stick
from math import sin
from bleRemoteScanner import startScanningForRemotes, getCurrentLedPatternGroup, getCurrentLedSubPattern, setCurrentLedPatternGroup, setCurrentLedSubPattern
from bleBottleTransmitter import BLERemoteTransmitter
from ledController import setupLeds, playLedPattern

BLE_NAME = "wedBot"
BLE_INTERVAL_MS = 250

bt = BLE()
bleTransmitter = BLERemoteTransmitter(bt, BLE_NAME, BLE_INTERVAL_MS)

if __name__ == "__main__":
    # Set the default LED pattern
    setCurrentLedPatternGroup(2)
    setCurrentLedSubPattern(2)
    
    startScanningForRemotes(bt, bleTransmitter)
    bleTransmitter.advertise(getCurrentLedPatternGroup(), getCurrentLedSubPattern(), 0)
    setupLeds()
    while True:
        playLedPattern(getCurrentLedPatternGroup(), getCurrentLedSubPattern())