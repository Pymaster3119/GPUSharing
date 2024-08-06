from tkinter import *
import tkscrolledframe
from tkinter import ttk
import main
import pickle

root = Tk()

Label(root, text="Transform").pack()
vars = {}
layers = []
masterframe = tkscrolledframe.ScrolledFrame(root)
masterframe.pack()
frame = masterframe.display_widget(Frame)
rownum = 0

def addLayer():
    global layers, rownum
    frametemp = DraggableFrame(frame)
    frametemp.pack()
    layers.append(frametemp)
    rownum += 1

def animate_move(frame, target_x, target_y):
    x, y = frame.winfo_x(), frame.winfo_y()
    dx = (target_x - x) / 5
    dy = (target_y - y) / 5
    for _ in range(5):
        x += dx
        y += dy
        frame.place(x=x, y=y)
        frame.update()
        root.after(5)

def reorder_frames():
    layers.sort(key=lambda frame: frame.winfo_y())
    for idx, frame in enumerate(layers):
        animate_move(frame, 10, idx*80)

class DraggableFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.name = StringVar()
        self.args = StringVar()
        Label(self, text="Name of layer:").grid(row=0, column=0)
        OptionMenu(self, self.name, *main.transformlist).grid(row=0, column=1)
        Label(self, text="Arguments to layer:").grid(row=0, column=2)
        Entry(self, textvariable=self.args).grid(row=0, column=3)
        for child in self.winfo_children():
            child.bind("<Button-1>", self.on_click)
            child.bind("<B1-Motion>", self.on_drag)
            child.bind("<ButtonRelease-1>", self.on_release)
        self.parent = parent

    def on_click(self, event):
        self._drag_data = {"x": event.x, "y": event.y}

    def on_drag(self, event):
        x = self.winfo_x() - self._drag_data["x"] + event.x
        y = self.winfo_y() - self._drag_data["y"] + event.y
        self.place(x=x, y=y)

    def on_release(self, event):
        self._lock_to_grid()

    def _lock_to_grid(self):
        y = self.winfo_y()
        new_y = round(y / 80) * 80
        self.place(x=10, y=new_y)
        reorder_frames()

Button(root, text="Add Transform Layer", command=addLayer).pack()

def savetransform(vars):
    try:
        for i in layers:
            vars[i.name.get()] = i.args.get()
        list = [main.ImageTransform(vars)]
        with open("ModelTransform", "wb") as txt:
            pickle.dump(list, txt)
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", lambda: savetransform(vars))
root.mainloop()
