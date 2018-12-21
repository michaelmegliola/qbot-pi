import RPi.GPIO as GPIO
import time
import numpy as np
GPIO.setmode(GPIO.BOARD)
################################################################################
#                                                                              #
# Utility class to drive stepper motor using H-bridge on BeagleBone Blue       #
#                                                                              #
################################################################################

class Stepper_28byj:
    halfstep_seq = [(1,0,0,0), (1,1,0,0), (0,1,0,0), (0,1,1,0), (0,0,1,0), (0,0,1,1), (0,0,0,1), (1,0,0,1)]
    step_interval = 0.005
    degrees_per_step = 0.0875

    def __init__(self, stepper_pins=[7,11,13,15]):
        self.stepper_pins = stepper_pins
        self.position = 0
        self.n = 0
        for pin in stepper_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)


    def start(self):
        pass

    def stop(self):
        pass

    def reset(self):
        pass

    def move(self, degrees):
        t0 = time.time() + Stepper_28byj.step_interval
        steps = int(round(degrees)/Stepper_28byj.degrees_per_step)
        for x in range(abs(steps)):
            while (time.time() < t0):
                pass
            for pin in range(4):
                GPIO.output(self.stepper_pins[pin], Stepper_28byj.halfstep_seq[self.n][pin])
            self.n += -1 if degrees > 0 else 1
            self.n %= len(Stepper_28byj.halfstep_seq)
            t0 = time.time() + Stepper_28byj.step_interval

        self.position += steps * Stepper_28byj.degrees_per_step


    def batch(stepper_request):                        #pass in a np array of tuples: [stepper, desired_position]
        t0 = time.time() + Stepper_28byj.step_interval
        while np.any(stepper_request[...,1]) > 0:
            print(stepper_request[...,1])
            for motor in stepper_request:                  #for each motor (tuple) in the array
                if abs(motor[1]) > 0:                      #if we're not done moving it
                    for x in range(8):                     #move this motor 8 microsteps 
                        while (time.time() < t0):
                            pass
                        for pin in range(4):
                            GPIO.output(motor[0].stepper_pins[pin], Stepper_28byj.halfstep_seq[motor[0].n][pin])
                            motor[0].n += -1 if motor[1] < 0 else 1        # decrement remaining distance
                            motor[0].n %= len(Stepper_28byj.halfstep_seq)  #roll stepper position marker
                            t0 = time.time() + Stepper_28byj.step_interval
                    motor[0].position += -0.7 if motor[1] > 0 else 0.7     #increment stepper position by 8 microsteps
                    motor[1] += -0.7 if motor[1] > 0 else 0.7              #decrement remaining distance to move
                    if -0.7 < motor[1] < 0.7:
                        motor[1] = 0                                       #zero out if less than one move away 


