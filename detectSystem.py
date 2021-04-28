import cv2
import datetime
import os
import sqlite3

##Creates the video capture
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(3, 650)  # Sets the camera width
camera.set(4, 480)  # Sets the camera height
print("Test")
# Creates the window size of for the face
minW = 0.1 * camera.get(3)
minH = 0.1 * camera.get(4)

face_module = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_module = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# recogniser = cv2.face.LBPHFacerecognizer_create() # This will rea the LBPH method
recogniser = cv2.face.LBPHFaceRecognizer_create()
recogniser.read(r"/Users/TMuja/Documents/Attempt/trainner/trainner.yml")  # This is where the YML file will be read


def getStudent(ID):
    connection = sqlite3.connect(r"/Users/TMuja/Documents/Attempt/FaceBase.db")
    command = "SELECT * FROM Class WHERE ID=" + str(ID)
    cursor = connection.execute(command)
    student = None
    for row in cursor:
        student = row
    connection.close()
    return student


print("Test 2")

# This is where the detection logic will occur
while True:
    ret, frame = camera.read()
    if ret is True:
        # print("frame.shape")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_module.detectMultiScale(gray, 1.5, 5, minSize=(int(minW), int(minH)), flags=cv2.CASCADE_SCALE_IMAGE)

        # This will loop for every single student
        for (x, y, w, h) in face:
            # print(x, y, w, h)
            # Crop the photo frame into a rectangle
            # If faces found
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            colour = (frame[y:y + h, x:x + w])
            GraGray = gray[y:y + w, x:x + w]
            eye_shape = eye_module.detectMultiScale(GraGray, 1.3, 5)
            for (ex, ey, ew, eh) in eye_shape:
                cv2.rectangle(colour, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                ID, conf = recogniser.predict(gray[y:y + h, x:x + w])
                student = getStudent(ID)
                if (student != None):
                    print(student, face)
                    if (conf > 50):
                        print(student[1] + ".")
                        student = getStudent(ID)
                        connection = sqlite3.connect(r"/Users/TMuja/Documents/Attempt/FaceBase.db")
                        time = datetime.datetime.now()
                        print("Added")
                        command = "UPDATE Class SET Attendance='Present', Time = datetime() WHERE ID=" + str(ID)
                        cursor = connection.execute(command)
                        connection.commit()
                        connection.close()
                        eyes = eye_module.detectMultiScale(colour)
                        print(conf)
                    else:
                        ID = "unknown"
                        if (conf > 75):  # Depends on the quality on training
                            print("Unknown Individual")
                            # fileLine = len(os.listdir(r"/Users/TMuja/Documents/Attempt/UnknownPeople"))+1
                            cv2.imwrite( r"/Users/TMuja/Documents/Attempt/UnknownPeople/" + os.sep + "TaggedUnknown" + ".jpg",
                                gray[y:y + h, x:x + w])
                    writing = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, str(ID), (x + 5, y - 5), writing, 2, (255, 255, 255), 1)

        cv2.imshow('Facial Recognition program', frame)  # show the camera
        if cv2.waitKey(1) == ord("q"):  # Q to exit
            cv2.destroyAllWindows()
            break
    else:
        continue
camera.release()
