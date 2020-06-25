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

Px1=Px2=Px3=Px4= 0
Py1=Py2=Py3=Py4=nPy1=nPy2=nPy3=nPy4=90

th1 = 90
th2 = 90
t1=t2=t3=t4=t5=t6=t7=t8=90
la = 60
lb = 100
lc = 20

xorient=0
yorient=0 #variables for deciding orientation
jok=0.69
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

def calDis(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  
#print calculateDistance(x1, y1, x2, y2)

def orient(xorient,yorient,Py1,Py2,Py3,Py4):
    nPy1 = Py1-jok*(40-calDis(xorient,yorient,-30, 30))
    nPy2 = Py2-jok*(40-calDis(xorient,yorient, 30, 30))
    nPy3 = Py3-jok*(40-calDis(xorient,yorient,-30,-30))
    nPy4 = Py4-jok*(40-calDis(xorient,yorient, 30,-30))
    return nPy1,nPy2,nPy3,nPy4;
    
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
                Px1 = -0.3125*xpos+40
                Px4 = Px3 = Px2 = Px1
                nPy1,nPy2,nPy3,nPy4 = orient(xorient,yorient,Py1,Py2,Py3,Py4)
            
                #print(str(int(Px1)) +","+ str(int(Py1)))
            if event.code == 5:
                ypos = event.value
                Py1 = -0.3125*ypos+130
                Py4 = Py3 = Py2 = Py1
                nPy1,nPy2,nPy3,nPy4 = orient(xorient,yorient,Py1,Py2,Py3,Py4)
            
            if event.code == 0:
                xorient = (event.value-128)/3.2
                #print(str(int(xorient)) +","+ str(int(yorient)))
                nPy1,nPy2,nPy3,nPy4 = orient(xorient,yorient,Py1,Py2,Py3,Py4)
                
            if event.code == 1:
                yorient = -(event.value-128)/3.2
                #print(str(int(xorient)) +","+ str(int(yorient)))
                nPy1,nPy2,nPy3,nPy4 = orient(xorient,yorient,Py1,Py2,Py3,Py4)
            
            t1,t2 = invkin(Px1,nPy1)
            t3,t4 = invkin(Px2,nPy2)
            t5,t6 = invkin(Px3,nPy3)
            t7,t8 = invkin(Px4,nPy4)
            
            
            if event.code == 1 or 0 or 2 or 5:
                #print(str(int(Px1)) +","+ str(int(nPy1))+","+str(int(Px2)) +","+ str(int(nPy2))+","+str(int(Px3)) +","+ str(int(nPy3))+","+str(int(Px4)) +","+ str(int(nPy4))+"\n")
                #print(str(int(t1)) +","+ str(int(t2))+","+str(180-int(t3)) +","+ str(180-int(t4))+","+str(int(t5)) +","+ str(int(t6))+","+str(180-int(t7)) +","+ str(180-int(t8))+"\n")
                #print(str(int(xorient)) +","+ str(int(yorient)))
                ser.open()
                ser.write(bytes(str(int(t1)) +","+ str(int(t2))+","+str(int(t3)) +","+ str(int(t4))+","+str(int(t5)) +","+ str(int(t6))+","+str(int(t7)) +","+ str(int(t8))+"\n",'utf-8'))
                ser.close()
            
            #print(str(int(xorient)) +","+ str(int(yorient)))   
            #print(str(int(Px)) +","+ str(int(Py)))
            #th1,th4 = invkin(Px1,Py1)
            #print(str(th1) +","+ str(th4))
            #ser.open()
            #ser.write(bytes(str(th1) +","+ str(th4)+"\n",'utf-8'))
            #ser.close()
            
