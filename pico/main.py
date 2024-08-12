#George Perros
#pico coffee relay controller
#February 2024

import machine
import utime


led_blue = machine.Pin(6, machine.Pin.OUT)
led_green = machine.Pin(7, machine.Pin.OUT)
led_yellow = machine.Pin(8, machine.Pin.OUT)
led_red = machine.Pin(9, machine.Pin.OUT)
button_black_1 = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
button_black_2 = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
button_black_3 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button_red = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
relay1 = Pin(20, Pin.OUT)
relay2 = Pin(21, Pin.OUT)
button_state = 0
def int_handler(pin): #Interrupt statement closes the relayes and the rest of the leds, and then light the red LED
    button_red.irq(handler=None)
    utime.sleep(0.2)
    global button_state
    global cleanflag
    if (button_red.value() == 1) and (button_state == 0):
        button_state = 1
        logger("inters.txt")
        cleanflag = False
        led_red.value(1)
        led_yellow.value(0)
        led_blue.value(0)
        led_green.value(0)
        relay1.value(1)
        relay2       .value(1)
        print("Red")
        utime.sleep(3)
    elif (button_red.value() == 0) and (button_state == 1):
        button_state = 0
        utime.sleep(0.5)
        print("Int")
    button_red.irq(handler=int_handler)
    
def log_show(file):
    with open(file) as f:
        lines = f.read()
        return lines

def logger(file):
    lines = 0
    with open(file, "r") as f:
        lines = f.read()
        print(lines)
        lines = int(lines)
        lines = lines+1
        lines = str(lines)
    with open(file, "w") as f:
        f.write(lines)
        
button_red.irq(trigger=machine.Pin.IRQ_RISING, handler=int_handler)
prog_mode = 0
single_shot = 15
double_shot = 30
cleanflag = False
while True:
    #During the interrupt you press the single shot button (1) and it open the configuration menu
    #Pressing either single or double shot, you increment the seconds with single shot(Decrease) and double shot(Increase)
    #Pressing button 3 (Continuous) takes you back
    if button_state == 1 and button_black_1.value() == 0:
        prog_mode = 1
        logger("configs.txt")
        while True:
            led_blue.value(1)
            led_green.value(1)
            led_yellow.value(1)
            led_red.value(0)
            utime.sleep(0.5)
            led_blue.value(0)
            led_green.value(0)
            led_yellow.value(0)
            utime.sleep(0.5)
            if button_black_1.value() == 0:
                while True:
                    led_red.value(1)
                    led_blue.value(1)
                    utime.sleep(0.2)
                    led_red.value(0)
                    led_blue.value(0)
                    utime.sleep(0.2)
                    if button_black_1.value() == 0:
                        led_blue.value(1)
                        utime.sleep(0.2)
                        led_blue.value(0)
                        utime.sleep(0.2)
                        led_blue.value(1)
                        utime.sleep(0.2)
                        led_blue.value(0)
                        utime.sleep(1)
                        if single_shot > 2:
                            single_shot = single_shot - 1
                        else:
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                    elif button_black_2.value() == 0:
                        led_blue.value(1)
                        utime.sleep(1)
                        led_blue.value(0)
                        utime.sleep(1)
                        led_blue.value(1)
                        utime.sleep(0.2)
                        led_blue.value(0)
                        utime.sleep(1)
                        if double_shot < 60:
                            single_shot = single_shot + 1
                        else:
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                    elif button_black_3.value() == 0:
                        break
            if button_black_2.value() == 0:
                while True:
                    led_red.value(1)
                    led_green.value(1)
                    utime.sleep(0.2)
                    led_red.value(0)
                    led_green.value(0)
                    utime.sleep(0.2)
                    if button_black_1.value() == 0:
                        led_green.value(1)
                        utime.sleep(0.2)
                        led_green.value(0)
                        utime.sleep(0.2)
                        led_green.value(1)
                        utime.sleep(0.2)
                        led_green.value(0)
                        utime.sleep(1)
                        if double_shot > 2:
                            double_shot = double_shot - 1
                        else:
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                            
                    elif button_black_2.value() == 0:
                        led_green.value(1)
                        utime.sleep(1)
                        led_green.value(0)
                        utime.sleep(1)
                        led_green.value(1)
                        utime.sleep(0.2)
                        led_green.value(0)
                        utime.sleep(1)
                        if double_shot < 60:
                            double_shot = double_shot + 1
                        else:
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                            led_red.value(1)
                            utime.sleep(0.1)
                            led_red.value(0)
                            utime.sleep(0.1)
                    elif button_black_3.value() == 0:
                        break
            elif button_black_3.value() == 0:
                break
    #This is a cleaning processes using the blind in the group, brewing for 5 seconds and the stopping for another 5. The process is done 10 times
    if button_state == 1 and button_black_2.value() == 0:
        num = 0
        cleanflag = True
        led_red.value(0)
        logger("clean.txt")
        while (num <= 10) and cleanflag:
            num = num + 1
            relay1.value(0)
            relay2.value(0)
            led_yellow.value(0)
            led_blue.value(1)
            utime.sleep(5)
            led_blue.value(0)
            led_yellow.value(1)
            relay1.value(1)
            relay2.value(1)
            utime.sleep(5)
    if prog_mode == 1:
        utime.sleep(3)
        prog_mode = 0
    button_state = 0
    cleanflag = False
    if button_black_1.value() == 0:#Button for single shot espresso
        logger("single.txt")
        num = 0
        #This while loop is used for checking if the interrupt button has been pressed and in order to break out and not brew
        while num <= (single_shot - 1):
            num = num+1
            led_blue.value(1)
            print("On blue")
            relay1.value(0)
            relay2.value(0)
            utime.sleep(1)
            if button_state == 1:
                break
        
    elif button_black_2.value() == 0:#Button for double shot espresso
        num = 0
        logger("double.txt")
        #This while loop is used for checking if the interrupt button has been pressed and in order to break out and not brew
        while num <= (double_shot - 1):
            num = num+1
            led_green.value(1)
            print("On Green")
            relay1.value(0)
            relay2.value(0)
            utime.sleep(1)
            if button_state == 1:
                break
    elif button_black_3.value() == 0: #Button for Continuous brewing
        led_yellow.value(1)
        relay1.value(0)
        relay2.value(0)
        print("On Yellow")
        utime.sleep(0.1)
    else:
        led_blue.value(0)
        led_yellow.value(0)
        led_green.value(0)
        led_red.value(0)
        relay1.value(1)
        relay2.value(1)
        
    utime.sleep(0.20)
