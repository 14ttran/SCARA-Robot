# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import utime
import motordriver
import encoder
import pcontroller

# @Testing
#if __name__ == '__main__':
#    while True:    
#        print('Commands:\nTrack position\n')        
#        command = input('What do you want to do? ')
#        if str(command) == str('Track position'):
#            encoder = Lab_1.Encoder()
#            while True:
#                try:
#                    position = encoder.read()
#                    utime.sleep_ms (100)
#                except KeyboardInterrupt:
#                    break
#            print('\n*<----- You are here\n')

#if __name__ == '__main__':
#motordriver = motordriver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5)
#encoder = encoder.Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7,8)
#controller = pcontroller.Pcontroller(12)
motordriver = motordriver.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
encoder = encoder.Encoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7,4)    
controller = pcontroller.Pcontroller(12)

while True:
    #    while True:
    input()
    time = []
    position = []
    kp = float(input('Set kp '))
    ki = float(input('Set ki '))
    psat = float(input('Set sat '))
    nsat = -psat
#    gain = 0.01
#    reference = float(input('Set reference '))
    reference = 300
    controller.setgain(kp,ki,psat,nsat)
    controller.setsetpoint(reference)
    period = float(input('Set  period ')) + utime.ticks_ms()
    #period = 500 + utime.ticks_ms()
    encoder.zero()
    while period >= utime.ticks_ms():
        try:
            location = encoder.read()
            time.append(utime.ticks_ms())
            position.append(location)
            #print ('Location ' + str(location))
            pwm = controller.control(location)
            #print('PWM is ' + str(pwm))
            motordriver.set_duty_cycle(pwm)
            utime.sleep_ms(10)
        except KeyboardInterrupt:
            break
    
    time[:] = [x-time[0] for x in time]
    #    print('Run done.\n')
    for i in range(len(time)):
        print(str(time[i]) +','+ str(position[i]))
    encoder.zero()
    
    print('1')
    
    #if __name__ == '__main__':
    #    motordriver = motordriver.MotorDriver()
    #    encoder = encoder.Encoder()
    #    while True:
    #        pwm = float(input('Set pwm '))
    #        motordriver.set_duty_cycle(pwm)
    #        while True:
    #            try:
    #                location = encoder.read()
    #                print ('Location ' + str(location))
    #                utime.sleep_ms(10)
    #            except KeyboardInterrupt:
    #                break
