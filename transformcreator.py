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
    tempframe = DraggableFrame(frame)
    tempframe.grid(row=rownum, column=0)
    layers.append(tempframe)
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
        animate_move(frame, 0, idx * 80)

class DraggableFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
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

    def on_click(self, event):
        self._drag_data = {"x": event.x, "y": event.y}

    def on_drag(self, event):
        x = self.winfo_x() - self._drag_data["x"] + event.x
        y = self.winfo_y() - self._drag_data["y"] + event.y
        self.place(x=x, y=y)
        self._confine_within_parent()

    def on_release(self, event):
        self._lock_to_grid()

    def _lock_to_grid(self):
        y = self.winfo_y()
        new_y = round(y / 80) * 80
        self.place(x=0, y=new_y)
        reorder_frames()

    def _confine_within_parent(self):
        x, y = self.winfo_x(), self.winfo_y()
        width, height = self.winfo_width(), self.winfo_height()
        parent_width, parent_height = self.parent.winfo_width(), self.parent.winfo_height()
        new_x = max(0, min(x, parent_width - width))
        new_y = max(0, min(y, parent_height - height))
        self.place(x=new_x, y=new_y)

Button(root, text="Add Transform Layer", command=addLayer).pack()

def savetransform(vars):
    try:
        for i in layers:
            vars[i.name.get()] = i.args.get()
        list = [main.ImageTransform(vars)]
        with open("ModelTransform", "wb") as txt:
            pickle.dump(list, txt)
    except Exception as e:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", lambda: savetransform(vars))

root.mainloop()
