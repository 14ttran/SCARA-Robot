# -*- coding: utf-8 -*-
#
## @file cotask.py
#  This file contains the Pcontroller class used to control a DC motor
"""
Spyder Editor

This is a proportional controller class.
Author: Ahmed Shorab, Kevin Tran, Tomy Tran
"""

#motor operating voltage

class Pcontroller:
    """This class implements a proportional controller for the motor. It is
    intended to be called continuously in order to properly control the
    location of the motor
    
    Example of how to use each function individually:
    \code
    ''' Create an Pcontroller object '''
    motorvoltage = 12 #Volts
    controller = pcontroller.Pcontroller(motorvoltage)
    ''' Set the destination of the motor '''
    destination = 1000
    controller.setsetpoint(destination)
    ''' Set the gain and saturation values of the controller '''
    kp = 0.01
    ki = 0
    psat = 4000
    nsat = -4000
    controller.setgain(kp,ki,psat,nsat)
    ''' Calculate the pwm value to send to the motor '''
    current_location = 0
    pwm = controller.control(current_location)
    \endcode
    """
    def __init__ (self, motor_voltage, kp = 0.0, ki = 0.0,psat =0,nsat=0,setpoint = 0):
        '''Initializes the motor controller with the appropriate gain, motor
        voltage, and setpoint. Contains code to implement integral control,
        but it is not recommended as the form of integral control implemented
        is not appropriate for stable position control.
        @param motor_voltage the voltage supplied to the motor
        @param kp the proportional gain
        @param ki the integral gain, recommend 0
        @param psat maximum 'positive' integral error
        @param nsat maximum 'negative' integral error
        @param setpoint desired location to move the motor to
        '''
        ## reference location [rad -> ticks]       
        self.setpoint = setpoint
        
        ## proportional gain
        self.kp = kp
        ## integral gain
        self.ki = ki
        ## peak motor voltage rating
        self.motor_voltage = motor_voltage
        #initialize 
        self.ierror = 0
        self.psat = psat
        self.nsat = nsat
        #print('Gain is ' + str(gain) + 'Setpoint is ' + str(self.setpoint))
        
    def control (self, actual = 0):
        '''This method computes the control loop.
        @param actual The measured location for feedback.        
        '''
        ## feedback value [ticks]        
        self.actual = actual

        ## error calculation [ticks]       
        self.perror = self.setpoint - self.actual
        #print('Error is ' + str(self.error))
        self.ierror += self.perror
        if self.ierror >= self.psat:
            self.ierror = self.psat
        elif self.ierror <= self.nsat:
            self.ierror = self.nsat
        ## proportional control calculation [volts]      
        self.actuation = (self.perror * self.kp) + ((self.ierror * self.ki))
        
        # saturation block to max signal value
#        if  self.pwm > 100:
#            self.pwm = 100
#        elif self.pwm < -100:
#             self.pwm = -100
#        
#        return self.pwm

        # saturation block to max signal value
        if self.actuation > self.motor_voltage:
            self.actuation = self.motor_voltage
        elif self.actuation < -1*(self.motor_voltage):
            self.actuation = -1*(self.motor_voltage)
        
        # duty cycle calculation [percent]
        self.pwmsignal = (self.actuation/self.motor_voltage)*100
        print (self.ierror)
        return self.pwmsignal
        
    def setsetpoint (self, setpoint):
        '''This method sets the reference value so the class need not be
        called again.
        @param setpoint A reference location for the controller.
        '''
        self.setpoint = setpoint
        
    def setgain (self, kp,ki,psat,nsat):
        '''This method sets the proportional gain so the class need not be
        called again.
        @param kp the proportional gain
        @param ki the integral gain, recommend 0
        @param psat maximum 'positive' pwm signal allowed
        @param nsat maximum 'negative' pwm signal allowed
        '''
        self.kp = kp
        self.ki = ki
        self.psat = psat
        self.nsat = nsat

        
