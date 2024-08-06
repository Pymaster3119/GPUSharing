from tkinter import *
import main
root = Tk()

Label(root, text="Transform").pack()
vars = {}
frame = Frame(root)
frame.pack()
rownum = 0
def addLayer():
    global vars, rownum
    name = StringVar()
    args = StringVar()
    vars[name] = args
    Label(frame, text= "Name of layer:").grid(row=rownum, column=0)
    Entry(frame, textvariable= name).grid(row=rownum, column=1)
    Label(frame, text= "Arguments to layer:").grid(row=rownum, column=2)
    Entry(frame, textvariable= name).grid(row=rownum, column=3)

Button(root, text= "Add Transform Layer", command= addLayer).pack()

def savetransform(vars):
    main.ImageTransform(vars)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", lambda: savetransform(vars))


root.mainloop()