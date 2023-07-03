from imutils import paths
import face_recognition
import pickle
import cv2
import os
# Definirea directorului pentru setul de date
dataset_folder = "Images"
# Obținerea phats-urilor către imagine
imagePaths = list(paths.list_images(dataset_folder))
# Inițializarea listelor de codificări și nume
knownEncodings = []
knownNames = []
# Parcurgerea în buclă a phat-urilor către imagini
for (i, imagePath) in enumerate(imagePaths):
 # Extragerea numelui persoanei
 name = os.path.basename(os.path.dirname(imagePath))
 # Încărcarea imagini și conversia acesteia în RGB
 image = cv2.imread(imagePath)
 rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 # Detectarea locației feței în imagine
 boxes = face_recognition.face_locations(rgb, model="hog")
 # Calcularea codificărilor feței
 encodings = face_recognition.face_encodings(rgb, boxes)
 # Atribuirea codificărilor și a numelor listelor respective
 knownEncodings.extend(encodings)
 knownNames.extend([name] * len(encodings))
# Serializarea codificarilor și a numelor pe disc
print("[INFO] Serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
with open("encodings.pickle", "wb") as f:
 f.write(pickle.dumps(data))
