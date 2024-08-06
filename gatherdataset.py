from tkinter import *
import tkscrolledframe
from tkinter import filedialog
import pickle
root = Tk()
masterframe = tkscrolledframe.ScrolledFrame(root)
masterframe.pack()
frame = masterframe.display_widget(Frame)
pathnumber = 0
paths = []
def addPath():
    global pathnumber, paths
    pathnumber += 1
    Label(frame, text="Type " + str(pathnumber)).grid(row=pathnumber, column=0)
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File for Images", filetypes = (("Zip files", "*.zip")))
    Label(frame, text=paths).grid(row=pathnumber, column=1)
    paths.append(filename)
Button(root, text="Add new type", command=addPath).pack()
def save():
    with open("paths", "wb") as txt:
        pickle.dump(paths, txt)
root.protocol("WM_DELETE_WINDOW", save)
root.mainloop()