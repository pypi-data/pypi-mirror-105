"""
this module detectes the perfect color of hsv 

"""

import cv2
import numpy as np

cap = "C:/Users/STUDHOLIC/Pictures/Capture2.PNG"

class ColorDetection:

    def color_picker(cap, hmin, smin, vmin, hmax, smax, vmax):

        def empty(a):
            pass

        cv2.namedWindow("Trackbars")
        cv2.resizeWindow("Trackbars", 640, 240)

        cv2.createTrackbar("Hue_min", "Trackbars", hmin, 179, empty)
        cv2.createTrackbar("Sat_min", "Trackbars", smin, 255, empty)
        cv2.createTrackbar("Val_min", "Trackbars", vmin, 255, empty)
        cv2.createTrackbar("Hue_max", "Trackbars", hmax, 179, empty)
        cv2.createTrackbar("Sat_max", "Trackbars", smax, 255, empty)
        cv2.createTrackbar("Val_max", "Trackbars", vmax, 255, empty)

        while True:
            img = cv2.imread(cap)
            #ret, img = cap.read()
            imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            h_min = cv2.getTrackbarPos("Hue_min", "Trackbars")
            s_min = cv2.getTrackbarPos("Sat_min", "Trackbars")
            v_min = cv2.getTrackbarPos("Val_min", "Trackbars")

            h_max = cv2.getTrackbarPos("Hue_max", "Trackbars")
            s_max = cv2.getTrackbarPos("Sat_max", "Trackbars")
            v_max = cv2.getTrackbarPos("Val_max", "Trackbars")
          

            lower = np.array([h_min, s_min, v_min])
            upper = np.array([h_max, s_max, v_max])

            mask = cv2.inRange(imgHsv, lower, upper)
            res_mask = cv2.bitwise_and(img, img, mask=mask)

            cv2.imshow("Originally", img)
            cv2.imshow("Mask", mask)
            cv2.imshow("result", res_mask)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__=='__main__':
    ColorDetection.color_picker(cap, 0, 0, 0, 0, 0, 0)
