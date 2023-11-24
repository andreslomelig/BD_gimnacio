import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
#import matplotlib.pylab as plt
import util
import os.path
import numpy as np
import pickle
import sqlite3

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x520+350+100")
        self.window.title("Face Recognition")      

        self.video_source = 0  # Puedes cambiar esto si tienes múltiples cámaras
        self.frame_count = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(self.window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_exit = tk.Button(self.window, text="Salir", width=10, command=self.exit)
        self.btn_exit.pack(padx=10, pady=10)

        self.update()

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def login(self,face_locations):
        factual = self.frame
        respuesta = ''
        
        unknow_img_path = './.tmp.jpg'
        cv2.imwrite(unknow_img_path,self.frame)
        unknown_picture = face_recognition.load_image_file(unknow_img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_picture)[0]
        conn = sqlite3.connect('GYM.db')
        cursor = conn.cursor()
        # Consulta SQL para obtener todos los Unknown_Encoding
        sql_select_all_encodings = "SELECT Facial_Features, Nombre FROM Cliente"
        # Ejecutar la consulta
        cursor.execute(sql_select_all_encodings)
        resultados = cursor.fetchall()

        # Iterar sobre los resultados y deserializar los Unknown_Encoding
        bo = 1
        for resultado in resultados:
            nombre = resultado[1]
            db_face_encoding = pickle.loads(resultado[0])
            results = face_recognition.compare_faces([db_face_encoding], unknown_encoding)
            if results[0] == True:
             respuesta = "Welcome, {}." .format(nombre)
             bo=0
             break
        if bo == 1:
            respuesta = "Invalid Access"
            

        # Cerrar la conexión
        conn.close()        

        self.register_new_user_window = tk.Toplevel(self.window)
        self.register_new_user_window.title("Bienvenido")

        for face_location in face_locations:
            cv2.line(factual, (face_location[1], face_location[0]), (face_location[1], face_location[2]), (0, 255, 0), 2)
            cv2.line(factual, (face_location[1], face_location[0]), (face_location[3], face_location[0]), (0, 255, 0), 2)
            cv2.line(factual, (face_location[3], face_location[2]), (face_location[1], face_location[2]), (0, 255, 0), 2)
            cv2.line(factual, (face_location[3], face_location[2]), (face_location[3], face_location[0]), (0, 255, 0), 2)

        photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(factual, cv2.COLOR_BGR2RGB)))

        label = tk.Label(self.register_new_user_window, image=photo)
        label.image = photo
        label.pack()

        text_label = tk.Label(self.register_new_user_window, text=respuesta)
        text_label.pack()

    def exit(self):
        self.vid.release()
        self.window.destroy()

    def update(self):
        ret, frame = self.vid.read()
        self.frame = frame
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        f = self.img_
        rgb_frame = f[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        self.frame_count += 1
        if self.frame_count % 30 == 0 and face_locations:
            self.last_frame = self.frame
            self.login(face_locations)   
        self.window.after(10, self.update)

    def start(self):
        self.window.mainloop()

# Crea la aplicación y comienza el bucle
app = App()
app.start()