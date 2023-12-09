from ubluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
from micropython import const
from time import sleep
from ble_advertising import decode_remote_services, decode_name

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_IRQ_SCAN_RESULT   = const(5)
_IRQ_SCAN_COMPLETE = const(6)

_REMOTE_BLE_NAME = "wedRem"

deviceFound = False
uuidList = []
bt = None

def bt_irq(event, data):
    if event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        if adv_type in (_ADV_IND, _ADV_DIRECT_IND):
            if(decode_name(adv_data) == _REMOTE_BLE_NAME):
                global uuidList
                uuidList = decode_remote_services(adv_data)
                global deviceFound
                deviceFound = True
    elif event == _IRQ_SCAN_COMPLETE:
        # Scan duration finished or manually stopped.
        if(deviceFound):
            print("Device found")
            print(uuidList)
        else:
            print("No device detected")
        deviceFound = False
        bt.gap_scan(1000, 30000, 30000)

def startScanningForRemotes(callingBt):
    global bt
    bt = callingBt
    bt.irq(bt_irq)
    bt.active(True)
    bt.gap_scan(1000, 30000, 30000)

if __name__ == "__main__":
    tempBt = BLE()
    startScanningForRemotes(tempBt)