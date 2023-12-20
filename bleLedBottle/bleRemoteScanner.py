from ubluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
from micropython import const
from ble_advertising import decode_remote_services, decode_name
from bleBottleTransmitter import BLERemoteTransmitter

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_IRQ_SCAN_RESULT   = const(5)
_IRQ_SCAN_COMPLETE = const(6)

_REMOTE_BLE_NAME = "wedRem"
_BOTTLE_BLE_NAME = "wedBot"

deviceFound = False
uuidList = []
largestDetectedTTL = 0
bt = None
bleTransmitter = None

currentLedPatternGroup = 0
currentLedSubPattern = 0

def getCurrentLedPatternGroup():
    return currentLedPatternGroup

def getCurrentLedSubPattern():
    return currentLedSubPattern

def bt_irq(event, data):
    global largestDetectedTTL
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        if adv_type in (_ADV_IND, _ADV_DIRECT_IND):
            if((decode_name(adv_data) == _REMOTE_BLE_NAME) or (decode_name(adv_data) == _BOTTLE_BLE_NAME)):
                global uuidList
                global deviceFound
                newlyFoundDeviceUuidList = decode_remote_services(adv_data)
                if(newlyFoundDeviceUuidList[2] >= largestDetectedTTL):
                    global currentLedPatternGroup
                    global currentLedSubPattern
                    uuidList = newlyFoundDeviceUuidList
                    deviceFound = True
                    largestDetectedTTL = newlyFoundDeviceUuidList[2]
                    bleTransmitter.advertise(uuidList[0], uuidList[1], uuidList[2])
                    currentLedPatternGroup = uuidList[1]
                    currentLedSubPattern = uuidList[0]
    elif event == _IRQ_SCAN_COMPLETE:
        # Scan duration finished or manually stopped.
        if(not deviceFound):
            largestDetectedTTL -= 1
            if(largestDetectedTTL < 0):
                largestDetectedTTL = 0
            if(len(uuidList) > 0): # If a device was previously found
                bleTransmitter.advertise(uuidList[0], uuidList[1], largestDetectedTTL) # Degrade the TTL to prevent an old message taking priority
        deviceFound = False
        bt.gap_scan(1000, 30000, 30000)

def startScanningForRemotes(callingBt, callingBleTransmitter):
    global bt
    bt = callingBt
    global bleTransmitter
    bleTransmitter = callingBleTransmitter
    bt.irq(bt_irq)
    bt.active(True)
    bt.gap_scan(1000, 30000, 30000)

if __name__ == "__main__":
    tempBt = BLE()
    startScanningForRemotes(tempBt)