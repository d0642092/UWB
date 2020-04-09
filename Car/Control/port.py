import serial
ser=serial.Serial("com5",9600,timeout=0.5)
print(ser.port)