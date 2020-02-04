from transform import four_point_transform
import seleccionador as tp
import cv2
import numpy as np
import argparse
import time
import math
import urllib.request
import serial, time
arduino = serial.Serial("COM8", 9600)#cambiar el com al correcto


tp.init(0.7,"C:/Users/sarig/Desktop/frozen_inference_graph.pb")#usa el modelo con 70% del modelo creado, poner la direccion de la ubicacion de frozen_inference 
cam=cv2.VideoCapture(0)
#url = 'http://192.168.0.40:8080/shot.jpg'
if(cam.isOpened()):

    # Capture frame-by-frame
    #imgResp = urllib.request.urlopen(url)
    #imgNp = np.array(bytearray(imgResp.read()),dtype = np.uint8)
    #frame = cv2.imdecode(imgNp,-1)
    #cv2.imshow('test',frame)

   
    for i in range(10):
        rois,rects,cls,error=tp.get_body_cropped(frame)#cls es etiqueta (unica cosa que nos interesa)
        print("inferencia")#en caso de no detectar nada imprimira inferencia en notepad
        if(len(cls)>0):
            code=cls[0]
            print(code)#imprime en notepad
            time.sleep(2)   #tiempo extra
            arduino.write(b'code') #pasa a arduino en bytes el valor de code(1,2,3,4,5,6)
            arduino.close()#cierra el puerto serial

	
	
if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
