import tkinter as tk
from tkinter import ttk

# --- Основное окно ---
root = tk.Tk()
root.title("Красивый стандартный экран")
root.geometry("500x300")
root.configure(bg="#e7ecf2")  # мягкий серо-голубой фон

# --- Стиль ttk ---
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Segoe UI", 12),
    padding=10
)

style.configure(
    "TLabel",
    font=("Segoe UI", 14),
    background="#e7ecf2",
    foreground="#333"
)

# --- Центральный фрейм ---
frame = ttk.Frame(root, padding=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

label = ttk.Label(frame, text="Добро пожаловать в приложение!")
label.pack(pady=10)

def on_click():
    label.config(text="Кнопка нажата!")

button = ttk.Button(frame, text="Нажми меня", command=on_click)
button.pack(pady=10)

# Тень/окантовка с помощью Canvas
shadow = tk.Canvas(root, width=480, height=260, bg="#d0d7df", highlightthickness=0)
shadow.place(relx=0.5, rely=0.5, anchor="center")
frame.lift()

root.mainloop()
