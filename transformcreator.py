from tkinter import *
import pickle
import main
root = Tk()

Label(root, text="Transform").pack()
vars = {}
layers = []
frame = Frame(root)
frame.pack(fill=BOTH, expand=True)
rownum = 0

def addLayer():
    global layers, rownum
    frametemp = DraggableFrame(frame, rownum)
    frametemp.place(x=10, y=rownum*80)
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
    def __init__(self, parent, row, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.row = row
        self.type = StringVar()
        self.args = StringVar()
        self.init_ui()
        for child in self.winfo_children():
            child.bind("<Button-1>", self.on_click)
            child.bind("<B1-Motion>", self.on_drag)
            child.bind("<ButtonRelease-1>", self.on_release)
        self.parent = parent

    def init_ui(self):
        Label(self, text=f"Layer {self.row} Type: ").place(x=0, y=0, width=120)
        OptionMenu(self, self.type, *main.transformlist).place(x=120, y=0, width=120)
        Label(self, text=f"Layer {self.row} Type: ").place(x=240, y=0, width=120)
        Entry(self, textvariable=self.args).place(x=360, y=0, width=120)
        self.config(width=480, height=30, bd=1, relief="solid")

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
            vars[i.type.get()] = i.args.get()
        list = [main.ImageTransform(vars)]
        with open("ModelTransform", "wb") as txt:
            pickle.dump(list, txt)
    except Exception as e:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", lambda: savetransform(vars))
root.mainloop()
