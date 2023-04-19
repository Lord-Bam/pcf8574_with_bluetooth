import machine
import time
import sh1106
from machine import Pin, SPI


i2c = machine.I2C(scl=machine.Pin(23), sda=machine.Pin(22), freq=400000)
print(i2c.scan())
display = sh1106.SH1106_I2C(128, 64, i2c, machine.Pin(16), 0x3C, rotate=180)
display.sleep(False)


display.fill(0)
display.text(f'going to 0', 0, 0, 1)
display.show()


display.fill(0)
display.text("test1", 0, 0, 1)
display.text("test1", 0, 10, 1)
display.text("test1", 0, 20, 1)
display.text("test1", 0, 30, 1)
display.show()
