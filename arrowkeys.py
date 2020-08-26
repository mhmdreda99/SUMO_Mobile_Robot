import sys
import pygame
import serial
from serial import SerialException
import serial.tools.list_ports

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))

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
    print('Use arrow keys to control robot')

    # Send keydown and keyup events over serial connection
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                ser.write(bytes(str(event.key) + ',' + 'd' + '\n', 'utf-8'))
            elif event.type == pygame.KEYUP:
                ser.write(bytes(str(event.key) + ',' + 'u' + '\n', 'utf-8'))
