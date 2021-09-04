import os
import cv2
from os import path
from fnmatch import fnmatch
from PIL import Image,ImageTk
from tkinter import *
from get_encodings import get_pickel_encoding
import PIL
import keyboard
def take_pictures(pathh):
    global path
    path=pathh
    
    def adjustWindow(take_pic):
        w = 1000
        h = 700
        ws = take_pic.winfo_screenwidth()
        hs = take_pic.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        take_pic.geometry('%dx%d+%d+%d' % (w,h,x,y))
        take_pic.resizable(False,False)

    
    def save_at_dir(img,count):
        cv2.imwrite(path + '/out'+str(count) + ".jpg", img)
        count += 1
        return count

    def display_gui():
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #Remove cv2.CAP_DSHOW if you get error
        cap.set(3, 640) # set video width
        cap.set(4, 480) # set video height
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        count = 0
        while True:
            ret, img = cap.read()
            #img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5,minSize=(100,100))
            for (x,y,w,h) in faces:
                #count+=1
                print(faces)
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                cv2.imwrite(path+ '/out'+ str(count) + ".jpg", img[y:y+h,x:x+w])
                #if keyboard.is_pressed('s'):
                    #cv2.imwrite(path+ '/in'+ str(count) + ".jpg", img[y:y+h,x:x+w])
                count+=1
                 #   count=save_at_dir(img[y:y+h,x:x+w],count)
                
                # Save the captured image into the datasets folder
            #img = PIL.Image.fromarray(img)
            #imgtk = ImageTk.PhotoImage(image=img)
            #lmain.imgtk = imgtk
            #lmain.configure(image=imgtk)
            #Button(take_pic, text='Capture', width=20, font=("Open Sans", 13, 'bold'), bg='brown', fg='white',command= lambda: save_at_dir(img)).place(x=500, y=460)
            cv2.imshow('imagenew', img)
            
            if count >= 5: # Take 5 face sample and stop video
                break
        
        cap.release()
        cv2.destroyAllWindows()
        #lmain.after(10,display_gui)

    #lmain = Label(take_pic)
    #lmain.pack()
    display_gui()
    get_pickel_encoding()