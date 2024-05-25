import tkinter as tk
from tkinter import Message, Text
import cv2
import os
import tkinter.ttk as ttk
import tkinter.font as font
import numpy as np
from PIL import Image, ImageTk
import csv
import json
import pandas as pd
import shutil
import datetime
import time

#window = tk.Tk()
#window.title("Login/Logout Website")
#window.geometry('1366x768')


# Login Credentials

# Loading Data from txt file
def loading_data():
    file = open('C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\data.txt', 'r', encoding='utf-8')
    data = json.load(file)
    file.close()
    return data


# Saving Data to .txt file
def saving_data(data):
    file = open('C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\data.txt', 'w', encoding='utf-8')
    json.dump(data, file, ensure_ascii=False)
    file.close()


# Saving data in a variable
data = loading_data()
print(data)

def create_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("1200x520+300+100")  # Set the same dimensions as the main window

    # Load and display the image on the left side
    left_frame = tk.Frame(login_window)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

    image = Image.open("C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\\\images\\Atm.jpg")
    image = ImageTk.PhotoImage(image)

    # Create a label for the image and keep a reference to the image object
    image_label = tk.Label(left_frame, image=image)
    image_label.image = image  # Keep a reference to the image
    image_label.pack()

    # Create a frame for the login form on the right side
    right_frame = tk.Frame(login_window)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Create and configure the label for the text
    welcome_label = tk.Label(right_frame, text="Login to ATM System", font=("Helvetica", 24), fg="dark blue")
    welcome_label.pack(padx=10, pady=(20, 10))

    
    font_size = 16

    # Create labels and entry fields for Account Number and Password
    username_label = tk.Label(right_frame, text="Username:")
    username_label.pack()
    txt = tk.Entry(right_frame, font=("Helvetica", 16), width=40)
    txt.pack()

    password_label = tk.Label(right_frame, text="Password:")
    password_label.pack()
    txt2 = tk.Entry(right_frame, font=("Helvetica", 16), width=40, show="*")
    txt2.pack()

    message = tk.Label(root, text="Notification", bg="grey", fg="white", width=30, height=1, font=('times', 15, 'bold'))
    message.place(x=700, y=400)

    def login_clear():
        txt.delete(0, 'end')
        txt2.delete(0, 'end')

    def TrackImages(UserId):
        recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
        recognizer.read("C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\TrainingImageLabel\\Trainner.yml")
        harcascadePath = "C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        df = pd.read_csv("C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\Details\\Details.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX          
        run_count=0;run=True
        while run:
        
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                print(Id, conf)
                if(conf < 50):
                    aa = df.loc[df['Id'] == Id]['Name'].values
                    aa_str = "-".join(aa.astype(str))
                    tt = str(Id) + "-" + aa_str
                    if (str(Id) == UserId):
                        message.configure(text="Face Recognized Successfully")
                        run = False
                    
                else:
                    Id='Unknown'                
                    tt=str(Id)            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            run_count += 1    
            cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q') or run_count==150):
                message.configure(text="Unable to Recognise Face")
                break
    
        cam.release()
        cv2.destroyAllWindows()
    
    def login_submit():
        username = txt.get()
        password = txt2.get()

        # Check if the username exists in the data dictionary
        if username in data:
            # Check if the password matches
            if data[username] == password:
                TrackImages(username)
                
                # Add your login code here
            else:
                message.configure(text="Id and Password does not Match")
        else:
            message.configure(text="Entered Id does not Exists")

        login_clear()

# Login Actions
    login_button = tk.Button(right_frame, text="Login", width=15, height=2, font=("Helvetica", 16), bg="green",command=login_submit)
    login_button.pack(pady=(20, 10))

    cancel_button = tk.Button(right_frame, text="Cancel", width=15, height=2, font=("Helvetica", 16), bg="gray", command=login_window.destroy)
    cancel_button.pack(pady=(0, 10))     

