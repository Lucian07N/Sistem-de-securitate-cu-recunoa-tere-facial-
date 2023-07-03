from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep, strftime
import subprocess
import os
import cv2
import face_recognition
import imutils
import pickle
from imutils.video import FPS
import face_recognition_models
BEAM_PIN = 17
def break_beam_callback(channel):
 """
 Funcție de callback apelată atunci când se detectează o schimbare a
 stării fasciculului. Verifică starea fasciculului și înregistrează un
 videoclip dacă fasciculul este întrerupt.
 """
 if GPIO.input(BEAM_PIN):
 print("Beam unbroken")
 else:
 print("Beam broken")
 with PiCamera() as camera:
 camera.rotation = 180
 camera.start_preview()
 timestamp = strftime("%Y-%m-%d-%H-%M-%S")
 video_file = f'/home/pi/Desktop/proiect_licenta/video/video_{timestamp}.h264'
 camera.start_recording(video_file)
 sleep(5)
 camera.stop_recording()
 camera.stop_preview()
 process_video(video_file)
def convert_to_mp4(video_file):
 """
 Converteste un fișier video .h264 în format .mp4 utilizând MP4Box.
 """
 output_file = video_file.replace('.h264', '.mp4')
 command = ['MP4Box', '-add', video_file, output_file]
 subprocess.run(command)
 print(f"Video saved as {output_file}")
def delete_file(file_path):
 """
 Șterge un fișier din sistem.
 """
 os.remove(file_path)
 print(f"Deleted file: {file_path}")
def process_video(video_file):
 """
 Procesează un fișier video înregistrat anterior, detectează fețele
 și le recunoaște utilizând modele pre-antrenate.
 Apoi afișează videoclipul cu fețele și numele recunoscute.
 """
 currentname = "unknown"
 encodingsP = "encodings.pickle"
 print("[INFO] loading encodings + face detector...")
 data = pickle.loads(open(encodingsP, "rb").read())
 vs = cv2.VideoCapture(video_file)
 fps = FPS().start()
 video_ended = False
 # Capturarea și procesarea fiecărui frame al videoclipului
 while not video_ended:
 ret, frame = vs.read()
 if not ret:
 video_ended = True
 break
 frame = imutils.resize(frame, width=500)
 boxes = face_recognition.face_locations(frame)
 encodings = face_recognition.face_encodings(frame, boxes)
  names = []
 for encoding in encodings:
 matches = face_recognition.compare_faces(data["encodings"], encoding)
 name = "Unknown"
 if True in matches:
 matchedIdxs = [i for (i, b) in enumerate(matches) if b]
counts = {}
 for i in matchedIdxs:
 name = data["names"][i]
counts[name] = counts.get(name, 0) + 1
 name = max(counts, key=counts.get)
 # Actualizarea numelui dacă o potrivire este găsită
 if currentname != name:
 currentname = name
print(currentname)
 names.append(name)
 # Desenarea dreptunghiurilor și afișarea numelui pentru fiecare față detectată
 for ((top, right, bottom, left), name) in zip(boxes, names):
 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
 y = top - 15 if top - 15 > 15 else top + 15
 cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)
 cv2.imshow("Facial Recognition is Running", frame)
 key = cv2.waitKey(1) & 0xFF
 if key == ord("q"):
 break
 fps.update()
 cv2.destroyAllWindows()
 vs.release()
 fps.stop()
 convert_to_mp4(video_file)
 delete_file(video_file)
 # Trimiterea emailului doar dacă numele detectat nu este "Lucian"
 if currentname != "Lucian":
 send_video_email()
def send_video_email():
 """
 Trimite un email cu videoclipul înregistrat.
 """
 command = ['python3', 'mail.py']
 subprocess.run(command)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=break_beam_callback)
message = input("Press enter to quit\n\n")
GPIO.cleanup()
