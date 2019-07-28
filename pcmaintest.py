# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 14:03:03 2018

@author: mecha13
"""
import serial
#import time
from matplotlib import pyplot #for plotting things

with serial.Serial('/dev/ttyACM0', 115200, timeout = 0.1) as ser_port:
    while True:
        input()
        ser_port.write(b'\r\n')
        gain = input('Gainz?\n')
        ser_port.write(bytes(gain, 'UTF-8') + (b'\r'))
        
        setpoint = input('Where?\n')
        ser_port.write(bytes(setpoint, 'UTF-8') + (b'\r'))
        
        runtime = input('For how long?\n')
        ser_port.write(bytes(runtime, 'UTF-8') + (b'\r'))
        
        
        lines = []
        trigger = 0
        #time.sleep(1)        

        
        while True:
            line = ser_port.readline()
            #print(line)
            if line != (b'1\r\n'):
                lines.append(line)
            if line == (b'1\r\n'):
                #print('eureka')
                break
        

        Column1 = [] #initialize lists
        Column2 = []
        for x in lines: 
            try: #see if the first two values in a line are valid numbers
                Value1 = float(x.decode('UTF-8').split(',',1)[0])
                Value2 = float(x.decode('UTF-8').split(',',2)[1])
            except ValueError:
                pass
            except IndexError:
                pass
            else: #append to list
                Column1 += [Value1]
                Column2 += [Value2]
        
        # plot things
        pyplot.plot(Column1,Column2)
        pyplot.xlabel('Time (ms)')
        pyplot.ylabel('Position')
        pyplot.show()
    #while True:
#        #action = input('What the f*ck do you want b*thc?\n')
#        #if str(action) == 'Run step response':
#        try:        
##            gain = input('Gainz?\n')
##            ser_port.write(bytes(gain, 'UTF-8') + (b'\r'))
##            
##            setpoint = input('Where?\n')
##            ser_port.write(bytes(setpoint, 'UTF-8') + (b'\r'))
##            
##            runtime = input('For how long?\n')
##            ser_port.write(bytes(runtime, 'UTF-8') + (b'\r'))
##
##            time.sleep((int(runtime) + 5000)/1000)
##            
#            x = ser_port.readlines()
#            for line in x:      
#                print(line.decode('UTF-8'))
#        except KeyboardInterrupt:
#            pass