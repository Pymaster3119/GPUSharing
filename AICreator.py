import main
from tkinter import *
import pickle
layers = []
root = Tk()

type = StringVar(root)
arg1 = StringVar(root)
arg2 = StringVar(root)

Entry(root, textvariable=type).pack()
Entry(root, textvariable=arg1).pack()
Entry(root, textvariable=arg2).pack()
Button(root, text= "Create value", command= lambda: layers.append(main.AILayer(type.get(), arg1.get(), arg2.get()))).pack()

def savelayers(layers):
    with open("Model", "wb") as txt:
        pickle.dump(layers, txt)
    root.destroy()
root.protocol("WM_DELETE_WINDOW", lambda: savelayers(layers))
root.mainloop()