def register():
    # Load an image to display on the left side
    image = Image.open("C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\images\\Atm.jpg")
    image = ImageTk.PhotoImage(image)

    # Open a new registration window
    registration_window = tk.Toplevel(root)
    registration_window.title("Registration")
    registration_window.geometry("1200x520+300+100")

    # Create a frame for the image on the left side
    left_frame = tk.Frame(registration_window)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

    image_label = tk.Label(left_frame)
    image_label.pack()
    image_label.img = image
    image_label.configure(image=image)

    # Create a frame for the registration form on the right side
    right_frame = tk.Frame(registration_window)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Create a form for user registration
    # Entry fields will expand to fill the available space
    name_label = tk.Label(right_frame, text="Name:")
    name_label.pack()
    global name_entry
    name_entry = tk.Entry(right_frame, font=("Helvetica", 16), width=40)
    name_entry.pack()

    mobile_label = tk.Label(right_frame, text="Mobile:")
    mobile_label.pack()
    global mobile_entry
    mobile_entry = tk.Entry(right_frame, font=("Helvetica", 16), width=40)
    mobile_entry.pack()

    Acc_no = tk.Label(right_frame, text="Account No:")
    Acc_no.pack()
    global Acc_entry
    Acc_entry = tk.Entry(right_frame, font=("Helvetica", 16), width=40, show="*")  # Mask the PIN
    Acc_entry.pack()

    username_label = tk.Label(right_frame, text="Username:")
    username_label.pack()
    global username_entry
    txt3 = tk.Entry(right_frame, font=("Helvetica", 16), width=40)
    txt3.pack()

    password_label = tk.Label(right_frame, text="Password:")
    password_label.pack()
    global password_entry
    txt4 = tk.Entry(right_frame, font=("Helvetica", 16), width=40, show="*")  # Mask the password
    txt4.pack()

    msg_label = tk.Label(root, text="Notification: ", bg='grey', fg='white', width=10, height=1, font=('times', 15, 'bold'))
    msg_label.place(x=350, y=500)
    message = tk.Label(root, text="", bg="Grey", fg="white", width=30, height=1, font=('times', 15, 'bold'))
    message.place(x=500, y=500)

    


# Main

    def reg_clear():
        txt3.delete(0, 'end')
        txt4.delete(0, 'end')


# Login_Functions



# Register_Functions

    def TakeImages():
        Id = (txt3.get())
        name = (txt4.get())
        phone = (mobile_entry.get())
        ret = 0
        if Id not in data:
            cam = cv2.VideoCapture(0)
            harcascadePath = "C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(
                        "C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\TrainingImage\\ " + name + '.' + Id + '.' + str(
                            sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    cv2.imshow('frame', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID: " + Id + " Name: " + name 
            row = [Id, name, phone]
            with open(
                'C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\Details\\Details.csv',
                'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text=res)
            ret = 1
        else:
            res = "Username Already Exists...Try another one!!!"
            message.configure(text=res)
        return ret

# Training Images

    def TrainImages():
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, Id = getImagesAndLabels(
            "C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save(
            "C:\\Users\\SIDDHI\\Desktop\\Security\\login-verification-master\\TrainingImageLabel\\Trainner.yml")
        res = "Registration Successful"
        message.configure(text=res)
        return True

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imagePath in imagePaths:
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)
        return faces, Ids

    def reg_submit():
        Userid = txt3.get()
        if Userid.isdigit():
            if TakeImages() == 1:
                if TrainImages():
                    data[txt3.get()] = txt4.get()
                    saving_data(data)
                else:
                    pass
        else:
            message.configure(text="User Id Should contain numbers only!!!")
        reg_clear()
        print(data)




# Register Actions
    submit_button = tk.Button(right_frame, text="Submit", width=15, height=2, font=("Helvetica", 16), bg="green", command=reg_submit)
    submit_button.pack(pady=(20, 10))
    
    # Create a Try Again button
    try_again_button = tk.Button(right_frame, text="Try Again", width=15, height=2, font=("Helvetica", 16), bg="gray", command=registration_window.destroy)
    try_again_button.pack(pady=(0, 10))


    
# Create the main window
root = tk.Tk()
root.title("ATM Security System")
root.geometry("1200x520+300+100")  # Set the main window size and position

# Create a frame for the image on the left side
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

# Load and display the image
image = Image.open("C:\\Users\\SIDDHI\\Desktop\\ATM_security - Copy\\ATM_security\\images\\Atm.jpg")
image = ImageTk.PhotoImage(image)
image_label = tk.Label(left_frame, image=image)
image_label.pack()

# Create a frame for the right side
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Create and configure the label for the text
welcome_label = tk.Label(right_frame, text="Welcome to ATM System", font=("Helvetica", 24), fg="dark blue")
welcome_label.pack(padx=10, pady=(20, 10))

font_size = 16
login_button = tk.Button(right_frame, text="Login", width=15, height=2, font=("Helvetica", font_size), pady=10, bg="green")
login_button.pack(pady=(0, 10))

register_button = tk.Button(right_frame, text="Register", width=15, height=2, font=("Helvetica", font_size), pady=10, bg="gray")
register_button.pack(pady=(0, 10))

# Set the "Register" button command
register_button.config(command=register)
login_button.config(command=create_login_window)

root.mainloop()
