import cv2
import os
import numpy as np
from PIL import Image

path = "Dataset/"
recogniser = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");


def extractImages(path):
    dirs = [os.path.join(path, f) for f in os.listdir(path)]
    faceImages = []
    ID = []
    for dirs in dirs:
        PIL_img = Image.open(dirs).convert("L")  # This is what will make it change
        img_numpy = np.array(PIL_img, "uint8")
        identification = int(os.path.split(dirs)[1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceImages.append(img_numpy[y:y + h, x:x + w])
            ID.append(identification)
            print(ID)
    return faceImages, ID

print("This might take a while....")
faces,ID = extractImages(path)
recogniser.train(faces, np.array(ID))
#Insert model name in the ""
recogniser.write("trainner/")
print("Done! Numbers of faces have been trained")
