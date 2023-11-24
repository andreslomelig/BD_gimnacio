import os.path
import datetime
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
import matplotlib.pylab as plt
import sqlite3
import pickle
db_dir = './db'
id = 1

# Consulta SQL para obtener todos los Unknown_Encoding

# Ejecutar la consulta
for nombre_archivo in os.listdir(db_dir):
    if id == 24:
        break
    ruta_imagen = os.path.join(db_dir, nombre_archivo)
    db_picture = face_recognition.load_image_file(ruta_imagen)
    db_face_encoding = face_recognition.face_encodings(db_picture)[0]
    unknown_encoding_serialized = pickle.dumps(db_face_encoding)
    print(db_face_encoding)
    conn = sqlite3.connect('GYM.db')
    cursor = conn.cursor()
    sql_update = f"UPDATE Cliente SET Facial_Features = ? WHERE Id_cliente = ?"
    cursor.execute(sql_update, (unknown_encoding_serialized, id))
    conn.commit()
    conn.close()
    id += 1
