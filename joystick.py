import sys
import pygame
import serial
from serial import SerialException
import serial.tools.list_ports
import os

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))

    pygame.joystick.init()

    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    if len(joysticks) == 0:
        print('Joystick not detected')
        exit()

    joystick = joysticks[0]
    joystick.init()

    clock = pygame.time.Clock()

    print()
    ser = None
    while ser is None:
        print('Getting available ports...')
        ports = serial.tools.list_ports.comports()
        # List available ports
        for i in range(len(ports)):
            print(str(i+1) + ': ' + ports[i].device)

        # Get selection from user input
        choice = input('Select a bluetooth port: ')
        while int(choice) < 1 or int(choice) > len(ports):
            print('Please input a value between 1 and ' + str(len(ports)))
            choice = input('Select a bluetooth port: ')

        port = ports[int(choice) - 1].device
        print('Connecting to ' + port + '...')
        # Connect to serial port
        try:
            ser = serial.Serial(port, 9600)
        except SerialException as e:
            print('Error: {}'.format(e))
    print('Connection established.')
    print('Use the controller to control robot')

    done = False

    lastX = 0
    lastY = 0

    # Send keydown and keyup events over serial connection
    while not done:
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                done = True # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                pass
                # print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                pass
                # print("Joystick button released.")

        if os.name == 'posix':
            x_axis = joystick.get_axis(2)
        else:
            x_axis = joystick.get_axis(4)
        y_axis = joystick.get_axis(1)

        if x_axis > 0.5 and lastX <= 0.5:
            print("KEYDOWN, right")
            ser.write(bytes('275,d\n', 'utf-8'))
        elif x_axis <= 0.5 and lastX > 0.5:
            print("KEYUP, right")
            ser.write(bytes('275,u\n', 'utf-8'))
        elif x_axis < -0.5 and lastX >= -0.5:
            print("KEYDOWN, left")
            ser.write(bytes('276,d\n', 'utf-8'))
        elif x_axis >= -0.5 and lastX < -0.5:
            print("KEYUP, left")
            ser.write(bytes('276,u\n', 'utf-8'))

        if y_axis > 0.5 and lastY <= 0.5:
            print("KEYDOWN, down")
            ser.write(bytes('274,d\n', 'utf-8'))
        elif y_axis <= 0.5 and lastY > 0.5:
            print("KEYUP, down")
            ser.write(bytes('274,u\n', 'utf-8'))
        elif y_axis < -0.5 and lastY >= -0.5:
            print("KEYDOWN, up")
            ser.write(bytes('273,d\n', 'utf-8'))
        elif y_axis >= -0.5 and lastY < -0.5:
            print("KEYUP, up")
            ser.write(bytes('273,u\n', 'utf-8'))

        clock.tick(20)

        lastX = x_axis
        lastY = y_axis

    pygame.quit()