'''
此程式用來檢測目前電腦上的所有序列埠..>就是指你的usb接了什麼啦
'''
import serial.tools.list_ports


port_list = list(serial.tools.list_ports.comports())
if len(port_list) == 0:
   print('找不到串口')
else:
    for i in range(0,len(port_list)):
        print(port_list[i])