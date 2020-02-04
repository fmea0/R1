import seleccionador as tp
import cv2
import tensorflow as tf
import numpy as np
import argparse
import time
import math
import urllib.request
import serial, time


url = 'http://192.168.43.1:8080/shot.jpg'
arduino = serial.Serial("COM9", 9600)#cambiar el com al correcto

tp.init(0.7,"E:/robotica/frozen_inference_graph.pb")#usa el modelo con 70%de tope, cambiar el lugar del archivo frozen-inference
rawString = arduino.readline()
time.sleep(2)
imgResp = urllib.request.urlopen(url)
imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
img = cv2.imdecode(imgNp,-1)


cam=cv2.VideoCapture(url)
if(cam.isOpened()):
    cv2.imshow('test',img)
    print("camara")
    _,frame=cam.read()
    print(rawString)
    time.sleep(2)
    if  (rawString == b'8\r\n'):
        print(rawString)
        for i in range(10):
            rois,rects,cls,error=tp.get_body_cropped(frame)
            if(len(cls)==1):
                arduino.write(b'1') #pasa a arduino en bytes el valor de code(1,2,3,4,5,6), realmente no se si pasa solo c
                time.sleep(2)
            elif(len(cls)==2):
                arduino.write(b'2') #pasa a arduino en bytes el valor de code(1,2,3,4,5,6), realmente no se si pasa solo c
                time.sleep(2)
            elif(len(cls)==3):
                arduino.write(b'3') #pasa a arduino en bytes el valor de code(1,2,3,4,5,6), realmente no se si pasa solo c
                time.sleep(2)
            elif(len(cls)==4):
                arduino.write(b'4') #pasa a arduino en bytes el valor de code(1,2,3,4,5,6), realmente no se si pasa solo c
                time.sleep(2)
                arduino.close()#cierra el puerto serial

                #rawString='0' #intento de resetear esta variable
            else:
                print("lo que recibe dela clase es: ")#en caso de no dectectar nada
                print(cls)#muestra la clas

cam.release()
cv2.destroyAllWindows()
