import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import pandas as pd
import datetime
import os

# -----------------------------
# Setup
# -----------------------------

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

attendance_file = "attendance.csv"

# create file if not exists
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv(attendance_file, index=False)


# -----------------------------
# Capture Attendance
# -----------------------------

def take_attendance():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

            name = name_entry.get()

            if name == "":
                cv2.putText(frame,"Enter Name First",(20,40),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            else:

                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")

                df = pd.read_csv(attendance_file)
                new_row = {"Name":name,"Date":date,"Time":time}

                df = pd.concat([df,pd.DataFrame([new_row])])
                df.to_csv(attendance_file,index=False)

                tree.insert("",0,values=(name,date,time))

                cv2.putText(frame,"Attendance Marked",(20,40),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

        cv2.imshow("Camera",frame)

        if cv2.waitKey(1)==27:
            break

    cap.release()
    cv2.destroyAllWindows()



def load_attendance():

    df = pd.read_csv(attendance_file)

    for i in tree.get_children():
        tree.delete(i)

    for index,row in df.iterrows():
        tree.insert("",0,values=(row["Name"],row["Date"],row["Time"]))




root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("900x600")
root.configure(bg="#1e1e2f")

title = tk.Label(root,
                 text="Smart Attendance Register",
                 font=("Segoe UI",24,"bold"),
                 bg="#1e1e2f",
                 fg="white")
title.pack(pady=20)

frame = tk.Frame(root,bg="#1e1e2f")
frame.pack()

name_label = tk.Label(frame,text="Student Name",
                      font=("Segoe UI",12),
                      bg="#1e1e2f",
                      fg="white")

name_label.grid(row=0,column=0,padx=10,pady=10)

name_entry = tk.Entry(frame,font=("Segoe UI",12),width=30)
name_entry.grid(row=0,column=1,padx=10,pady=10)


btn1 = tk.Button(root,
                 text="Start Camera Attendance",
                 font=("Segoe UI",12,"bold"),
                 bg="#4CAF50",
                 fg="white",
                 command=take_attendance)

btn1.pack(pady=10)


btn2 = tk.Button(root,
                 text="Load Attendance",
                 font=("Segoe UI",12,"bold"),
                 bg="#2196F3",
                 fg="white",
                 command=load_attendance)

btn2.pack(pady=10)



columns=("Name","Date","Time")

tree = ttk.Treeview(root,columns=columns,show="headings",height=15)

for col in columns:
    tree.heading(col,text=col)
    tree.column(col,width=200)

tree.pack(pady=20)

root.mainloop()