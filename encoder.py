# -*- coding: utf-8 -*-
#
## @file cotask.py
#  This file contains the Encoder class used to determine the location of a motor
import pyb
import math

class Encoder:
    """This class implements the encoder a DC motor to the ME 405 board.
    
    Example:
    \code
    ''' Create an Encoder object '''
    enc = encoder.Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7,4)
    ''' Get the current location of the motor '''
    location = enc.read()
    ''' Zero the encoder reading at the current location '''
    enc.zero()
    \endcode
    """
    def __init__(self,positive_pin,negative_pin,timer):
        '''Initializes the GPIO pins to read the encoder channels
        @param positive_pin this pin reads the 'positive' side of the encoder
        @param negative_pin this pin reads the 'negative' side of the encoder
        @param timer increments or decrements according to the changes in
        the positive and negative pins
        '''
        #print ('Creating the time keeper.')
        #self.pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.OUT_PP)
        #self.pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.OUT_PP)
        self.pos_pin = pyb.Pin (positive_pin, pyb.Pin.OUT_PP)
        self.neg_pin = pyb.Pin (negative_pin, pyb.Pin.OUT_PP)
        
#        self.tim8_ch1 = pyb.Timer (8, freq=20000)
#        self.ch1 = self.tim8_ch1.channel (1, pyb.Timer.ENC_A, pin=self.pinC6)
#        self.tim8_ch2 = pyb.Timer (8, freq=20000)
#        self.ch2 = self.tim8_ch2.channel (2, pyb.Timer.ENC_B, pin=self.pinC7)
        
        #self.tim8_ch1 = pyb.Timer (8, period=65535, prescaler=0)
        self.timer = pyb.Timer (timer, period=65535, prescaler=0)        
        self.ch1 = self.timer.channel (1, pyb.Timer.ENC_AB, pin=self.pos_pin)
        #self.tim8_ch2 = pyb.Timer (8, period=65535, prescaler=0)
        self.ch2 = self.timer.channel (2, pyb.Timer.ENC_AB, pin=self.neg_pin)

        self.A_position = 0
        self.A_last = 0

    def read(self):
        '''Reads the encoder output and calculates the current position of the motor'''
        #Code for channel A        
        self.A_current = self.timer.counter()
        self.A_delta_position = self.A_current - self.A_last
        if (self.A_delta_position > 32768): # and (self.A_delta_positionlast < 0)):
            self.A_delta_position = -65536+self.A_delta_position
        elif (self.A_delta_position < -32768):# and (self.A_delta_positionlast > 0)):
            self.A_delta_position = 65536+self.A_delta_position
        self.A_position += self.A_delta_position
        self.A_last = self.A_current
        self.A_delta_positionlast = self.A_delta_position
        #print ('A =' + str(self.A_position))
        
        ##radial position in float [rad]         
        self.radial = self.A_position * (2*math.pi/4000)
        

        return self.A_position

    def zero(self):
        '''Resets the encoder position to zero.'''
        self.A_position = 0
        self.A_last = self.timer.counter()


#if __name__ == '__main__':
#    encoder = encoder.Encoder()
#    while True:
#        try:
#            position = encoder.read()
#            utime.sleep_ms (100)
#        except KeyboardInterrupt:
#            break
#    print('\n*<----- You are here\n')