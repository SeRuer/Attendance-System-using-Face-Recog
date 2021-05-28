import cv2
import os
import os.path
from PyQt5.QtWidgets import *
import sys
import sqlite3
from PyQt5.uic import loadUi
from PIL import Image
import numpy as np
import pyrebase
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import datetime as datetime
import matplotlib.dates as mdates
from matplotlib import style
style.use('Solarize_Light2')

#Insert Firebase API in here
firebaseConfig = {"apiKey": "",
                  "authDomain": "",
                  "databaseURL": "",
                  "projectId": "",
                  "storageBucket": "",
                  "messagingSenderId": "",
                  "appId": "",
                  "measurementId": ""}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
conn = sqlite3.connect('FaceBase.db')
curs = conn.cursor()


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("mainProgram.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.enterButton.clicked.connect(self.loginAction)
        self.invalid.setVisible(False)
        self.show()

    def loginAction(self):
        email = self.email.text()
        password = self.password.text()
        try:
            auth.sign_in_with_email_and_password(email, password)
            print("Succesfully logged in with this email:", email)
            self.mainTwo = MainApplication()
            self.close()
            self.mainTwo.show()
        except:
            print("Error")
            self.invalid.setVisible(True)


class MainApplication(QMainWindow):
    def __init__(self):
        super(MainApplication, self).__init__()
        loadUi("mainWindow.ui", self)
        self.Function_Buttons()
        self.loadData()
        self.loadAttendance()

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    def Function_Buttons(self):
        self.deleteButton.clicked.connect(self.deleteData)
        self.submitButton.clicked.connect(self.submitData)
        self.searchButton.clicked.connect(self.searchStudent)
        self.takePhoto_button.clicked.connect(self.takePictures)
        self.trainface_button.clicked.connect(self.trainRecognition)
        self.reportButton.clicked.connect(self.dataGraph)



    #################-----1 Add Student Functionalities -----######################

    def submitData(self):
        self.conn = sqlite3.connect("FaceBase.db")
        self.curs = self.conn.cursor()
        # allows the user to type into one of the boxes shown
        idNumber = self.lineEdit_idNumber.text()
        username = self.lineEdit_username.text()
        degree = self.lineEdit_degree.text()
        gender = self.lineEdit_gender.text()
        warningMessage = QMessageBox.warning(self, "Add Student Data", "Are you certain you want to add this student to the database?", QMessageBox.Yes | QMessageBox.No)
        if warningMessage == QMessageBox.Yes:
            # The query that will insert the data into the FaceBase.db Database
            self.curs.execute("INSERT OR IGNORE INTO Class(ID, Name, Major, Gender) VALUES (?, ?, ?, ?)",
                              (idNumber, username, degree, gender))

            #Clears text box after submission
            self.lineEdit_idNumber.setText('')
            self.lineEdit_username.setText('')
            self.lineEdit_degree.setText('')
            self.lineEdit_gender.setText('')
            self.statusBar().showMessage("New student has succesfully been added")
            self.conn.commit()
            self.loadData()
    ###############################################################################
    #################----- Delete Student Functionalities -----######################
    def deleteData(self):
        conn = sqlite3.connect('FaceBase.db')
        curs = conn.cursor()
        eliminate = "SELECT * FROM Class"
        rely = curs.execute(eliminate)

        warningMessage = QMessageBox.warning(self, "Delete Student Data", "Are you certain you want to delete this student from the database?", QMessageBox.Yes | QMessageBox.No)
        if warningMessage == QMessageBox.Yes:
            for row in enumerate(rely):
                if row[0] == self.tableWidgetTwo.currentRow():
                    info = row[1]
                    id = info[0]
                    name = info[1]
                    major = info[2]
                    gender = info[3]
                    attendance = info[4]
                    time = info[5]
                    curs.execute("DELETE FROM Class WHERE ID=? AND Name=? AND Major=? AND Gender=? AND Attendance=? "
                                 "AND Time=?",
                                 (id, name, major, gender, attendance, time))
                    conn.commit()
                    self.statusBar().showMessage("S`tudent has succesfully been deleted")
                    self.loadData()
                    self.loadAttendance()


    #################----- Load Widget data  -----######################
    def loadData(self):
        self.conn = sqlite3.connect("FaceBase.db")
        self.curs = self.conn.cursor()
        self.curs.execute("SELECT ID, Name, Major, Gender FROM Class")
        data = self.curs.fetchall()

        self.tableWidgetTwo.setRowCount(0)
        self.tableWidgetTwo.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidgetTwo.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_allocator = self.tableWidgetTwo.rowCount()
            self.tableWidgetTwo.insertRow(row_allocator)

        conn.close()

    ###############################################################################
    #################----- Load Widget data  -----######################
    def loadAttendance(self):
        self.conn = sqlite3.connect("FaceBase.db")
        self.curs = self.conn.cursor()
        self.curs.execute("SELECT ID, Name, Major, Gender, Attendance, Time FROM Class")
        data = self.curs.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_allocator = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_allocator)

        conn.close()




    #################----- Search Student Functionalities -----######################

    def searchStudent(self):
        searchStudent = self.searchLineEdit.text()
        # This will load the user interface database
        conn = sqlite3.connect('FaceBase.db')
        self.curs = conn.cursor()

        search = ("SELECT * FROM Class WHERE ID =?")
        self.curs.execute(search, [(searchStudent)])
        row = self.curs.fetchone()
        return row

    #############################################################
    #################----- Graph Data -----######################
    def dataGraph(self):
        # This will load the user interface database
        conn = sqlite3.connect('FaceBase.db')
        self.curs = self.conn.cursor()
        self.curs.execute("SELECT Time FROM Class")
        dates = []
        values = []
        for row in self.curs.fetchall():
            print(row[0])
            dates.append(datetime.datetime.fromtimestamp(row[0]))
            values.append(row[1])

        plt.plot_date(dates, values, '-')
        plt.show()


    #################----- Taking pictures of person functionality -----######################

    # Counter for images
    def count_pictures(k):
        try:
            float(1)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(k)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def takePictures(self):
        print("Camera on")
        captureDevice = cv2.VideoCapture(0)
        captureDevice.set(3, 650)  # Sets the camera width
        captureDevice.set(4, 480)  # Sets the camera height

        print("Files read")
        # self.checkCascade()
        ID = input("Input user ID:   ")
        if (self.count_pictures(ID)):
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            counter = 0
            print("Detect #1")
            while True:
                ret, frame = captureDevice.read()

                # For now this will convert the frames to grey scale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # print("Convert function #2")
                # detects the frames for different sizes
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)
                # This will loop for every single student
                # print("Loop is about to start")
                for (x, y, w, h) in faces:
                    print(x, y, w, h)
                    # Crop the photo frame into a rectangle
                    # If faces found
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # add the sample number
                    counter = counter + 1
                    # Save the face into the folder
                    cv2.imwrite("Dataset/" + os.sep + ID + ".jpg", gray[y:y + h, x:x + w])
                    # Showcase the frame

                cv2.imshow('Frame', frame)
                # Wait for only 80 milli
                if cv2.waitKey(1) & 0xFF == ord('f'):
                    cv2.destroyAllWindows()
                    break
                    # So this will break if the pictures are more than 100
                elif counter > 200:  # decreased the pictures due to scalability issues
                    break

        captureDevice.release()


    #################----- Train pictures of person functionality -----######################

    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def extractImages(path, self):
        path = "Dataset/"
        recogniser = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

        dirs = [os.path.join(path, f) for f in os.listdir(path)]
        faceImages = []
        ID = []
        for dirs in dirs:
            PIL_img = Image.open(dirs).convert("L")  # This is what will make it change
            img_numpy = np.array(PIL_img, "uint8")
            identification = int(os.path.split(dirs)[1].split(".")[0])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceImages.append(img_numpy[y:y+h, x:x+w])
                ID.append(identification)
                print(ID)
        return faceImages, ID

    def trainRecognition(self):
        recogniser = cv2.face.LBPHFaceRecognizer_create()
        detect = "haarcascade_frontalface_alt"
        faceCascade = cv2.CascadeClassifier(detect)
        faceImages, ID = self.extractImages("Dataset/")
        recogniser.train(faceImages, np.array(ID))
        recogniser.save("trainner/trainner.yml")
        print("Done")


def main():
    app = QApplication(sys.argv)
    win = Login()
    win.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


if __name__ == '__main__':
    main()
