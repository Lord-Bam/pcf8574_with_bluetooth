import machine
import time 

button_press_detected = False
last_time  = time.ticks_ms()


def handle_interrupt(pin):
    new_time = time.ticks_ms()
    global last_time
    print(pin)
    #only handle the first interrupt arriving
    if (new_time - last_time) > 30:
        #wait for bouncing to stop so the correct value can be read.
        time.sleep(0.01)
        last_time = new_time
        global button_press_detected
        button_press_detected = True
        global interrupt_pin
        interrupt_pin = pin


#pcf8574
i2c = machine.I2C(0, scl=machine.Pin(23), sda=machine.Pin(22), freq=400000)
i2c.writeto(56, b'\xf0')
pcf_pin = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
pcf_pin.irq(trigger = machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler = handle_interrupt)
print(i2c.scan())


#leds
led1 = machine.Pin(15, machine.Pin.OUT)
led2 = machine.Pin(2, machine.Pin.OUT)
led3 = machine.Pin(4, machine.Pin.OUT)
led4 = machine.Pin(16, machine.Pin.OUT)

#buttons
button1 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button3 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button4 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
button1.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=handle_interrupt)
button2.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=handle_interrupt)
button3.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=handle_interrupt)
button4.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=handle_interrupt)

led1.value(0)
led2.value(0)
led3.value(0)
led4.value(0)
print_time = time.ticks_ms()
while True:

    new_time = time.ticks_ms()
    if (new_time - print_time) > 2000:
        print_time = new_time
        byte = i2c.readfrom(56, 1)
        i = int.from_bytes(byte, 'big') 
        bit_string = ('{:0>8}'.format(f"{i:b}"))
        print(bit_string)
    
    if button_press_detected:
        print("button_press_detected")
        
        if (interrupt_pin == button1 and button1.value() == 0):
            print("button1 on")
            byte = i2c.readfrom(56, 1)
            byte = byte[0] | 1
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            
        if (interrupt_pin == button1 and button1.value() == 1):
            print("button1 off")
            byte = i2c.readfrom(56, 1)
            byte = byte[0] ^ 1
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            
        if (interrupt_pin == button2 and button2.value() == 0):
            print("button2 on")
            byte = i2c.readfrom(56, 1)
            byte = byte[0] | 2
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            
        if (interrupt_pin == button2 and button2.value() == 1):
            print("button2 off")
            byte = i2c.readfrom(56, 1)
            byte = byte[0] ^ 2
            i2c.writeto(56, byte.to_bytes(2, 'big'))
            
            
        elif (interrupt_pin == button3 and button3.value() == 0):
            print("button3")
        elif (interrupt_pin == button4 and button4.value() == 0):
            print("button4")
            
            
        elif (interrupt_pin == pcf_pin):
            byte = i2c.readfrom(56, 1)
            i = int.from_bytes(byte, 'big') 
            bit_string = ('{:0>8}'.format(f"{i:b}"))
            print(bit_string)
            
            
            button_value = byte[0] >> 4
            
            if ((byte[0] >> 7 ) & 1 == 0):
                print("button 5")
                led1.value(1)
            if ((byte[0] >> 7 ) & 1 == 1):
                print("button 5")
                led1.value(0)
                
            if ((byte[0] >> 6 ) & 1 == 0):
                print("button 6")
                led2.value(1)
            if ((byte[0] >> 6 ) & 1 == 1):
                print("button 6")
                led2.value(0)
                
            if ((byte[0] >> 5 ) & 1 == 0):
                print("button 7")
                led3.value(1)
            if ((byte[0] >> 5 ) & 1 == 1):
                print("button 7")
                led3.value(0)
                
            if ((byte[0] >> 4 ) & 1 == 0):
                print("button 8")
                led4.value(1)
            if ((byte[0] >> 4 ) & 1 == 1):
                print("button 8")
                led4.value(0)
                
                
        print("")
        button_press_detected = False
    
        

