
import zmq
import numpy as np
import base64
import cv2

from Program.Car.past_code.SenpaiWork.Control import zmqserver
import threading
from pynput import keyboard


# command_ip = '10.22.26.212:55688'
# cam_ip = '10.22.26.212:5555'
command_ip = '192.168.8.104:55688'
cam_ip = '192.168.8.104:5555'
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://"+command_ip)

    

def t_zmqcamserver(ip):
    zmqserver.start(ip)

def send_command(cd):
    socket.send(cd)
    print('send')
    print(socket.recv())

def on_press(key):
    key = key.char
    if key == "w":
        send_command(b'\xFA\x01\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
        print('W')
    elif key == "s":
        send_command(b'\xFA\x02\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
        print('S')
    elif key == "a":
        send_command(b'\xFA\x03\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
        print('A')
    elif key == "d":
        send_command(b'\xFA\x04\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
        print('D')
    elif key == "q":
        send_command(b'\xFA\x05\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
        print('q')
    elif key == "e":
        send_command(b'\xFA\x06\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
        print('e')
    else:
        print('wrong key')

def keytest():
    with keyboard.Listener(
        on_press=on_press) as listener:
        listener.join() 

kt = threading.Thread(target = keytest)

t_cam = threading.Thread(target = t_zmqcamserver,args = (cam_ip,))

if __name__ == "__main__":
    t_cam.start()
    print('cam start')
    kt.start()
    print('key start')
    t_cam.join()
    pass


