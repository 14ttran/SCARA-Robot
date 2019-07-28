# -*- coding: utf-8 -*-
#
## @privatesection - Stuff in this file doesn't need to be Doxygen-ed
#
#  @author jr

import pyb
import micropython
import gc

import cotask
import task_share
import print_task

#motor imports
#import utime
import motordriver
import encoder
import pcontroller
#import loadfile
import md3
# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)


GOING = micropython.const (0)
PRINT = micropython.const (1)
INPUT = micropython.const (2)
WAIT  = micropython.const (3)

y = micropython.const (4)
r = micropython.const (5)
b = micropython.const (6)

def Overlord ():
    #name of state for Overlord task
    Overlords = 0
    global mdone1
    global mdone2
    global mdone3
    global NEWVAL1
    global NEWVAL2
    global NEWVAL3
    while True:
        #State 0: Initialization state. Reads file and stores xyz coordinate 
        #profile. Converts coordinates to link angles then encoder ticks        
        if Overlords == 0:
            #counter to increment motor tick command lists. Starts at 1 becasue we start at state 2
            mcount = 1
            #Counter keeping track of when more paint is needed
            pcount = 0
            #Counter to increment more paint command list
            ccount = 0
            #Counter to increment wash brush command list
            #Calibrated value when more paint needed
            MORESAUCE = 100
            #Variable to select color
            Color_Select = 0
            #Done flag for get more paint state
            SAUCED = 0
            #NEW Value flag
            NEWVAL1 = 0
            NEWVAL2 = 0
            NEWVAL3 = 0
            #Motor done flags
            mdone1 = 0
            mdone2 = 0
            mdone3 = 0
            WASHED = 0
            #flag to say file has been laoded
            loaded = 0
            FIRSTLOOP = 1
            lift_height = -11675
            paint_height = 11000
            dip_height = 12413
            first5 = 1
            sm1.put(0,False)
            sm2.put(0,False)
            painting = 0
            switch = 0
            
            
            #use user input to define filename and res
            filename = input('Enter Profile file name \n')
#            res = float(input('Enter Profile resolution\n'))
            Color = input('Enter color (y,b,r) \n')            
#            load = loadfile.Loadfile(filename)
#            m1,m2,m3 = load.normal()
            
            Overlords = float(input('Move to starting position. Enter a 2 to begin \n'))
        #State 1:Read lists containing motor position commands and send each point to 
        #respective motor controller tasks
        elif Overlords == 1:
            if FIRSTLOOP == 1:
                afile = open(filename,'r') #open the file in read mode
                FIRSTLOOP = 0

            while (mdone1 and mdone2 and mdone3):
                line = afile.readline() #read an individual line
                if line == '': #check if reached end of file
                    Overlords = 3 #transition to done state
                    FIRSTLOOP = 1 #raise DONE flag
                    afile.close() #close the file
                    break #break from the loop
                elif pcount == MORESAUCE:
                    Overlords = 2
                    Color_Select = 0
                    pcount = 0
                    mdone1 = 0
                    mdone2 = 0
                    mdone3 = 0
                    break
                try: #see if the first two values in a line are valid numbers
                #profile hpgl version
                    Value1 = (-float(line.split(',')[1]))
                    Value2 = (float(line.split(',')[2]))
                    Value3 = int(line.split(',')[0])
                #manual test input
#                     Value1 = (-float(line.split(',')[0]))
#                     Value2 = (float(line.split(',')[1]))
#                     Value3 = int(line.split(',')[2])
                
                except ValueError:
                    pass
                except IndexError:
                    pass
                else:
                    if Value3 == 1:
                        Overlords = 5
                        first5 = 1
                        painting = 1
                        
                        break
                    elif Value2*sm2.get(False) < 0:
                        Overlords = 5
                        switch = 1
                        first5 = 1
                        mdone1 = 0
                        mdone2 = 0
                        mdone3 = 0
                    else:
                        if Value3 == 0:
                            Value3 = paint_height
#                        elif Value3 == 1:
#                            Value3 = lift_height
                        sm1.put(Value1,False)
                        sm2.put(Value2,False)
                        sm3.put(Value3,False)
                        NEWVAL1 = 1
                        NEWVAL2 = 1
                        NEWVAL3 = 1
                        mdone1 = 0
                        mdone2 = 0
                        mdone3 = 0
                        pcount +=1

