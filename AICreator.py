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
        animate_move(frame, idx*160, 10)

class DraggableFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.type = StringVar(value=f"Type {len(frames) + 1}")
        self.arg1 = StringVar(value=f"Input {len(frames) + 1}")
        self.arg2 = StringVar(value=f"Output {len(frames) + 1}")
        Label(self, text="Type of layer:").grid(row=0, column=0)
        Entry(self, textvariable=self.type).grid(row=0, column=1)
        Label(self, text="Input Size:").grid(row=1, column=0)
        Entry(self, textvariable=self.arg1).grid(row=1, column=1)
        Label(self, text="Output Size:").grid(row=2, column=0)
        Entry(self, textvariable=self.arg2).grid(row=2, column=1)
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
        x = self.winfo_x()
        new_x = round(x / 160) * 160
        self.place(x=new_x, y=10)
        reorder_frames()

root = Tk()
frames = []
for i in range(10):
    frame = DraggableFrame(root, width = 160, height = 160)
    frame.place(x=i*160, y=10)
    frames.append(frame)

def savelayers(layers):
    for i in frames:
        layers.append(main.AILayer(i.type, i.arg1, i.arg2))
    with open("Model", "wb") as txt:
        pickle.dump(layers, txt)
root.protocol("WM_DELETE_WINDOW", lambda: savelayers(layers))
root.mainloop()