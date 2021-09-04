import cv2 
import numpy as np
from architecture import *
import get_encodings
#normalize,l2_normalizer
from PIL import Image,ImageTk
from sklearn.preprocessing import Normalizer

from tkinter import *
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import PIL
from datetime import datetime
def recognise(root):
    #a=get_encodings.get_pickel_encoding()
    def record_attendance(idd):
        #if os.path.isfile('student_attendance.csv'):
        df=pd.read_csv('student_attendance.csv')
        s=datetime.now()
        date=str(s.day) +'-' + str(s.month) 
            #+ ' ' + str(s.hour) + ':'+ str(s.minute)
        if idd in df['Name'].values:
            loc=df.loc[df['Name']==idd].index.item()
            if date not in df.columns:    
                df[date]='A'
            df[date][loc]='P'
       
            df.to_csv('student_attendance.csv',index=False)

        else:
            pass        
        
    
          
    def display():
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        face_encoder = InceptionResNetV2()
        path = "facenet_keras_weights.h5"
        face_encoder.load_weights(path)
        encodings_path = 'encodings.pkl'
        
        def normalize(img):
            mean, std = img.mean(), img.std()
            return (img - mean) / std
        
        def load_pickle(path):
            with open(path, 'rb') as f:
                encoding_dict = pickle.load(f)
            return encoding_dict
    
        encoding_dict = load_pickle(encodings_path)
    
    
    
        def get_encode(face_encoder, face, size):
            face = normalize(face)
            face = cv2.resize(face, size)
            encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
            return encode
    
    
    
        def detect(img ,encoder,encoding_dict):
            required_size = (160,160)
            encode = get_encode(encoder, img, required_size)
            l2_normalizer = Normalizer('l2')

            encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
            name = 'unknown'
        
            distance = float("inf")
            for db_name, db_encode in encoding_dict.items():
                dist = cosine(db_encode, encode)
                if dist < distance and dist<0.8:
                    name = db_name
                    distance = dist
            return name
        
        cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #cam = cv2.VideoCapture(0) Use this if camera doesn't work properly and comment above line using #
        cam.set(3, 640) 
        cam.set(4, 480)
        while True:
            ret, img =cam.read()
            
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale( 
                    gray,
                    scaleFactor = 1.1,
                    minNeighbors = 5,
                    minSize = (200,200),
                   )
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                face=img[y:y+h,x:x+w]
                name= detect(face , face_encoder , encoding_dict)
                #record_attendance(name)
                cv2.putText(img, str(name), (x+5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                cv2.putText(img, 'Press Esc to Exit', (0,0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            #img = PIL.Image.fromarray(img)
            #imgtk = ImageTk.PhotoImage(image=img)
            #lmain.imgtk = imgtk
            #lmain.configure(image=imgtk)
            
            cv2.imshow('camera',img) 
            
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                cam.release()
                cv2.destroyAllWindows()
                break
        #lmain.after(10,display)
        
    #lmain# = Label(root)
    #lmain.pack()    
        
    #cv2.imshow('camera',img) 
    display()


