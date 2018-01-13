# This program will let you test your ESC and brushless motor.
# Make sure propeller is not attached.

import argparse #importing argparse library 
import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library, type "sudo killall pigpiod" if the library can't init

#ESC=4  #Connect the ESC in this GPIO pin 

pi = pigpio.pi();
#pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 700  #change this if your ESC's min value is different or leave it be
#print ("For first time launch, select calibrate")
#print ("Type the exact word for the function you want")
#print ("calibrate OR manual OR control OR arm OR stop")

def manual_drive(ESC,arm_speed): #You will use this function to program your ESC if required

    while True:
    #    if inp == "stop":
    #        stop(ESC)
    #        break
       # print ("motor spins")
        pi.set_servo_pulsewidth(ESC,arm_speed)
    #    time.sleep(0.5)
        #pi.set_watchdog(ESC,3000)
       # print ("input new value and press enter")
        #inp=input()
                
def calibrate(ESC):   #This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print ("calibration selected on pin:"+ str(ESC), "\n")
    print("Disconnect the battery and press Enter \n")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print ("Setting minimum value, it will take 12 second")
            time.sleep(12)
            print ("Calibration done, resetting ESC")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print ("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print ("Motor armed")
            #control(ESC) # You can change this to any other function you want
            
def control(ESC): 
    print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 1500    # change your speed if you want to.... it should be between 700 - 2000
    print ("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        
        if inp == "q":
            speed -= 100    # decrementing the speed like hell
            print ("speed = %d" % speed)
        elif inp == "e":    
            speed += 100    # incrementing the speed like hell
            print ("speed = %d" % speed)
        elif inp == "d":
            speed += 10     # incrementing the speed 
            print ("speed = %d" % speed)
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print ("speed = %d" % speed)
        elif inp == "stop":
            stop(ESC)          #going for the stop function
            break
        elif inp == "manual":
            manual_drive(ESC)
            break
        elif inp == "arm":
            arm(ESC)
            break	
        else:
            print ("WHAT DID I SAID!! Press a,q,d or e")
            
def arm(ESC,arm_speed): #This is the arming procedure of an ESC 
    print ("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(2)
        manual_drive(ESC,arm_speed) 
        
def stop(ESC): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

def Main():    
    parser = argparse.ArgumentParser()
    group= parser.add_mutually_exclusive_group()
    parser.add_argument("pin", help="Input the GPIO Pin connected to the ESC.", type=int)
    group.add_argument("-c", "--calibration", action="store_true",\
                       help="calibrate ESC for first time useage.")
    group.add_argument("-m", "--move", action="store_true", \
                       help="spin the motor, motor must be arm and calibrated.")
    group.add_argument("-s", "--stop_motor", action="store_true", help="stop the motor.")
    group.add_argument("-a", "--arm_motor", action="store_true", help="arm the motor.")
    group.add_argument("-man", "--manual_motor", action="store_true", \
                       help="manually input value to spin the motor.")
    parser.add_argument("speed",nargs="?",help="manual input motor speed",type=int)
    args = parser.parse_args()

    if args.calibration:
        calibrate(args.pin)
    elif args.move:
        control(args.pin)
    elif args.stop_motor:
        stop(args.pin)
    elif args.arm_motor:
        arm(args.pin,args.speed)
    elif args.manual_motor:
        if args.speed is None:
            print("missing speed value, range (700-2000)")
            stop(args.pin)
        else:
            arm(args.pin, args.speed)

if __name__== '__main__':
    Main()
