# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 21:21:47 2018

@author: mecha13
"""
class Loadfile:
    '''This class loads data from an imported file and converts to encoder ticks'''
    def __init__(self, filename):
        self.filename = filename

        #Convert x,y,z coordinates to encoder ticks through derived two link
        #inverse kinematics. Place results in lists then return 
    def normal(self):
        '''This method loads files that do not need conversion into lists
        '''
        with open (self.filename, 'r') as a_file:
            #insert sam code here
            self.lines = a_file.readlines () 
            self.m1 = []
            self.m2 = []
            self.m3 = []
            
            for num in self.lines:
                try:
                    self.num1 = float(num.split(',')[0])
                    self.num2 = float(num.split(',')[1])
                    self.num3 = float(num.split(',')[2])
                    
                except ValueError:
                    pass
                except IndexError:
                    pass
                #Perform inverse kinematics and ticks conversion here
                else:
                    self.m1 += [self.num1]
                    self.m2 += [self.num2]
                    self.m3 += [self.num3]
        
                    
        return self.m1,self.m2,self.m3;    
    def converthpgl(self,res):
        '''This method converts from hpgl coordinates to encoder tick commands
        @param res is the resolution of the profile, in steps per inch
        '''
        with open (self.filename, 'r') as a_file:
            #insert sam code here
            self.lines = a_file.readlines () 
            self.m1 = []
            self.m2 = []
            self.m3 = []
            
            for num in self.lines:
                try:
                    self.num1 = float(num.split(',')[0])
                    self.num2 = float(num.split(',')[1])
                    self.num3 = float(num.split(',')[2])
                    
                except ValueError:
                    pass
                except IndexError:
                    pass
                #Perform inverse kinematics and ticks conversion here
                else:
                    self.m1 += [self.num1*(1/res)]
                    self.m2 += [self.num2*(1/res)]
                    self.m3 += [self.num3*(1/res)]
        
                    
        return self.m1,self.m2,self.m3;
#Test code       
#if __name__ == '__main__':
##    while True:
#    x = []
#    y = []
#    z = []
#    
#    try:
#        filename = input('Enter profile filename\n')
##            res = input(')
#        load = Loadfile(filename)
#        mU,m1,m2 = load.normal()
#        print(*mU)
#        print(*m1)
#        print(*m2)
#        
#    except KeyboardInterrupt:
#        pass
      
    
