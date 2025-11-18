from tkinter import *
from tkinter import ttk



def newbtn(root):
    frame = Frame(root)

    label = Label(frame, text="QQ")
    label.place(x=12, y=12)
    print('helo')




def HelloWorld(world):
    root = Tk()
    root.title("Имя окна")
    root.geometry('400x400')
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    if world == "print":
        txt = 'Hello World'
    else:
        txt = world

    label = Label(root, text=txt)
    label.place(x=200, y=10)

    buton = Button(root, text="test button", command=newbtn(root))
    buton.place(x=150, y=80)


    root.mainloop()

if __name__ == "__main__":
    HelloWorld("print")
