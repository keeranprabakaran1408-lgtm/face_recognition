import cv2
import sqlite3
from gpiozero import LED
from datetime import datetime
green_led = LED(17)
face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml')
recogniser = cv2.face.LBPHFaceRecognizer_create()
recogniser.read('trainer.yml')
conn = sqlite3.connect('access_log.db')
cursor = conn.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS access_log (id INTEGER PRIMARY KEY AUTOINCREMENT, label INTEGER, confidence REAL, status TEXT, timestamp TEXT)''')
conn.commit()
stream = cv2.VideoCapture(0)

if not stream.isOpened():
	print("No Stream")
	exit()
count = 0
filename = 0
while(True):
	
	ret,frame = stream.read()
	gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.15, minNeighbors=5, minSize=(30,30))
	
	for(x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
		face_crop = gray_image[y:y+h, x:x+w]
		label, confidence = recogniser.predict(face_crop)
		text = f"Label: {label} Con: {confidence}"
		cv2.putText(frame,text,  (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)




		if confidence < 85:
			text = f"Access Granted ({int(confidence)})"
			colour = (0, 255, 0)
			green_led.on()
			cursor.execute("INSERT INTO access_log(label, confidence, status, timestamp) VALUES(?,?,?,?)", (label, confidence, "Granted", str(datetime.now())))
			conn.commit()

		else:
			text = f"Access Denied ({int(confidence)})"
			colour = (0, 0, 255)
			green_led.off()
			cursor.execute("INSERT INTO access_log (label, confidence, status, timestamp) VALUES (?,?,?,?)", (label, confidence, "Denied", str(datetime.now())))
			conn.commit()
                        

		frame_width = frame.shape[1]
		cv2.rectangle(frame, (0, 0), (frame_width, 50), colour, -1)

		cv2.putText(frame, text,  (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


	#	if  filename<=40:
			#face_img =  gray_image[y:y+h, x:x+w]
			#if count % 5 == 0:
				#filename_string = "dataset/keeran/test" + str(filename) + ".jpg"
				#cv2.imwrite(filename_string, face_img)
				#filename+=1

		if len(faces) == 0:
			green_led.off()
		count+=1
	if not ret:
		print("NO stream")
		break
	cv2.imshow("Webcam", frame)
	if cv2.waitKey(1) == ord('q'):
		break
conn.close()
stream.release()
cv2.destroyAllWindows()