#            print(mcount)


        #State 2: Get more paint state    
        elif Overlords == 2:
        #Load file for get more paint routine, based on the selected color
            if Color_Select == 0:
                if Color == 'y':
                    cfile = open('yellow.csv','r') #open the file in read mode
                    Overlords = 5
                    paint = 1
                    mdone1 = 0
                    mdone2 = 0
                    mdone3 = 0
                elif Color == 'r':
                    cfile = open('red.csv','r') #open the file in read mode
                    Overlords = 5
                    paint = 1
                    mdone1 = 0
                    mdone2 = 0
                    mdone3 = 0
                elif Color == 'b':
                    cfile = open('blue.csv','r') #open the file in read mode
                    Overlords = 5
                    paint = 1
                    mdone1 = 0
                    mdone2 = 0
                    mdone3 = 0
                Color_Select = 1

            while (mdone1 and mdone2 and mdone3):
                line = cfile.readline() #read an individual line
                if line == '': #check if reached end of file
                    Overlords = 1 #transition to wash state
                    pcount = 0
                    cfile.close() #close the file
                    mdone1 = 1
                    mdone2 = 1
                    mdone3 = 1
                    break #break from the loop
                try: #see if the first two values in a line are valid numbers
                    Value1 = int(line.split(',')[0])
                    Value2 = int(line.split(',')[1])
                    Value3 = int(line.split(',')[2])
                except ValueError:
                    pass
                except IndexError:
                    pass
                else:
                    sm1.put(Value1,False)
                    sm2.put(Value2,False)
                    sm3.put(Value3,False)
                    NEWVAL1 = 1
                    NEWVAL2 = 1
                    NEWVAL3 = 1
                    mdone1 = 0
                    mdone2 = 0
                    mdone3 = 0
                
#            print(ccount)
            
        #State 3: Done printing state    
        elif Overlords == 3:
            if FIRSTLOOP == 1:
#                afile = open('done.csv','r') #open the file in read mode
                sm3.put(0,False)
                mdone1 = mdone2 =mdone3 = 0
                NEWVAL1 = 1
                NEWVAL2 = 1
                NEWVAL3 = 1
                FIRSTLOOP = 0
                DONE = 0

            while (mdone1 and mdone2 and mdone3):
                Overlords = -1
#                line = afile.readline() #read an individual line
#                if line == '': #check if reached end of file
#                    Overlords = -1 #transition to dummy state state
#                    afile.close() #close the file
#                    break #break from the loop
#                try: #see if the first two values in a line are valid numbers
#                    Value1 = float(line.split(',')[0])
#                    Value2 = float(line.split(',')[1])
#                    Value3 = float(line.split(',')[2])
#                except ValueError:
#                    pass
#                except IndexError:
#                    pass
#                else:
#                    sm1.put(Value1,False)
#                    sm2.put(Value2,False)
#                    sm3.put(Value3,False)
#                    NEWVAL1 = 1
#                    NEWVAL2 = 1
#                    NEWVAL3 = 1
#                    mdone1 = 0
#                    mdone2 = 0
#                    mdone3 = 0
                
#            print(mcount)
            
        #State 4: Wash brush state
#        elif Overlords == 4:
#            if loaded == 0:
#                afile = open('wash.csv','r') #open the file in read mode
#                loaded = 1
#                
#            while (mdone1 and mdone2 and mdone3):
#                line = afile.readline() #read an individual line
#                if line == '': #check if reached end of file
#                    FIRSTLOOP = 1                 
#                    Overlords = 3 #transition to wash state
#                    afile.close() #close the file
#                    break #break from the loop    
#                try: #see if the first two values in a line are valid numbers
#                    Value1 = float(line.split(',',1)[0])
#                    Value2 = float(line.split(',',2)[1])
#                    Value3 = float(line.split(',',3)[2])
#                except ValueError:
#                    pass
#                except IndexError:
#                    pass
#                else:
#                    if Value3 == 0:
#                        Value3 = paint_height
#                    elif Value3 == 1:
#                        Value3 = lift_height
#                        
#                    sm1.put(Value1,False)
#                    sm2.put(Value2,False)
#                    sm3.put(Value3,False)
#                    NEWVAL1 = 1
#                    NEWVAL2 = 1
#                    NEWVAL3 = 1
#                    mdone1 = 0
#                    mdone2 = 0
#                    mdone3 = 0
        #power lifitng state
        elif Overlords == 5:
            if first5 == 1:
                first5 = 0
                sm3.put(lift_height,False)
                mdone1 = 0
                mdone2 = 0
                mdone3 = 0
                NEWVAL1 = 1
                NEWVAL2 = 1
                NEWVAL3 = 1
            elif (mdone1 and mdone2 and mdone3):
                if paint == 1:
                    Overlords = 2
                    first5 = 1
                    paint = 0
                    mdone1 = 1
                    mdone2 = 1
                    mdone3 = 1
                elif switch ==1:
                    switch = 2
                    sm1.put(Value1,False)
                    sm2.put(Value2,False)
                    NEWVAL1 = 1
                    NEWVAL2 = 1
                    NEWVAL3 = 1
                    mdone1 = 0
                    mdone2 = 0
                    mdone3 = 0
                elif switch == 2:
                    sm1.put(Value1,False)
                    sm2.put(Value2,False)
                    sm3.put(paint_height,False)
                    NEWVAL1 = 1
                    NEWVAL2 = 1
                    NEWVAL3 = 1
                    mdone1 = 0
                    mdone2 = 0
                    mdone3 = 0
                    Overlords = 1
                    first5 = 1
                    switch = 0
                elif painting == 1:
                    Overlords = 1
                    first5 = 1
                    mdone1 = 1
                    mdone2 = 1
                    mdone3 = 1
        print(Overlords)
        yield (Overlords)        
        
