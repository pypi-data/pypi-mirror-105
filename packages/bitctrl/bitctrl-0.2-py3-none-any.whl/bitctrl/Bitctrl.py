#I have never made a module before, so if you got any advice feel free to tell me.

#IMPORTANT:
#TO USE THIS WITH MICROBIT, YOUR MICROBIT WILL HAVE TO TURN THIS PYTHON SCRIPT INTO A .hex FILE AND INSTALL IT ON TO YOUR MICROBIT:

# serial.redirect_to_usb()
# def on_forever():
#     if input.button_is_pressed(Button.AB):
#         while input.button_is_pressed(Button.AB):
#             serial.write_line("A")
#             pause(15)
#     if input.button_is_pressed(Button.A):
#         while input.button_is_pressed(Button.A):
#             serial.write_line("A")
#             pause(15)
#     if input.button_is_pressed(Button.B):
#         while input.button_is_pressed(Button.B):
#             serial.write_line("B")
#             pause(15)
# forever(on_forever)
#If you plan on using this in pygame, your milliseconds in "pause" should be half of that number,
#and then half of that number; so if you have 60 fps in pygame, you divide that by two, so 30, then divide
#30 by two, which is 15 - hence why I have it pausing for 15 milliseconds

import serial
import keyboard
import time

#When bitctrl returns something, like 'B', it sends back the string 'B' which you can use for other stuff in your main script(s). Example:
# from bitctrl import Bitctrl
# while True:
#     bitctrl = Bitctrl.bitctrl('a','b','c')
#     if bitctrl == 'B':
#         print("epic")

#Get ports
s_inst = serial.Serial()
#The microbit's baudrate
s_inst.baudrate = 115200
s_inst.port ='COM3'
s_inst.open()


def bitctrl(buttonA,buttonB,buttonAB,keyboard_press=True):
    #'while True:' remove if you want to use in pygame, basically if you want to use it in another while loop. If you wish to always listen, then remove the comment from while True:
    #but be sure not to use it inside of another while loop, or loop then. Because it will stop all other code from running, so it is best to have it commented out, and implement that function
    #in your own script, like the example shown above.
        if s_inst.in_waiting:
            packet = s_inst.readline().decode('utf')
            if packet.strip() == 'AB':
                if keyboard_press:
                    keyboard.press_and_release(buttonAB)
                return 'AB'
            if packet.strip() == 'A':
                if keyboard_press:
                    keyboard.press_and_release(buttonA)
                return 'A'
            if packet.strip() == 'B':
                if keyboard_press == True:
                    keyboard.press_and_release(buttonB)
                return 'B'

def _bit_tilt(UP,DOWN,RIGHT,LEFT):
    if s_inst.in_waiting:
        packet = s_inst.readline().decode('utf')
        #Checks if the packet sent contains "ROLL". Roll is basically "tilting left or right", if I used 'PITCH' in the .hex file, it wouldn't have optimal numbers.
        if 'ROLL' in packet.strip():
            #Splits the packet
            split_packet = packet.strip().split()
            num_packet = split_packet[0]
            if int(num_packet) >= 38:
                #print(f'tilting right{num_packet}')
                return RIGHT
            if int(num_packet) <= -45:
                #print(f'tilting left{num_packet}')
                return LEFT
        if 'PITCH' in packet.strip():
            split_packet = packet.strip().split()
            num_packet = split_packet[0]
            if int(num_packet) >= 70:
                #print(f"tilting down {num_packet}")
                return DOWN
            if int(num_packet) <= 40:
                # print(f'tilting up{num_packet}')
                return UP
