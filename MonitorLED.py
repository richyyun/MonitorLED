import PIL.ImageGrab
import time
import serial
import atexit
from statistics import mean

## For turning off LEDs and closing the serial connection
def closeserial(s,w,h):
    s.write(bytes((w*2+h*2)*3*2))
    s.close()

## Connect to arduino
arduino = serial.Serial('COM3',115200,timeout = 0.1)

time.sleep(1) ## Just to make sure connection has occured

## Number of LEDs
width = 33;
height = 19;
depth = 100;

## Call closeserial at exit
atexit.register(closeserial,'arduino','width','height')

size = [1920,1080];

temp = list(range(1,width+1));
horz = [round(size[0]/x) for x in temp];
temp = list(range(1,height+1));
vert = [round(size[1]/x) for x in temp];

## Flag from arduino for data transfer
flag = [];
while  True:
    flag = arduino.read();
    if flag:

        ## Capture screen 
        im = PIL.ImageGrab.grab();

        ## Resample     
        small = im.resize((width,height),PIL.Image.HAMMING)
        small = list(small.getdata())
        
        ## Top
        for w in range(width):
            arduino.write(bytes(small[w]))
            
        ## Right
        for h in range(height):
            arduino.write(bytes(small[width*(h+1)-1]))

        ## Bottom
        for w in range(width):
            arduino.write(bytes(small[width*(height)-1-w]))

        ## Left
        for h in range(height):
            arduino.write(bytes(small[width*(height-h-1)]))

        # Reset data request flag
        flag = []

