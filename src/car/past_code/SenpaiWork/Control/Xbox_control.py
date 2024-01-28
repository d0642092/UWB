import zmq
# import numpy as np
# import base64
# import cv2
import pygame
from Program.Car.past_code.SenpaiWork.Control import zmqserver
import time
import threading
from pynput import keyboard

# command_ip = '10.22.26.212:55688'
# cam_ip = '10.22.26.212:5555'
command_ip = '192.168.8.104:55688'
cam_ip = '192.168.8.104:5555'
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://" + command_ip)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

def t_zmqcamserver(ip):
    zmqserver.start(ip)


def send_command(cd):
    socket.send(cd)
    print('send')
    print(socket.recv())


def on_press():
    try:
        pygame.init()

        # Set the width and height of the screen [width,height]
        size = [500, 700]
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("My Game")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # Initialize the joysticks
        pygame.joystick.init()

        # Get ready to print
        textPrint = TextPrint()

        while done == False:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
            joystick_count = pygame.joystick.get_count()

            screen.fill(WHITE)
            textPrint.reset()

            textPrint.indent()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                hats = joystick.get_numhats()
                textPrint.print(screen, "Number of hats: {}".format(hats))
                textPrint.indent()
                for i in range(hats):
                    hat = joystick.get_hat(i)
                    textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
                    if hat == (1, 0):
                        print("FX right")
                        send_command(b'\xFA\x04\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
                    if hat == (-1, 0):
                        print("FX left")
                        send_command(b'\xFA\x03\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
                    if hat == (0, 1):
                        print("FX up")
                        send_command(b'\xFA\x01\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
                    if hat == (0, -1):
                        print("FX down")
                        send_command(b'\xFA\x02\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')



                textPrint.unindent()

                textPrint.unindent()

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # Limit to 20 frames per second
            clock.tick(5)
    except Exception:

        pygame.quit()

# key = key.char
    # if key == "w":
    #     send_command(b'\xFA\x01\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
    #     print('W')
    # elif key == "s":
    #     send_command(b'\xFA\x02\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
    #     print('S')
    # elif key == "a":
    #     send_command(b'\xFA\x03\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
    #     print('A')
    # elif key == "d":
    #     send_command(b'\xFA\x04\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
    #     print('D')
    # elif key == "q":
    #     send_command(b'\xFA\x05\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
    #     print('q')
    # elif key == "e":
    #     send_command(b'\xFA\x06\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
    #     print('e')
    # else:
    #     print('wrong key')


def keytest():
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()


# kt = threading.Thread(target=keytest)
kt = threading.Thread(target=on_press())

t_cam = threading.Thread(target=t_zmqcamserver, args=(cam_ip,))

if __name__ == "__main__":
    t_cam.start()
    print('cam start')
    kt.start()
    print('key start')
    t_cam.join()
    pass