def Control1 ():
    ''' Proportional Control of Motor 1, which controls the first link  '''

    Controls = INPUT #Change state to INPUT
    counter = 0
    cont_count = 0
    global mdone1
    global mdone2
    global mdone3
    global NEWVAL1
    #motor initialize stuff
    ###change to new motors
    motorvoltage = 12
    md = motordriver.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    enc = encoder.Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7,4)
    controller = pcontroller.Pcontroller(motorvoltage)
    enc.zero()
    md.set_duty_cycle(0)
    kp = 0.15
    ki = 0
#    psat = 0.15*motorvoltage/ki
#    nsat = -psat
    psat = nsat = 0
    controller.setgain(kp,ki,psat,nsat)

    while True:
        
        if Controls == INPUT: #if in INPUT state
#            mdone1 = md1.get(False) 
                       
            ref = sm1.get(False)
#            enc.zero()
            #print('I1')
            controller.setsetpoint(ref)
            if  NEWVAL1 == 1:   
                Controls = GOING
                NEWVAL1 = 0
                #print('SET')
                #print(NEWVAL1)
        elif Controls == GOING:            
#            if NEWVAL1 == 1:
#                ref = sm1.get(False)
#                controller.setsetpoint(ref)
#                NEWVAL1 = 0
            location = enc.read()
            pwm = controller.control(location)
            if pwm >= 25:
                pwm = 25
            elif pwm <= -25 :
                pwm = -25
            md.set_duty_cycle(pwm)
            cont_count +=1
            if abs(location-ref) <= 10:
                mdone1 = 1
                if mdone3 == 1 and mdone2 == 1 and mdone1 ==1:
                    md.set_duty_cycle(0)
                    Controls = INPUT
            else:
                mdone1 = 0
            #print(str(ref) + ',' + str(location) + ',' + str(abs(location-ref)) + ',' + str(mdone1) + ',' + str(pwm))
            #print(str(ref) + ',' + str(mdone1) + ',' + str(NEWVAL1))
            print('1'+','+str(ref) + ',' + str(location))
        else:
            raise ValueError ('Illegal state for task 1')
        # Periodically check and/or clean up memory
        counter += 1
        if counter >= 60:
            counter = 0
            print_task.put (' Memory: {:d}\n'.format (gc.mem_free ()))
        yield (Controls)

def Control2 ():
    ''' Proportional Control of Motor 2, which controls the 2nd link
    which holds the paintbrush'''
    global mdone1
    global mdone2
    global mdone3
    global NEWVAL2
    Controls = INPUT
    counter = 0
    cont_count = 0
    md = motordriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)
    enc = encoder.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7,8)
    motorvoltage = 12
    controller = pcontroller.Pcontroller(motorvoltage)
    enc.zero()
    md.set_duty_cycle(0)
    kp = 0.15
    ki = 0
#    psat = 0.15*motorvoltage/ki
#    nsat = -psat
    psat = nsat = 0
    controller.setgain(kp,ki,psat,nsat)
    #motor initialize stuff
    ###change to new motors
    
    while True:
        
        if Controls == INPUT: #if in INPUT state
#            mdone2 = md2.get(False) 
            ref = sm2.get(False) 
#            enc.zero()
            controller.setsetpoint(ref)
            
            if  NEWVAL2==1:   
                Controls = GOING
                NEWVAL2 = 0
                
        elif Controls == GOING:
#            if NEWVAL2 == 1:
#                ref = sm2.get(False)
#                controller.setsetpoint(ref)
#                NEWVAL2 = 0            
            location = enc.read()
            pwm = controller.control(location)
            if pwm >= 25:
                pwm = 25
            elif pwm <= -25 :
                pwm = -25
            md.set_duty_cycle(pwm)
            cont_count +=1
            if ((abs(location-ref) <= 10)):
                mdone2 = 1
                if mdone3 == 1 and mdone2 == 1 and mdone1 ==1:
                    md.set_duty_cycle(0)
                    Controls = INPUT
            else:
                mdone2 = 0
            #print(str(ref) + ',' + str(mdone2) + ',' + str(NEWVAL2))
            print('2'+','+str(ref) + ',' + str(location))
        else:
            raise ValueError ('Illegal state for task 1')
    
        # Periodically check and/or clean up memory
        counter += 1
        if counter >= 60:
            counter = 0
            print_task.put (' Memory: {:d}\n'.format (gc.mem_free ()))
    
        yield (Controls)
    
