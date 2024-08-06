import tkinter as tk

class DraggableFrame(tk.Frame):
    def __init__(self, parent, labels, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        for text in labels:
            label = tk.Label(self, text=text)
            label.pack(expand=True, fill=tk.BOTH)
            label.bind("<Button-1>", self.on_click)
            label.bind("<B1-Motion>", self.on_drag)
            label.bind("<ButtonRelease-1>", self.on_release)
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

root = tk.Tk()
root.title("Draggable Frames")
root.geometry("150x800")
frames = []

for i in range(10):
    frame = DraggableFrame(root, labels=[f"Frame {i+1}", f"Label {i+1}.1", f"Label {i+1}.2"], width=120, height=80, bd=1, relief=tk.SOLID)
    frame.place(x=10, y=i*80)
    frames.append(frame)

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
    frames.sort(key=lambda frame: frame.winfo_y())
    for idx, frame in enumerate(frames):
        animate_move(frame, 10, idx*80)

root.mainloop()