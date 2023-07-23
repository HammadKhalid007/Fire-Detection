import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDialog, QMessageBox
import pyrebase
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel, QVBoxLayout
import imutils
import time
import numpy as np
import cv2,os,time
import pyshine as ps
from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import winsound
import torch
import firebase_admin
from firebase_admin import credentials, storage, auth, db
import firestore
from google.cloud import firestore
import smtplib
import ssl
from email.message import EmailMessage





cred = credentials.Certificate('serviceaccount.json')
config ={

}

firebase_admin.initialize_app(cred, config)
firebase = pyrebase.initialize_app(config)
db2 = firebase.database()
# authen = firebase.auth()
bucket = storage.bucket()
db1 = firebase_admin.db.reference('admins')


class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        V = app.desktop().screenGeometry()
        h = V.height()
        w = V.width()
        widget.setGeometry(500, 250, 800, 522)
        # widget.setMaximumWidth(w-1120)
        # widget.setMaximumHeight(h-558)
        widget.setWindowTitle("Fire Detection")
        loadUi("login.ui",self)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.userName.text()
        password = self.Password.text()
        if len(user) == 0 or len(password) == 0:
            self.label_2.setText("Enter All Fields!")
        else:
            try:
                # retrieve the user's email and password from the database
                user_data = db2.child("admins").order_by_child("email_password").equal_to(user + "_" + password).get()
                print(user_data.val())
                if len(user_data.val()) == 0:
                    self.label_2.setText("User not found!")
                    return False
                user_password = list(user_data.val().values())[0]["password"]
                print(user_password)

                main = Home()
                widget.addWidget(main)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                print("Login successfully!")
                return True

            except Exception as e:
                print(e)
                self.label_2.setText("Error authenticating user!")


class Home(QMainWindow):
    def __init__(self):
        super(Home, self).__init__()
        loadUi("home01.ui", self)
        V = app.desktop().screenGeometry()
        h = V.height()
        w = V.width()
        widget.setGeometry(0, 25, w, h-25)
        # widget.setMaximumWidth(w)
        # widget.setMaximumHeight(h-25)
        widget.setWindowTitle("Fire Detection")
        self.statusButton_3.clicked.connect(self.loginscreen)
        self.statusButton.clicked.connect(self.emergency)
        self.statusButton_2.clicked.connect(self.switch_to_main)
        self.comboBox.activated.connect(self.clicker)

    def clicker(self):
        a = self.comboBox.currentText()
        print(a)
        if a == "1":
            self.camer1()
        if a == "2":
            self.camer2()
        if a == "3":
            self.camer3()
        if a == "4":
            self.camer4()

    def camer1(self):
        cam = camera1()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height + 10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def camer2(self):
        cam = camera2()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height + 10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def camer3(self):
        cam = camera3()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height + 10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def camer4(self):
        cam = camera4()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height + 10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def emergency(self):
        emer = emergency_dialog()
        widget2.addWidget(emer)
        widget2.setFixedWidth(600)
        widget2.setFixedHeight(400)
        widget2.setCurrentIndex(widget2.currentIndex() + 1)
        widget2.show()

    def loginscreen(self):
        self.playing = False
        log = LoginScreen()
        widget.addWidget(log)
        widget.setFixedHeight(522)
        widget.setFixedWidth(800)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def alert1(self):
        a = alert()
        b.addWidget(a)
        b.setFixedWidth(600)
        b.setFixedHeight(400)
        b.setCurrentIndex(b.currentIndex() + 1)
        b.show()

    def switch_to_main(self):
        self.hide()
        # Hide the home screen
        main = mainscreen()
        # widget.addWidget(main)
        # V = app.desktop().screenGeometry()
        # h = V.height()
        # w = V.width()
        # widget.setGeometry(0, 25, w, h-25)
        # widget.setMaximumWidth(w)
        # widget.setMaximumHeight(h-25)
        #         widget.setCurrentIndex(widget.currentIndex() + 1)
        main.setGeometry(0,25,1920,1080)
        # main.setMaximumWidth(1920)
        # main.setMaximumHeight(1080-25)
        main.show()  # Show the main screen
        main.start_video()  # Automatically start the video


