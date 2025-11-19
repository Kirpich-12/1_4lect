import tkinter as tk
from bandit import OneArmedBandit


root = tk.Tk()
root.title("Изменяющееся окно")
root.geometry("400x400")
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")


def startwind():
    for widget in root.winfo_children():
        widget.destroy()
        
    label = tk.Label(root, text="Нажмите кнопку, чтобы поиграть в казино", font=("Arial", 12))
    label.pack(pady=20)
    
    button = tk.Button(root, text="Казино", command=sec_wind)
    button.pack()

def sec_wind():
    for widget in root.winfo_children():
        widget.destroy()
    
    label = tk.Label(root, text="Добро пожаловать в казино!", font=("Arial", 14))
    label.pack(pady=20)

    rollbtn = tk.Button(root, text='Слоты', command=rollet)
    rollbtn.pack(pady=20)
    
    button = tk.Button(root, text="Вернуть обратно", command=startwind)
    button.pack(pady=8)

    
def dothis():
    app = OneArmedBandit()
    app.place_slaves

def rollet():
    for widget in root.winfo_children():
        widget.destroy()
    
    label = tk.Label(root, text="Слоты", font=("Arial", 14))
    label.pack(pady=20)

    button = tk.Button(root, text="Слоты", command=dothis)
    button.pack(pady=20)

    button = tk.Button(root, text="Вернуть обратно", command=sec_wind)
    button.pack(pady=20)

startwind()
root.mainloop()