def Control3 ():
    ''' Proportional Control of Motor 3, which controls the z-axis  '''
    global mdone1
    global mdone2
    global mdone3
    global NEWVAL3
    
    Controls = INPUT
    counter = 0
    cont_count = 0
    md = md3.MD3(pyb.Pin.board.PB0, pyb.Pin.board.PB8, pyb.Pin.board.PB9, 3)
    enc = encoder.Encoder(pyb.Pin.board.PA8,pyb.Pin.board.PA9,1)
    motorvoltage = 12
    controller = pcontroller.Pcontroller(motorvoltage)
    enc.zero()
    md.set_duty_cycle(0)
    kp = 0.1
    ki = 0
#    psat = 0.15*motorvoltage/ki
#    nsat = -psat
    psat = nsat = 0
    controller.setgain(kp,ki,psat,nsat)
    location = 0
    #motor initialize stuff
    ###change to new motors
    
    while True:
        
        if Controls == INPUT: #if in INPUT state
#            mdone3 = md_3.get(False) 
            ref = sm3.get(False) 
#            enc.zero()
            controller.setsetpoint(ref)
            #print('I3')
            if  NEWVAL3==1:   
                Controls = GOING
                NEWVAL3 = 0
                #print('set')
                
        elif Controls == GOING:
#            if NEWVAL3 == 1:
#                ref = sm3.get(False)
#                controller.setsetpoint(ref)
#                NEWVAL3 = 0
            location = enc.read()
            pwm = controller.control(location)
            md.set_duty_cycle(pwm)
            cont_count +=1
            if abs(location-ref) <= 50:
                mdone3 = 1
                if mdone3 == 1 and mdone2 == 1 and mdone1 ==1:
                    md.set_duty_cycle(0)
                    Controls = INPUT
            print('3'+','+str(ref) + ',' + str(location))
        else:
            raise ValueError ('Illegal state for task 1')
    
        # Periodically check and/or clean up memory
        counter += 1
        if counter >= 60:
            counter = 0
            print_task.put (' Memory: {:d}\n'.format (gc.mem_free ()))
    
        #print(Controls)
        yield (Controls)
# =============================================================================

if __name__ == "__main__":
    global mdone1
    global mdone2
    global mdone3
    global NEWVAL1
    global NEWVAL2
    global NEWVAL3 
        #counter to increment motor tick command lists. Starts at 1 becasue we start at state 2
    mcount = 1
    #Counter keeping track of when more paint is needed
    pcount = 0
    #Counter to increment more paint command list
    ccount = 0
    #Counter to increment wash brush command list
    wcount = 0
    #Calibrated value when more paint needed
    MORESAUCE = 1000
    #Variable to select color
    Color_Select = 0
    #Done flag for get more paint state
    SAUCED = 0
    #NEW Value flag
    NEWVAL1 = 0
    NEWVAL2 = 0
    NEWVAL3 = 0
    #Motor done flags
    mdone1 = 0
    mdone2 = 0
    mdone3 = 0
    #flag to say file has been laoded
    loaded = 0
    print ('\033[2JTesting scheduler in cotask.py\n')
    
    # Create a share and some queues to test diagnostic printouts
    sm1 = task_share.Share ('f', thread_protect = False, name = "Share_1")
    sm2 = task_share.Share ('f', thread_protect = False, name = "Share_2")
    sm3 = task_share.Share ('f', thread_protect = False, name = "Share_3")
#    md1 = task_share.Share ('B', thread_protect = False, name = "mdone1")
#    md2 = task_share.Share ('B', thread_protect = False, name = "mdone2")
#    md_3 = task_share.Share ('B', thread_protect = False, name = "mdone3")
#    nv = task_share.Share ('B', thread_protect = False, name = "new value")
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (Control1, name = 'Control1', priority = 4, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (Control2, name = 'Control2', priority = 4, 
                         period = 10, profile = True, trace = False)
    task3 = cotask.Task (Control3, name = 'Control3', priority = 5, 
                         period = 10, profile = True, trace = False)
    task4 = cotask.Task (Overlord, name = 'Overlord', priority = 2, 
                         period = 50, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task4)

    # A task which prints characters from a queue has automatically been
    # created in print_task.py; it is accessed by print_task.put_bytes()

    # Create a bunch of silly time-wasting busy tasks to test how well the
    # scheduler works when it has a lot to do
#    for tnum in range (10):
#        newb = busy_task.BusyTask ()
#        bname = 'Busy_' + str (newb.ser_num)
#        cotask.task_list.append (cotask.Task (newb.run_fun, name = bname, 
#            priority = 0, period = 400 + 30 * tnum, profile = True))

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is sent through the serial por
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list) + '\n')
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')

