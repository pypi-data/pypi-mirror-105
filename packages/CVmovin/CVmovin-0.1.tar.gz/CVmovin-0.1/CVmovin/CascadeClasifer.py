
import numpy as np
import cv2
################################ 
cap = cv2.VideoCapture(0)
##################################
class CascadeDetec():
	"""
	  - This class is detets the cascade_classifier and gives the value
	"""
	def __init__(self, cas='E:/programming/Ultimate A.I/resources/cascade clasifier'):
		self.cascade = cas
		self.face_cascade = cv2.CascadeClassifier(self.cascade)

	def detectsign(self, img): 
		"""
		  - This funtions takes in img and gives contour img with detected varibles for been used further
		"""
		self.img = img
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
		stop = False
		for (x,y,w,h) in self.faces:
		    self.img = cv2.rectangle(self.img,(x,y),(x+w,y+h),(0,255,0),2)
		    self.img = cv2.putText(self.img, "Stop", (x, y), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 2)
		    stop = True
		return stop , img

def main():
	stop_sign = CascadeDetec()
	while True:
		_, img = cap.read()
		stop_detected, imgu = stop_sign.detectsign(img)
		cv2.imshow("image", imgu)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	return stop_detected

if __name__ == '__main__':
	stop = main()

		