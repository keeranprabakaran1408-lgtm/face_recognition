import cv2
import numpy as np
import os

recogniser = cv2.face.LBPHFaceRecognizer_create()

tests = []
labels = []
for filename in os.listdir("dataset/keeran"):
	load_file = "dataset/keeran/" + filename
	grayscale_images = cv2.imread(load_file, cv2.IMREAD_GRAYSCALE)
	tests.append(grayscale_images)
	labels.append(0)
	
recogniser.train(tests, np.array(labels))
recogniser.save('trainer.yml')
