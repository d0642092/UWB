import cv2
import zmq
import pickle
import base64
import time
context = zmq.Context()
camera = cv2.VideoCapture(0)  # init the camera
camera.set(3, 1280);
camera.set(4, 720);
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
def start(ip):
    footage_socket = context.socket(zmq.PUB)
    footage_socket.bind('tcp://'+ip+':5555')
    while True:
        try:
            grabbed, frame = camera.read()  # grab the current frame
            cv2.imshow("image", frame)
            cv2.waitKey(1)
            encoded, buffer = cv2.imencode('.jpg', frame, encode_param)
            data = base64.b64encode(buffer)
            footage_socket.send_pyobj(data)
        except KeyboardInterrupt:
            camera.release()
            cv2.destroyAllWindows()
            print ("\n\nBye bye\n")
            break