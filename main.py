# This example demonstrates a peripheral implementing the Nordic UART Service (NUS).
# Test met https://play.google.com/store/apps/details?id=com.mightyit.gops.bleterminal&hl=nl&gl=US
# Test IOS met https://apps.apple.com/us/app/nrf-connect-for-mobile/id1054362403

import bluetooth

from ble_uart import BLEUART

print("Start BLE demo on ESP32")

def demo():
    import time

    ble = bluetooth.BLE()
    uart = BLEUART(ble)

    def on_rx():
        print(uart.read())
        print("rx: ", uart.read().decode().strip())

    uart.irq(handler=on_rx)
    nums = [4, 8, 15, 16, 23, 42]
    i = 0

    try:
        while True:
            uart.write(str(nums[i]) + "\n")
            i = (i + 1) % len(nums)
            time.sleep_ms(1000)
    except KeyboardInterrupt:
        pass

    uart.close()


if __name__ == "__main__":
    demo()
