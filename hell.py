from tkinter import *
import ttk

def HelloWorld(world):
    root = Tk() # инициализация окна
    root.title("Имя окна") # имя окна
    root.geometry('400x400') # размер окна
    style = ttk.Style(root)
    root.tk.call('source', 'azure.tcl')  # Укажи здесь путь к файлу темы
    style.theme_use('azure')

    if world == "print":
        txt = 'Hello World'
    else:
        txt = world

    label = Label(root, text=txt) # добавлям метку
    label.place(x=200,y=10)              # местоположение метки по пикселям
    root.mainloop() # отображение окна
