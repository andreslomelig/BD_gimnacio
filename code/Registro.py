import os.path
import datetime
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import util
import sqlite3
import pickle
#import matplotlib.pylab as plt

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.idact = 26

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)


        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknow_img_path = './.tmp.jpg'
        cv2.imwrite(unknow_img_path,self.most_recent_capture_arr)

        unknown_picture = face_recognition.load_image_file(unknow_img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_picture)[0]

        bo = 1
        for nombre_archivo in os.listdir(self.db_dir):
            ruta_imagen = os.path.join(self.db_dir, nombre_archivo)
            db_picture = face_recognition.load_image_file(ruta_imagen)
            db_face_encoding = face_recognition.face_encodings(db_picture)[0]
            print(db_face_encoding)
            results = face_recognition.compare_faces([db_face_encoding], unknown_encoding)
            if results[0] == True:
             nombre, extension = os.path.splitext(nombre_archivo)
             util.msg_box('Welcome back ', 'Welcome, {}.' .format(nombre))
             bo=0
             break
        if bo == 1:
            util.msg_box('Tu no estas registrado', "Tu no Estas registrado")


        # Establecer la conexión con la base de datos (ajusta la cadena de conexión según tu caso)
        conn = sqlite3.connect('GYM.db')
        cursor = conn.cursor()

        # Consulta SQL para obtener todos los Unknown_Encoding
        sql_select_all_encodings = "SELECT Facial_Features, Nombre FROM Cliente"

        # Ejecutar la consulta
        cursor.execute(sql_select_all_encodings)
        resultados = cursor.fetchall()

        # Iterar sobre los resultados y deserializar los Unknown_Encoding
        for resultado in resultados:
            id_cliente = resultado[1]
            unknown_encoding = pickle.loads(resultado[0])
            print(f"Cliente {id_cliente}: {unknown_encoding}")

        # Cerrar la conexión
        conn.close()
    
        #output = subprocess.check_output(['face_recognition',self.db_dir, unknow_img_path])
        os.remove(unknow_img_path)
        


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x700+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput Name:')
        self.text_label_register_new_user.place(x=750, y=70)
        '''
        self.entry_text_register_new_user2 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user2.place(x=750, y=580)

        self.text_label_register_new_user2 = util.get_text_label(self.register_new_user_window, 'Please, \ninput Age:')
        self.text_label_register_new_user2.place(x=750, y=500)
        
        self.entry_text_register_new_user4 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user4.place(x=750, y=470)

        self.text_label_register_new_user3 = util.get_text_label(self.register_new_user_window, 'Please, \ninput phone:')
        self.text_label_register_new_user3.place(x=750, y=550)

        self.entry_text_register_new_user5 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user5.place(x=750, y=630)

        self.text_label_register_new_user5 = util.get_text_label(self.register_new_user_window, 'Please, \ninput Email:')
        self.text_label_register_new_user5.place(x=750, y=710)

        self.entry_text_register_new_user6 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user6.place(x=750, y=790)

        self.text_label_register_new_user6 = util.get_text_label(self.register_new_user_window, 'Please, \ninput Email:')
        self.text_label_register_new_user6.place(x=750, y=870)

        self.entry_text_register_new_user7 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user7.place(x=750, y=950)

        self.text_label_register_new_user7 = util.get_text_label(self.register_new_user_window, 'Please, \ninput Birth Date:')
        self.text_label_register_new_user7.place(x=750, y=1030)

        self.entry_text_register_new_user8 = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user8.place(x=750, y=1110)

        self.text_label_register_new_user8 = util.get_text_label(self.register_new_user_window, 'Please, \ninput Home Adress:')
        self.text_label_register_new_user8.place(x=750, y=1190)
        '''

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        conn = sqlite3.connect('GYM.db')
        cursor = conn.cursor()  
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)),self.register_new_user_capture)
        unknow_img_path = './.tmp.jpg'
        cv2.imwrite(unknow_img_path,self.register_new_user_capture)
        unknown_picture = face_recognition.load_image_file(unknow_img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_picture)[0]
        unknown_encoding_serialized = pickle.dumps(unknown_encoding)
        datos = (self.idact, name, 'Calle 123',unknown_encoding_serialized)
        self.idact += 1
        sql_insert_cliente = "INSERT INTO Cliente (Id_cliente, Nombre, Domicilio, Facial_Features) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert_cliente, datos)
        conn.commit()
        conn.close()
        util.msg_box('Success!', 'User was registered successfully !')
        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()