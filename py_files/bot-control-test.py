#import evdev
from evdev import InputDevice, categorize, ecodes
import serial
import math

ser = serial.Serial('/dev/ttyUSB0',115200)  # open serial port
print(ser.name)

ser.write(b'start')     # write a string
ser.close()
#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

#button code variables (change to suit your device)
aBtn = 304
bBtn = 305
xBtn = 307
yBtn = 308

up = 17
down = 17
left = 16
right = 16

start = 315
select = 314

lTrig = 310
rTrig = 311

xpos = 128
ypos = 128

Px = 0
Py = 90

th1 = 90
th2 = 90

la = 60
lb = 100
lc = 20

xorient=128
yorient=128 #variables for deciding orientation

#prints out device info at start
print(gamepad)

def invkin(Px,Py):
    Px = Px+10
    E1 = -2*la*Px
    F1 = -2*la*Py
    G1 = la*la - lb*lb + Px*Px + Py*Py
    theta1 = math.degrees(2*math.atan((-F1 + math.sqrt(E1*E1 + F1*F1 - G1*G1))/(G1-E1)))
    if theta1>0:
        th1 = theta1-90
    else:
        th1 = theta1+270
    E4 = 2*la*(-Px+lc)
    F4 = -2*la*Py
    G4 = lc*lc + la*la - lb*lb + Px*Px + Py*Py - 2*lc*Px
    theta4 = math.degrees(2*math.atan((-F4 - math.sqrt(E4*E4 + F4*F4 - G4*G4))/(G4-E4)))
    th4 = theta4+90
    return int(th1),int(th4);

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == yBtn:
                ser.open()
                ser.write(b'Y')     # write a string
                ser.close()
            elif event.code == bBtn:
                print("B")
            elif event.code == aBtn:
                print("A")
            elif event.code == xBtn:
                print("X")
                
            elif event.code == start:
                print("start")
            elif event.code == select:
                print("select")

            elif event.code == lTrig:
                print("left bumper")
            elif event.code == rTrig:
                print("right bumper")
                
    # for ABS events, analog keys and d-pad
            
    elif event.type == ecodes.EV_ABS:
        if event.value == 1 and event.code == down:
            print("down")
        elif event.value == 1 and event.code == right:
            print("right")
        
        elif event.value == -1:
            if event.code == up:
                print("up")
            elif event.code == left:
                print("left")
        elif event.value!= 0:
            #print(str(event.code) +","+ str(event.value))
            if event.code == 2:
                xpos = event.value
                Px = -0.3125*xpos+40 
            if event.code == 5:
                ypos = event.value
                Py = -0.3125*ypos+130
                
            if event.code == 0:
                xorient = (event.value-128)/40
            if event.code == 1:
                yorient = (event.value-128)/40
                
            #print(str(int(Px)) +","+ str(int(Py)))
            th1,th4 = invkin(Px,Py)
            #print(str(th1) +","+ str(th4))
            ser.open()
            ser.write(bytes(str(th1) +","+ str(th4)+"\n",'utf-8'))
            ser.close()
            
