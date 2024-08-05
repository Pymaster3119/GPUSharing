import main
import pickle
layers = []

from tkinter import *

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
    frames.sort(key=lambda frame: frame.winfo_x())
    for idx, frame in enumerate(frames):
        animate_move(frame, idx*80, 10)

class DraggableFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.type = StringVar(self)
        self.arg1 = StringVar()
        self.arg2 = StringVar()
        Label(super(), text="Type of layer:").grid(row=0, column=0)
        Label(super(), textvariable=self.type).grid(row=1, column=0)
        Label(super(), text="Input Size:").grid(row=0, column=1)
        Label(super(), textvariable=self.arg1).grid(row=1, column=1)
        Label(super(), text="Output Size:").grid(row=0, column=2)
        Label(super(), textvariable=self.arg1).grid(row=1, column=2)
        super().__init__(parent, *args, **kwargs)
        for child in self.winfo_children():
            child.pack(expand=True, fill=BOTH)
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
        x = self.winfo_x()
        new_x = round(x / 80) * 80
        self.place(x=new_x, y=10)
        reorder_frames()

root = Tk()
frames = []
for i in range(10):
    frame = DraggableFrame(root)
    frame.place(x=i*80, y=10)
    frames.append(frame)

def savelayers(layers):
    with open("Model", "wb") as txt:
        pickle.dump(layers, txt)
root.protocol("WM_DELETE_WINDOW", lambda: savelayers(layers))
root.mainloop()