import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Puedes cambiar esto si tienes múltiples cámaras

        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="Tomar Foto", width=10, command=self.snapshot)
        self.btn_snapshot.pack(padx=10, pady=10)

        self.btn_open_gallery = tk.Button(window, text="Abrir Galería", width=15, command=self.open_gallery)
        self.btn_open_gallery.pack(padx=10, pady=10)

        self.update()
        self.window.mainloop()

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW) 
        self.window.after(10, self.update)
    def open_gallery(self):
        gallery_window = tk.Toplevel(self.window)
        gallery_window.title("Galería")

        image = Image.open("snapshot.png")
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(gallery_window, image=photo)
        label.image = photo  # Para evitar que la imagen sea eliminada por el recolector de basura
        label.pack()

# Crea la aplicación y comienza el bucle
root = tk.Tk()
app = WebcamApp(root, "Webcam App")