class mainscreen(QMainWindow):
    def __init__(self):
        super(mainscreen, self).__init__()
        loadUi("main_screen.ui", self)
        V = app.desktop().screenGeometry()
        h = V.height()
        w = V.width()
        widget.setGeometry(0, 25, w, h - 25)
        widget.setMaximumWidth(w)
        widget.setMaximumHeight(h - 25)
        widget.setWindowTitle("Fire Detection")
        self.statusButton_3.clicked.connect(self.loginscreen)
        self.statusButton.clicked.connect(self.emergency)
        self.statusButton_2.clicked.connect(self.home)
        self.comboBox.activated.connect(self.clicker)
        self.playing = False
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', r'best.pt')
        self.cap = cv2.VideoCapture(0)
        self.cap1 = cv2.VideoCapture(1)
        self.cap3 = cv2.VideoCapture(0)
        self.cap4 = cv2.VideoCapture(1)
        # self.cap = cv2.VideoCapture('test.mp4')
        # self.cap1 = cv2.VideoCapture('fire3.mp4')
        # self.cap3 = cv2.VideoCapture('test.mp4')
        # self.cap4 = cv2.VideoCapture('fire3.mp4')

    def start_video(self):
        self.playing = True
        self.play_video()

    def play_video(self):
        timer = 0
        timer1 = 0
        timer2 = 0
        timer3 = 0
        count = 0
        while self.playing:
            ret, frame = self.cap.read()
            img1, image1 = self.cap1.read()
            # img2, image2 = self.cap3.read()
            # img3, image3 = self.cap4.read()
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            print("fps: ", fps)


            if ret:
                count += 1
                if count % 5 != 0:
                    continue

                #detection for camera 1
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                # Get the predictions
                results = self.model(img)

                # Extract the bounding boxes and labels
                boxes = results.xyxy[0].tolist()
                labels = results.names[0]
                scores = results.xyxy[0][:, 4].tolist()

                # Set the confidence threshold
                confidence_threshold = 0.32

                # Filter predictions based on confidence score
                filtered_boxes = []
                filtered_labels = []
                for box, score in zip(boxes, scores):
                    if score > confidence_threshold:
                        filtered_boxes.append(box)
                        filtered_labels.append(labels[int(box[5])])

                # Draw the bounding boxes and labels
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("arial.ttf", 20)
                for box, label in zip(filtered_boxes, filtered_labels):
                    xmin, ymin, xmax, ymax, confidence, _ = box
                    label_text = f"{label} {confidence:.2f}"
                    draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=3)
                    draw.text((xmin, ymin - 20), label_text, font=font, fill="red")

                # Convert the PIL Image back to OpenCV format
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)



                #detection for camera 2
                image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
                img1 = Image.fromarray(image1)
                # Get the predictions
                results1 = self.model(img1)

                # Extract the bounding boxes and labels
                boxes1 = results1.xyxy[0].tolist()
                labels1 = results1.names[0]
                scores1 = results1.xyxy[0][:, 4].tolist()

                # Set the confidence threshold
                confidence_threshold = 0.32
                # Filter predictions based on confidence score
                filtered_boxes1 = []
                filtered_labels1 = []
                for box1, score1 in zip(boxes1, scores1):
                    if score1 > confidence_threshold:
                        filtered_boxes1.append(box1)
                        filtered_labels1.append(labels1[int(box1[5])])

                # Draw the bounding boxes and labels
                draw1 = ImageDraw.Draw(img1)
                font1 = ImageFont.truetype("arial.ttf", 20)
                for box1, label1 in zip(filtered_boxes1, filtered_labels1):
                    xmin1, ymin1, xmax1, ymax1, confidence1, _1 = box1
                    label_text1 = f"{label1} {confidence1:.2f}"
                    draw1.rectangle([(xmin1, ymin1), (xmax1, ymax1)], outline="red", width=3)
                    draw1.text((xmin1, ymin1 - 20), label_text1, font1=font1, fill="red")

                # Convert the PIL Image back to OpenCV format
                image1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)


                #detection for camera 3
                image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                img2 = Image.fromarray(image2)
                # Get the predictions
                results2 = self.model(img2)
                
                # Extract the bounding boxes and labels
                boxes2 = results2.xyxy[0].tolist()
                labels2 = results2.names[0]
                scores2 = results2.xyxy[0][:, 4].tolist()
                
                # Set the confidence threshold
                confidence_threshold = 0.32
                # Filter predictions based on confidence score
                filtered_boxes2 = []
                filtered_labels2 = []
                for box2, score2 in zip(boxes2, scores2):
                    if score2 > confidence_threshold:
                        filtered_boxes2.append(box2)
                        filtered_labels2.append(labels2[int(box2[5])])
                
                # Draw the bounding boxes and labels
                draw2 = ImageDraw.Draw(img2)
                font2 = ImageFont.truetype("arial.ttf", 20)
                for box2, label2 in zip(filtered_boxes2, filtered_labels2):
                    xmin2, ymin2, xmax2, ymax2, confidence2, _2 = box2
                    label_text2 = f"{label2} {confidence2:.2f}"
                    draw2.rectangle([(xmin2, ymin2), (xmax2, ymax2)], outline="red", width=3)
                    draw2.text((xmin2, ymin2 - 20), label_text2, font2=font2, fill="red")
                
                # Convert the PIL Image back to OpenCV format
                image3 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)


                #detection for camera 4
                image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2RGB)
                img3 = Image.fromarray(image3)
                # Get the predictions
                results3 = self.model(img3)
                
                # Extract the bounding boxes and labels
                boxes3 = results3.xyxy[0].tolist()
                labels3 = results3.names[0]
                scores3 = results3.xyxy[0][:, 4].tolist()
                
                # Set the confidence threshold
                confidence_threshold = 0.32
                # Filter predictions based on confidence score
                filtered_boxes3 = []
                filtered_labels3 = []
                for box3, score3 in zip(boxes3, scores3):
                    if score3 > confidence_threshold:
                        filtered_boxes3.append(box2)
                        filtered_labels3.append(labels3[int(box3[5])])
                
                # Draw the bounding boxes and labels
                draw3 = ImageDraw.Draw(img3)
                font3 = ImageFont.truetype("arial.ttf", 20)
                for box3, label3 in zip(filtered_boxes3, filtered_labels3):
                    xmin3, ymin3, xmax3, ymax3, confidence3, _3 = box3
                    label_text3 = f"{label3} {confidence3:.2f}"
                    draw3.rectangle([(xmin3, ymin3), (xmax3, ymax3)], outline="red", width=3)
                    draw3.text((xmin3, ymin3 - 20), label_text3, font3=font3, fill="red")
                
                # Convert the PIL Image back to OpenCV format
                image3 = cv2.cvtColor(np.array(img3), cv2.COLOR_RGB2BGR)




                self.displayimage(frame, 1)
                self.displayimage1(image1, 1)
                self.displayimage2(image2, 1)
                self.displayimage3(image3, 1)

                #alert camera 1
                if timer > 51:
                    timer = 0
                elif len(filtered_boxes) != 0:
                    timer = timer + 1
                    print(timer)
                    winsound.Beep(frequency=5000, duration=100)
                    if timer == 2:
                        print("Fire detected")
                        self.alert1()
                        try:
                            cv2.imwrite("fire_detected.png", frame)
                            image_blob = bucket.blob('images/image.jpg')
                            image_blob.upload_from_filename('fire_detected.png')
                            image_upload_success = True
                        except:
                            image_upload_success = False


                # alert camera 2
                if timer1 > 51:
                    timer1 = 0
                elif len(filtered_boxes1) != 0:
                    timer1 = timer1 + 1
                    print(timer1)
                    winsound.Beep(frequency=5000, duration=100)
                    if timer1 == 2:
                        print("Fire detected in camera 2")
                        self.alert1()
                        try:
                            cv2.imwrite("fire_detected1.png", frame)
                            image_blob1 = bucket.blob('images/image.jpg')
                            image_blob1.upload_from_filename('fire_detected2.png')
                            image_upload_success1 = True
                        except:
                            image_upload_success1 = False



                # alert camera 3
                if timer2 > 51:
                    timer2 = 0
                elif len(filtered_boxes2) != 0:
                    timer2 = timer2 + 1
                    print(timer2)
                    winsound.Beep(frequency=5000, duration=100)
                    if timer2 == 2:
                        print("Fire detected in camera 3")
                        self.alert1()
                        try:
                            cv2.imwrite("fire_detected2.png", frame)
                            image_blob2 = bucket.blob('images/image.jpg')
                            image_blob2.upload_from_filename('fire_detected2.png')
                            image_upload_success2 = True
                        except:
                            image_upload_success2 = False


                # alert camera 4
                if timer3 > 51:
                    timer3 = 0
                elif len(filtered_boxes3) != 0:
                    timer3 = timer3 + 1
                    print(timer3)
                    winsound.Beep(frequency=5000, duration=100)
                    if timer3 == 2:
                        print("Fire detected in camera 4")
                        self.alert1()
                        try:
                            cv2.imwrite("fire_detected3.png", frame)
                            image_blob3 = bucket.blob('images/image.jpg')
                            image_blob3.upload_from_filename('fire_detected3.png')
                            image_upload_success3 = True
                        except:
                            image_upload_success3 = False

                cv2.waitKey(25)

            else:
                self.cap.release()
                self.cap1.release()
                self.cap3.release()
                self.cap4.release()
                cv2.destroyAllWindows()
                break

    def stop_video(self):
        self.playing = False



    def clicker(self):
        a = self.comboBox.currentText()
        print(a)
        if a == "1":
            self.camer1()
        if a == "2":
            self.camer2()
        if a == "3":
            self.camer3()
        if a == "4":
            self.camer4()
        if a == "5":
            self.camer5()
        if a == "6":
            self.camer6()


    def camer1(self):
        cam = camera1()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height+10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def camer2(self):
        cam = camera2()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height+10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def camer3(self):
        cam = camera3()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height+10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def camer4(self):
        cam = camera4()
        width = cam.get_width()
        height = cam.get_height()
        widget3.setFixedWidth(width)
        widget3.setFixedHeight(height+10)
        widget3.addWidget(cam)
        widget3.setCurrentIndex(widget3.currentIndex() + 1)
        widget3.show()

    def displayimage(self, img, window = 1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGB888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.label_2.setPixmap(QPixmap.fromImage(img))
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayimage1(self, img, window = 1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGB888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.label_7.setPixmap(QPixmap.fromImage(img))
        self.label_7.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayimage2(self, img, window = 1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGB888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.label_8.setPixmap(QPixmap.fromImage(img))
        self.label_8.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def displayimage3(self, img, window = 1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGB888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.label_9.setPixmap(QPixmap.fromImage(img))
        self.label_9.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


    def emergency(self):
        emer = emergency_dialog()
        widget2.addWidget(emer)
        widget2.setFixedWidth(600)
        widget2.setFixedHeight(400)
        widget2.setCurrentIndex(widget2.currentIndex() + 1)
        widget2.show()

    def loginscreen(self):
        self.playing = False
        log = LoginScreen()
        widget.addWidget(log)
        widget.setFixedHeight(522)
        widget.setFixedWidth(800)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def alert1(self):
        a = alert()
        b.addWidget(a)
        b.setFixedWidth(600)
        b.setFixedHeight(400)
        b.setCurrentIndex(b.currentIndex()+1)
        b.show()

    def home(self):
        self.hide()
        self.playing = False
        home_screen = Home()
        widget.addWidget(home_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class alert(QDialog):
    def __init__(self):
        super(alert, self).__init__()
        loadUi("alert.ui", self)
        self.pushButton.clicked.connect(self.emergency)

    def emergency(self):
        emer = emergency_dialog()
        widget2.addWidget(emer)
        widget2.setFixedWidth(600)
        widget2.setFixedHeight(400)
        widget2.setCurrentIndex(widget2.currentIndex() + 1)
        widget2.show()


class emergency_dialog(QDialog):
    def __init__(self):
        super(emergency_dialog, self).__init__()
        loadUi("emergency_contact.ui", self)


class camera1(QMainWindow):
    def __init__(self):
        super(camera1, self).__init__()
        loadUi("extended.ui", self)
        self.playing = True
        self.cap = cv2.VideoCapture(0)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.closeEvent = self.closeEventOverride
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

    def update_frame(self):
        ret, frame = self.cap.read()
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print("fps: ", fps)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(fps), (50, 50), font, 1, (0, 0, 255), 2)
        if ret and self.playing == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_image)
            self.label.setPixmap(pixmap)
        else:
            self.playing = False

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def closeEventOverride(self, event):
        event.accept()


class camera2(QMainWindow):
    def __init__(self):
        super(camera2, self).__init__()
        loadUi("extended.ui", self)
        self.playing = True
        self.cap = cv2.VideoCapture("fire3.mp4")
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.closeEvent = self.closeEventOverride
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

    def update_frame(self):
        ret, frame = self.cap.read()
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print("fps: ", fps)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(fps), (50, 50), font, 1, (0, 0, 255), 2)
        if ret and self.playing == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_image)
            self.label.setPixmap(pixmap)
        else:
            self.playing = False

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def closeEventOverride(self, event):
        self.playing = False
        self.cap.release()
        event.accept()


class camera3(QMainWindow):
    def __init__(self):
        super(camera3, self).__init__()
        loadUi("extended.ui", self)
        self.playing = True
        self.cap = cv2.VideoCapture("fire4.mp4")
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.closeEvent = self.closeEventOverride
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

    def update_frame(self):
        ret, frame = self.cap.read()
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print("fps: ", fps)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(fps), (50, 50), font, 1, (0, 0, 255), 2)
        if ret and self.playing == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_image)
            self.label.setPixmap(pixmap)
        else:
            self.playing = False

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def closeEventOverride(self, event):
        self.playing = False
        self.cap.release()
        event.accept()


class camera4(QMainWindow):
    def __init__(self):
        super(camera4, self).__init__()
        loadUi("extended.ui", self)
        self.playing = True
        self.cap = cv2.VideoCapture("test.mp4")
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.closeEvent = self.closeEventOverride
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

    def update_frame(self):
        ret, frame = self.cap.read()
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print("fps: ", fps)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(fps), (50, 50), font, 1, (0, 0, 255), 2)
        if ret and self.playing == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap(q_image)
            self.label.setPixmap(pixmap)
        else:
            self.playing = False

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def closeEventOverride(self, event):
        self.playing = False
        self.cap.release()
        event.accept()



app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget2 = QtWidgets.QStackedWidget()
widget3 = QtWidgets.QStackedWidget()
b = QtWidgets.QStackedWidget()
login = LoginScreen()
widget.addWidget(login)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
