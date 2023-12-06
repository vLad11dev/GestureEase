# main_app.py
# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk
from gesture_recognition import GestureRecognition

class HandGestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Recognition App")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton", padding=10, relief="flat", background="#4CAF50", foreground="#10470b", font=("Helvetica", 12))

        self.tab_control = ttk.Notebook(root)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text="Запуск")
        self.tab_control.add(self.tab3, text="Проект")

        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.start_button = ttk.Button(self.tab1, text="Запустить", command=self.start_gesture_recognition)
        self.start_button.pack(pady=40)


        label_frame = ttk.Frame(self.tab1)
        label_frame.pack()

        self.image_labels = []
        gestures_info = [
            "Жест 1: Снимок экрана",
            "Жест 2: Экранная клавиатура",
            "Жест 3: Запуск голосового помощника",
            "Жест 4: Клик мыши",
            "Жест 5: Управление мышью",
            "Жест 6: Музыкальное приложение",
            "Жест 7: Запуск браузера",
            "Жест 8: Понижение громкости",
            "Жест 9: Повышение громкости",
            "Жест 10: Пауза / Запуск",
        ]

        common_image_size = (100, 100)

        for i in range(1, 11):
            image_path = f'image/{i}.jpg'

            pil_image = Image.open(image_path)
            pil_image = pil_image.resize(common_image_size, resample=Image.LANCZOS) # Resize image
            photo_image = ImageTk.PhotoImage(pil_image)

            label = ttk.Label(label_frame, image=photo_image, compound=tk.TOP, text=gestures_info[i - 1])
            label.photo = photo_image
            self.image_labels.append(label)


        row = 0
        column = 0
        for label in self.image_labels:
            label.grid(row=row, column=column, padx=10, pady=10, sticky="w")
            column += 1
            if column == 5:
                column = 0
                row += 1

        # Tab 2
        self.gesture_recognition = GestureRecognition()

        # Tab 3
        self.project_info = tk.Text(self.tab3, wrap="word", width=60, height=10, relief="flat", background="#f0f0f0", font=("Helvetica", 16))
        self.project_info.insert(tk.END,
                                 "Проект \"GestureEase\" - это интуитивная и простая система управления компьютером с использованием жестов, разработанная с учетом всех пользователей, включая тех, у кого ограничена моторика рук. Наша цель - сделать повседневное взаимодействие с компьютером максимально доступным и комфортным для всех.")
        self.project_info.configure(state="disabled")
        self.project_info.pack(pady=20)

        self.gesture_thread = None

    def start_gesture_recognition(self):
        if self.gesture_thread is None or not self.gesture_thread.is_alive():
            self.gesture_thread = Thread(target=self.gesture_recognition_thread)
            self.gesture_thread.start()

    def gesture_recognition_thread(self):
        self.gesture_recognition.start_gesture_recognition_thread()

        while True:

            self.root.update_idletasks()
            self.root.update()

if __name__ == "__main__":
    root = tk.Tk()

    root.iconphoto(True, tk.PhotoImage(file="hand_eye.png"))

    app = HandGestureApp(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 1100
    window_height = 600

    x_position = (root.winfo_screenwidth() - window_width) // 2
    y_position = (root.winfo_screenheight() - window_height) // 2
    root.resizable(width=False, height=False)
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_position, y_position))

    root.mainloop()
