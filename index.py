from PIL import Image,ImageTk
from tkinter import *
import tkinter as tk
import cv2
import numpy as np
import PIL
from recognise_faces import recognise
import tkinter.messagebox as tm
import csv
import pandas as pd
global root
import os
from os import path
from add_pictures import take_pictures
def adjustWindow(window):
    w = 1000
    h = 700
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w,h,x,y))
    window.resizable(False,False)

def display_attendance(df):
    dis_att = Tk()
    dis_att.geometry('580x250')
    txt = Text(dis_att) 
    txt.pack() 
    class PrintToTXT(object): 
        def write(self, s): 
            txt.insert(END, s)
            return
    sys.stdout = PrintToTXT()
    print('Attendance for:',df['Name'])
    print (df)
    dis_att.mainloop()
    
def validate():
    view_att.destroy()
    df=pd.read_csv('student_attendance.csv')
    id_given=idd.get()
    pin_given=pin.get()
    pin_main=df[df['ID']==id_given]['Pincode'].values
    if (pin_main == pin_given):
        d=df.loc[df['ID'] == id_given]        
        display_attendance(d)
    
    
            
def view_attendance():
    global idd,pin,view_att
    view_att = Tk()
    view_att.title("View Attendance")
    adjustWindow(view_att)
    idd = IntVar(view_att)
    pin = StringVar(view_att)
    
    Label(view_att, text="", bg='light blue', width='150', height='80').place(x=0, y=0)
    Label(view_att, text="ID", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue',anchor=W).place(x=130, y=160)
    ids=Entry(view_att, textvariable=idd).place(x=300, y=160)
    Label(view_att, text="Pincode", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue', anchor=W).place(x=130, y=280)
    pincode=Entry(view_att, textvariable=pin).place(x=300, y=280)
    Button(view_att, text='Submit', width=20, font=("Open Sans", 13, 'bold'), bg='brown', fg='white',command=validate).place(x=500, y=460)
    view_att.mainloop()
    
    
def add_in_csv():
    new_entry.destroy()
    with open('student_attendance.csv', 'a', newline='') as f:
        field=[ "ID", "Name","Pincode"]
        writer = csv.DictWriter(f, fieldnames=field)
        if os.stat('student_attendance.csv').st_size == 0:
            writer.writeheader()
        writer.writerow({"ID":id_new.get(), "Name":name_new.get(), "Pincode":pincode_new.get()})
        #messagebox.showinfo("Success", "Successfully added to CSV file")
    df=pd.read_csv('student_attendance.csv')
    df.to_csv('student_attendance.csv',na_rep='NA',index = False)
    messagebox.showinfo("Success", "Successfully added to CSV file")
    if not path.exists('Dataset'):
        os.mkdir('Dataset')
    if not path.exists('Dataset/'+name_new.get()):
        os.mkdir('Dataset/'+name_new.get())
        take_pictures('Dataset/'+name_new.get())

     
            
def new_student():
    global id_new,name_new,pincode_new,new_entry
    new_entry = Tk()
    new_entry.title("New Entry")
    adjustWindow(new_entry)
    id_new = IntVar(new_entry)
    name_new = StringVar(new_entry)
    pincode_new = StringVar(new_entry)
    
    Label(new_entry, text="", bg='light blue', width='150', height='80').place(x=0, y=0)
    Label(new_entry, text="ID", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue',anchor=W).place(x=130, y=160)
    idd=Entry(new_entry, textvariable=id_new).place(x=300, y=160)
    Label(new_entry, text="Name", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue', anchor=W).place(x=130, y=220)
    name=Entry(new_entry, textvariable=name_new).place(x=300, y=220)
    Label(new_entry, text="Pincode", font=("Open Sans", 11, 'bold'), fg='black', bg='light blue', anchor=W).place(x=130, y=280)
    pincode=Entry(new_entry, textvariable=pincode_new).place(x=300, y=280)
    Button(new_entry, text='Take Picture', width=20, font=("Open Sans", 13, 'bold'), bg='brown', fg='white',command=add_in_csv).place(x=500, y=460)
    new_entry.mainloop()
    
root = Tk()
root.title("Welcome")

adjustWindow(root)

    
Label(root, text="", bg='light blue', width='1000', height='800').place(x=0, y=0)
Label(root, text="Attendance System", width='50', height="2", font=("Calibri", 30,'bold'), fg='white', bg='purple', anchor = CENTER).place(x=0, y=0)
Button(root, text='Add new record', width=17, font=("Open Sans", 15, 'bold'), bg='blue', fg='white',  command = new_student).place(x=80, y=550)
Button(root, text='View Attendance', width=17, font=("Open Sans", 15, 'bold'), bg='blue', fg='white',  command = view_attendance).place(x=380, y=550)
Button(root, text='Take Attendance', width=17, font=("Open Sans", 15, 'bold'), bg='blue', fg='white',  command = lambda: recognise(root)).place(x=680, y=550)

root.mainloop()


