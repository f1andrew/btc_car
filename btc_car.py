#!/usr/bin/python3
import time
import threading
from evdev import InputDevice, categorize, ecodes #remote
import RPi.GPIO as GPIO
from btwrapper import Bluetoothctl
from config import *

#remote
print("ready")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
in1=23
in2=24
in3=7
in4=8
lp=12
rp=18
led=4

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(lp,GPIO.OUT)
GPIO.setup(rp,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,GPIO.LOW)

p1 = GPIO.PWM(lp, motor_speed)  # motor_speed can be changed in config.py
p1.start(50)
p2 = GPIO.PWM(rp, motor_speed)
p2.start(50)

f=True
def blinking(time_b):
    global f
    print("Thread starting")
    if time_b:
        while f:
            GPIO.output(led,GPIO.HIGH)
            time.sleep(time_b)
            GPIO.output(led,GPIO.LOW)
            time.sleep(time_b)
    else:
        GPIO.output(led,GPIO.HIGH)
        while f:
            pass
    print("Thread finishing")

x = threading.Thread(target=blinking,args=(1,))
x.start()

print("Init bluetooth...")
try:
    bl = Bluetoothctl()
    bl.power_on()
    bl.agent_on() 
    bl.default_agent()
    bl.pair(dev_addr)
    bl.connect(dev_addr)
    print('Connect')

    #creates object 'gamepad' to store the data
    gamepad = InputDevice('/dev/input/event0')
    #loop and filter by event code and print the mapped label
    print('Ready')
    f=False
    x.join()
    f=True
    x = threading.Thread(target=blinking,args=(0,))
    x.start()
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            print(event.code)
            if event.value == 1:
                print(event.code)
                if event.code == 30:
                    print("forward")
                    GPIO.output(in2,GPIO.HIGH)
                    GPIO.output(in4,GPIO.HIGH)
                elif event.code == 16:
                    print("stop")
                    GPIO.output(in2,GPIO.LOW)
                    GPIO.output(in4,GPIO.LOW)
                elif event.code == 32:
                    print("backward")
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in3,GPIO.HIGH)
                elif event.code == 46:
                    print("stop")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in3,GPIO.LOW)
                elif event.code == 17:
                    print("right")
                    GPIO.output(in1,GPIO.HIGH)
                    GPIO.output(in4,GPIO.HIGH)
                elif event.code == 18:
                    print("stop")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in4,GPIO.LOW)
                elif event.code == 45:
                    print("right")
                    GPIO.output(in2,GPIO.HIGH)
                    GPIO.output(in3,GPIO.HIGH)
                elif event.code == 44:
                    print("stop")
                    GPIO.output(in2,GPIO.LOW)
                    GPIO.output(in3,GPIO.LOW)
except:
    f=False
    x.join()
    GPIO.cleanup()
