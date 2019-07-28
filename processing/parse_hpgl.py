''' @file parse_hpgl.py
This program takes in hpgl file and parses it into a list of commands and 
parses it into a list of commands and positions. It takes only hpgl files with
paths in them. It returns a list with the commands and coordinates for relevant
commands. The more high resolution of the x,y coordinates the better.

@author Samuel Lee
@copyright Samuel Lee 

'''

def parse_file(file_name):
    ''' Takes in a file name for a hpgl file and parses it into a list.
    A raw hpgl file has text that looks as follows:
    
    IN;SP1;PU0,0;PD0,90;PU487,751;PD492,749
    
    the first two letters determines the code command. 
    Each command has a certain amount of parameters thereafter that represent
    a particular setting or position.
    
    Each command is separated by a ';'
    
    For more information on hpgl code refer to
    @link http://www.isoplotec.co.jp/HPGL/eHPGL.htm @endlink
    
    @param file_name The hpgl file name 'names.hpgl'
    @return parsed_list List of command, nested list with command & parameters
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
    # Initialize the list for the parsed results
    parsed_list = []
    # For every command in the hpgl code
    for n in all_list:
        # The first two letters of the element determine the command
        cmd = n[:2]
        if len(n)>2:
            # Some commands do not have arguments (e.g. IN)
            # This makes the commands that do have arguments have numbers
            numbers = n[2:]
            
        if cmd == 'IN':
            # Initialize for go to home
            parsed_list.append(['IN',(0,0)])
        elif cmd == 'SP':
            # Select Pen and a zero zero which does not have a purpose but 
            # placed just to have a consistent format
            parsed_list.append(['SP',(0,0)])
        elif cmd == 'PU':
            # Pen Up and the coordinate at which to bring the pen up
            PU_list = ['PU']
            coordinates = numbers.split(',')
            PU_list.extend(pair_split(coordinates))
            # Adds the coordinates (x,y) in as tuples
            parsed_list.append(PU_list)
        elif cmd == 'PD':
            # Pen Down and the coordinates to move the pen
            PD_list = ['PD']
            coordinates = numbers.split(',')
            PD_list.extend(pair_split(coordinates))
            # Adds the coordinates (x,y) in as tuples
            parsed_list.append(PD_list)
        else:
            print('Error, unknown command')
    return parsed_list

def pair_split(iterable):
    ''' A quick function to split a list and pair up elements in a list.
    This is particular to a list of integers and returns the coordinates
    as tuples
    @param iterable A list of integers of paired x,y coordinates (x1,y1,x2,y2)
    @return list_of_pairs Returns a list of tuples of the coordinates
    '''
    list_of_pairs = []
    i = 0
    # While loop to pair up list
    while i < len(iterable):
        list_of_pairs.append((int(iterable[i]),int(iterable[i+1])))
        i += 2 
    return list_of_pairs
    