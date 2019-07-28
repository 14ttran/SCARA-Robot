''' @file hpgl_coord.py
This program takes in hpgl file and parses it into a of (i,x,y) coordinates
as each element of the list, where i indicates pen up or down. It takes only 
hpgl files with paths in them.The higher resolution of the x,y coordinates 
the better.

@author Tomy Tran
@copyright Tomy Tran

**Based on parse_hpgl.py by Samuel Lee** 

'''

import math

def parse_file(file_name, resolution = 1016):
    ''' Takes in a file name for a hpgl file and parses it into a list.
    A raw hpgl file has text that looks as follows:
    
    IN;SP1;PU0,0;PD0,90;PU487,751;PD492,749
    
    the first two letters determines the code command. 
    Each command has a certain amount of parameters thereafter that represent
    a particular setting or position.
    
    Each command is separated by a ';'
    
    For more information on hpgl code refer to
    @link http://www.isoplotec.co.jp/HPGL/eHPGL.htm @endlink
    
    @param file_name The hpgl file name 'names.hpgl', use quotes
    @param resolution the resolution of the hpgl conversion, default=1016dpi
    @return coord_list List of (i,x,y) coordinates in inches, i is unitless
    index for up = 1 or down = 0
    '''
    # Determining if the code is a file already or a str for the file name.
    if type(file_name) == str:
        file = open(file_name, 'r')
    else:
        file = file_name
    # Read the file text
    string_file = file.readline()
    # Close the file    
    file.close()
    # Split by every command
    all_list = string_file.split(';')
    # Delete the last split which is a newline character
    del all_list[-1]
    # Initialize the list for the parsed results units are pixels
    coord_list = []
    # Set resolution in dpi
    res = resolution
    # For every command in the hpgl code
    for n in all_list:
        # The first two letters of the element determine the command
        cmd = n[:2]
        if len(n)>2:
            # Some commands do not have arguments (e.g. IN)
            # This makes the commands that do have arguments have numbers
            numbers = n[2:]
            
        if cmd == 'IN':
            # Initialize for go to home, pass this cmd
            pass
#            coord_list.append(['IN',(0,0)])
        elif cmd == 'SP':
            # Select Pen and a zero zero which does not have a purpose but 
            # placed just to have a consistent format
            pass
#            coord_list.append(['SP',(0,0)])
        elif cmd == 'PU':
            # Pen Up and the coordinate at which to bring the pen up
#            PU_list = []
            i = 0
            coordinates = numbers.split(',')
            while i < len(coordinates):
                #convert the coordinate values to inches                
                inch_coord1 = round(int(coordinates[i])/res,2)
                inch_coord2 = round(int(coordinates[i+1])/res,2)
#                inch_coord1 = round(inch_coord1, 2)
#                inch_coord2 = round(inch_coord2, 2)
#                PU_list.extend(pair_split(coordinates))
                # Adds the coordinates (i,x,y) in as lists
                coord_list.append([1,inch_coord1,inch_coord2])
                i += 2
        elif cmd == 'PD':
            # Pen Down and the coordinates to move the pen
#            PD_list = ['PD']
            j = 0
            coordinates = numbers.split(',')
            while j < len(coordinates):
                #convert the coordinate values to inches                
                inch_coord1 = round(int(coordinates[j])/res,2)
                inch_coord2 = round(int(coordinates[j+1])/res,2)
#                inch_coord1 = round(inch_coord1, 2)
#                inch_coord2 = round(inch_coord2, 2)
#                PD_list.extend(pair_split(coordinates))
                # Adds the coordinates (i,x,y) in as lists
                coord_list.append([0,inch_coord1,inch_coord2])
                j += 2
        else:
            print('Error, unknown command')
    #delete the first command of the file so it starts with drawing
    #ONLY WORKS IF TOOL OFFSET IS ZERO
    del coord_list[:2]
    
    return coord_list

def inv_kinematics(xyzcoord, picxoffset = 0.25, picyoffset = 0.25):
    '''Function that uses denavit-hartenberg method to get inverse kinematics
    for the 2 revolute joints.
    THIS FUNCTION IGNORES i-COORDINATE FOR THIS ROBOT.
    
    For more info about inverse kinematic calculations here
    @link https://appliedgo.net/roboticarm/
    
    @param xyzcoord A list with each element being a point (i,x,y) in inches.
    @return joint_angles List of joint angles for each joint in form of
    [up or down, j1 angle, j2 angle]
    '''
    #define elements of the robot
    #length of the first arm joint-to-joint in inches    
    a1 = 7.42
    #length of the second arm joint-to-joint in inches
    a2 = 5.5
    #limits of the joint angles in degrees
    j1low = -58
    j1high = 68
    j2low = -180
    j2high = 180
    
    #offset of universe frame to  first robot axis in inches
    robotxoffset = 1.39
    robotyoffset = -5.58       
    
    #picture offset from hpgl file (moving the bottom left corner up and right)
    totalxoffset = robotxoffset + picxoffset
    totalyoffset = robotyoffset + picyoffset
    
    #create a list of joint angles from the list of xy-coord
    #list of angles in degrees [up or down, j1, j2]
    angles = []
    for i in range(len(xyzcoord)):
        #define element as each element in list [up or down, xcoord, ycoord]
        element = xyzcoord[i]
        #offset hpgl coordinates to line up in the physical system        
        element[1] += totalxoffset
        element[2] += totalyoffset
        
        #calculate inverse kine equations from
        #https://appliedgo.net/roboticarm/
        
        hypotenuse = math.sqrt(element[1]*element[1] + element[2]*element[2])
        intermediate_angle = math.degrees(math.acos((a1*a1 + hypotenuse*hypotenuse - a2*a2)/(2*a1*hypotenuse)))
        if element[2] >= 0:            
            j1 = round(math.degrees(math.atan2(element[2],element[1])) - intermediate_angle, 2)
            j2 = round(180 - math.degrees(math.acos((a1*a1 + a2*a2 - hypotenuse*hypotenuse)/(2*a1*a2))), 2)
        elif element[2] < 0:
            j1 = round(math.degrees(math.atan2(element[2],element[1])) + intermediate_angle, 2)
            j2 = round(math.degrees(math.acos((a1*a1 + a2*a2 - hypotenuse*hypotenuse)/(2*a1*a2))) - 180, 2)
        
        #convert joint angles [deg] to motor ticks for 
        #Polulu 37D gearmotor with encoder [3200 ticks/rev]
        ticks1 = int(j1 * 8.89)
        ticks2 = int(j2 * 8.89)
        
        #save to list angles in form [up down, ticks1, ticks2]
        angles.append([element[0],ticks1,ticks2])
        
    return angles

def file_save(file_name, data):
    '''This function is a filesaving function to store a list to a text file.
    @param file_name Is the name of the desired file, example 'test.txt'
    @param data is any data that is to be saved to file
    '''
    #check that the filename is a string
    if type(file_name) == str:
        file = open(file_name, 'w')
    for i in range(len(data)):
        element = data[i]
        file.write(str(element[0])+', '+str(element[1])+', '+str(element[2])+'\n')
    file.close
