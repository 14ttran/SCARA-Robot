# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 14:03:03 2018

@author: mecha13
"""
#import serial
from matplotlib import pyplot #for plotting things

#with serial.Serial('/dev/ttyACM0', 115200, timeout = 0.1) as ser_port:
afile = open('test.csv','r') #open the file in read mode
while True:
    line = afile.readline() #separate the lines in the code
    if line == '':
        print('End of file')
        break
    try: #see if the first two values in a line are valid numbers
        Value1 = float(line.split(',',1)[0])
        Value2 = float(line.split(',',2)[1])
        Value3 = float(line.split(',',3)[2])
        break
    except ValueError:
        pass
    except IndexError:
        pass