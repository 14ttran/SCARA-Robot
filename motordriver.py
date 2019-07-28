# -*- coding: utf-8 -*-
#
## @file cotask.py
#  This file contains the MotorDriver class used to drive a DC motor
"""
Spyder Editor

This is a temporary script file.
"""

import pyb

class MotorDriver:
    """This class implements a motor driver for the ME 405 board.
    
    Example:
    \code
    ''' Create a MotorDriver object '''
    md = motordriver.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    ''' Drive the motor with a pwm signal '''
    pwm = 50 #set a pwm of 50%    
    md.set_duty_cycle(pwm)
    \endcode """
    
    def __init__(self, enable_pin, positive_pin, negative_pin, timer):
        '''Creates a motor driver by intializing GPIO pins and turning the
        motor off for safety.
        @param enable_pin this pin enables the motor driver to supply power
        to the motor.
        @param positive_pin this pin supplies voltage to the 'positive' side of
        the motor
        @param negative_pin this pin supplies voltage to the 'negative' side of
        the motor
        @param timer this timer controls the pwm timing of the output pins.
        '''
        self.en_pin = pyb.Pin (enable_pin, pyb.Pin.OUT_PP)
        #sets EN_A pin
        #self.pinB4 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
        self.pos_pin = pyb.Pin (positive_pin, pyb.Pin.OUT_PP)
        #sets IN1_A pin
        #self.pinB5 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
        self.neg_pin = pyb.Pin (negative_pin, pyb.Pin.OUT_PP)
        #sets IN2_A pin
        self.en_pin.low()           #sets motor to off
        
        self.timer = pyb.Timer (timer, freq=20000)
        self.ch1 = self.timer.channel (1, pyb.Timer.PWM, pin=self.pos_pin)
        self.ch2 = self.timer.channel (2, pyb.Timer.PWM, pin=self.neg_pin)

        #print ('Creating a motor driver')

    def set_duty_cycle (self, level):
        '''This method sets the duty cycle to be sent to the motor to the
        given level. Positive values cause torque in one direction, negative
        values in the opposite direction.
        @param level A signed integer holding the duty cycle of the voltage
        sent to the motor'''
        self.en_pin.high()
        
        if (level >= 0):
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(level)
            
        elif (level < 0):
            self.ch2.pulse_width_percent(0)
            self.ch1.pulse_width_percent(-1*level)
        
        #print ('Setting duty cycle to ' + str (level))        
            
