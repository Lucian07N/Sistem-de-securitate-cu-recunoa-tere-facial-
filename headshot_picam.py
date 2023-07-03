import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
name = 'Lucian'
# Inițializare cameră PiCamera
cam = PiCamera()
cam.rotation = 180
cam.resolution = (512, 304)
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))
img_counter = 0
while True:
 # Capturare cadre continuu
 for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   image = frame.array

   # Afișare imagine
   cv2.imshow("Press Space to take a photo", image)

   # Eliberare buffer pentru următorul cadru
   rawCapture.truncate(0)

   # Verificare apăsare tastă
   k = cv2.waitKey(1)
   rawCapture.truncate(0)

   # Dacă este apăsată tasta 'q', se iese din buclă
   if k == ord('q'):
     break
   # Dacă este apăsată tasta Spațiu, se salvează imaginea
   elif k == 32:
     # Tasta Spațiu apăsată
     img_name = "Imagini/" + name + "/imagine_{}.jpg".format(img_counter)
     cv2.imwrite(img_name, image)
     print("{} salvată!".format(img_name))
     img_counter += 1

 if k == ord('q'):
    print("q hit, closing...")
    break
# Închidere ferestre
cv2.destroyAllWindows()
