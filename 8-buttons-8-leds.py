import machine
import time
import bluetooth
from ble_uart import BLEUART
import time
import sh1106

#global variables
button_press_detected = False
bluetooth_press_detected = False
last_time  = time.ticks_ms()
interrupt_pin = ""


buttons = [1,1,1,1,1,1,1,1]
bluetooth_buttons = [1,1,1,1,1,1,1,1]

#pin interrupt handler
def button_handler(pin):
    new_time = time.ticks_ms()
    global last_time
    #debounce on interrupt level, only handle the first interrupt arriving
    if (new_time - last_time) > 30:
        #wait for bouncing to stop so the correct value can be read.
        time.sleep(0.01)
        last_time = new_time
        set_button_state(pin)
 

def set_button_state(button):
    global button_press_detected
    button_press_detected = True
    if(button == button1 or button == button2 or button == button3 or button == button4):
        print("normal button")
        if(button == button1):
            buttons[0] = button.value()
        if(button == button2):
            buttons[1] = button.value()
        if(button == button3):
            buttons[2] = button.value()
        if(button == button4):
            buttons[3] = button.value()
    else:
        print("pcf button")
        byte = i2c.readfrom(56, 1)
        i = int.from_bytes(byte, 'big') 
        bit_string = ('{:0>8}'.format(f"{i:b}"))
        print(bit_string)
        bit_string = "".join(reversed(bit_string))
        for x in range(4,8,):
            buttons[x] = int(bit_string[x])
        
    print(buttons)
    

#bluetooth rx interrupt  handler      
def bluetooth_rx_handler():
    bluetooth_message = uart.read().decode().strip()
    print("rx: ", bluetooth_message)
    set_bluetooth_button_state(bluetooth_message)
    
def set_bluetooth_button_state(bluetooth_message):
    bluetooth_message = bluetooth_message[0:3].split("/")
    bluetooth_buttons[int(bluetooth_message[0])] = int(bluetooth_message[1])
    global bluetooth_press_detected
    bluetooth_press_detected = True
    print(bluetooth_buttons)
    




#pcf8574
i2c = machine.I2C(0, scl=machine.Pin(23), sda=machine.Pin(22), freq=400000)
print(i2c.scan())
i2c.writeto(56, b'\xf0')
pcf_pin = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
pcf_pin.irq(trigger = machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler = button_handler)


#bluetooth
ble = bluetooth.BLE()
uart = BLEUART(ble, name="bas")    
uart.irq(handler=bluetooth_rx_handler)
bluetooth_message = ""

#leds
led5 = machine.Pin(15, machine.Pin.OUT)
led6 = machine.Pin(2, machine.Pin.OUT)
led7 = machine.Pin(4, machine.Pin.OUT)
led8 = machine.Pin(16, machine.Pin.OUT)
led5.value(0)
led6.value(0)
led7.value(0)
led8.value(0)

#buttons
button1 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button3 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button4 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
button1.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=button_handler)
button2.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=button_handler)
button3.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=button_handler)
button4.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=button_handler)



#create display
def write_to_display():
    display.fill(0)
    displayline1 = ""
    displayline2 = ""
    displayline3 = ""
    
    for x in range(0,8):
        displayline1 += str(buttons[x])
        displayline2 += str(bluetooth_buttons[x])
        displayline3 += str(buttons[x] & bluetooth_buttons[x])
    
    display.text(f"but: {str(displayline1)}", 0, 0)
    display.text(f"ble: {str(displayline2)}", 0, 10)
    display.text(f"res: {str(displayline3)}", 0, 20)
    display.show()


display = sh1106.SH1106_I2C(128, 64, i2c, machine.Pin(25), 0x3C, rotate=180)
display.sleep(False)
write_to_display()

# print_time = time.ticks_ms()

def print_pcf():
    byte = i2c.readfrom(56, 1)
    i = int.from_bytes(byte, 'big') 
    bit_string = ('{:0>8}'.format(f"{i:b}"))
    return bit_string

while True:
    write_value = 240    
    if button_press_detected or bluetooth_press_detected:
        print("button_press_detected")
        print("before_writing: ", print_pcf())
        #led 1
        if (buttons[0]  == 0 or bluetooth_buttons[0] == 0):
            write_value = write_value + 1          
        
        #led 2           
        if (buttons[1]  == 0 or bluetooth_buttons[1] == 0):
            write_value = write_value + 2
            
        #led 3   
        if (buttons[2]  == 0 or bluetooth_buttons[2] == 0):
            write_value = write_value + 4
        
        #led 4  
        if (buttons[3]  == 0 or bluetooth_buttons[3] == 0):
            write_value = write_value + 8
        
        if (buttons[4]  == 0 or bluetooth_buttons[4] == 0):
            led5.value(1)
        else:
            led5.value(0)
            
        if (buttons[5]  == 0 or bluetooth_buttons[5] == 0):
            led6.value(1)
        else:
            led6.value(0)
            
        if (buttons[6]  == 0 or bluetooth_buttons[6] == 0):
            led7.value(1)
        else:
            led7.value(0)
            
        if (buttons[7]  == 0 or bluetooth_buttons[7] == 0):
            led8.value(1)
        else:
            led8.value(0)
            
        i2c.writeto(56, write_value.to_bytes(2, 'big'))
        write_to_display()
        
        print("after writing: ", print_pcf())
        print("")
        button_press_detected = False
        bluetooth_press_detected = False
    
        

