from tkinter import *
import main
import pickle
root = Tk()

Label(root, text="Transform").pack()
vars = {}
layers = []
frame = Frame(root)
frame.pack()
rownum = 0
def addLayer():
    global layers, rownum
    layers.append(transformlayer(rownum))
    rownum += 1

class transformlayer:
    def __init__ (self,rownum):
        self.name = StringVar()
        self.args = StringVar()
        Label(frame, text= "Name of layer:").grid(row=rownum, column=0)
        OptionMenu(frame, self.name, *main.transformlist).grid(row=rownum, column=1)
        Label(frame, text= "Arguments to layer:").grid(row=rownum, column=2)
        Entry(frame, textvariable= self.args).grid(row=rownum, column=3)

Button(root, text= "Add Transform Layer", command= addLayer).pack()

def savetransform(vars):
    for i in layers:
        vars[i.name.get()] = i.args.get()
    list = [main.ImageTransform(vars)]
    with open("ModelTransform", "wb") as txt:
        pickle.dump(list, txt)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", lambda: savetransform(vars))


root.mainloop()