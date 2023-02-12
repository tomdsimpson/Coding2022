# Facial Recognition

import face_recognition
import cv2
import os
import numpy as np
import math


# Encoding know faces
def encode_Faces():
    knownFaces = []
    knownNames = []
    for face in os.listdir("Faces"):
        face_image = face_recognition.load_image_file(f"Faces/{face}")
        face_encoding = face_recognition.face_encodings(face_image)[0]
        knownFaces.append(face_encoding)
        knownNames.append(face.split(".")[0])
    
    return knownFaces, knownNames

# Confidence
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

# Face comparisons
def run_recognition(knownFaces, knownNames):

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Video source not found. ") 
        cap.release()
        cv2.destroyAllWindows()
    
    else:

        # Resizing to reduce load
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        processed_frame = True

        while True:

            ret, frame = cap.read()

            if processed_frame:
                rgb = frame[:, :, ::-1] # Converting BRG -> RGB
                face_locations = face_recognition.face_locations(rgb)
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                found_faces = []
                
                for face in face_encodings:
                    
                    matches = face_recognition.compare_faces(knownFaces, face)
                    name = "unknown"
                    confidence = "unknown"
                    face_distances = face_recognition.face_distance(knownFaces, face)
                    best_match = np.argmin(face_distances)

                    if matches[best_match]:
                        name = knownNames[best_match]
                        confidence = face_confidence(face_distances[best_match])

                    found_faces.append(f"{name}, {confidence}")
            
            processed_frame = not processed_frame
            
            # Displaying matches
            for (top, right, bottom, left), name in zip(face_locations, found_faces):

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            cv2.imshow("Face Recognition", frame)
            key = cv2.waitKey(1)
            if key == 27:
                cap.release()
                cv2.destroyAllWindows()

knownFaces, knownNames = encode_Faces()
run_recognition(knownFaces, knownNames)