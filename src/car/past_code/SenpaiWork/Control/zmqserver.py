import cv2
import zmq
import base64
import numpy as np
import pickle


def start(ip):
    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)
    footage_socket.connect('tcp://'+ip)
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    print('wait for cam data')
    while True:
        try:
            frame = footage_socket.recv_pyobj()
            img = base64.b64decode(frame)
            nparr = np.frombuffer(img, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow("image", frame)
            cv2.waitKey(1)

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            print ("\n\nBye bye\n")
            break
