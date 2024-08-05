import tkinter as tk

class DraggableFrame(tk.Frame):
    def __init__(self, parent, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = tk.Label(self, text=text)
        self.label.pack(expand=True, fill=tk.BOTH)
        self.label.bind("<Button-1>", self.on_click)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.parent = parent

    def on_click(self, event):
        self._drag_data = {"x": event.x, "y": event.y}

    def on_drag(self, event):
        x = self.winfo_x() - self._drag_data["x"] + event.x
        y = self.winfo_y() - self._drag_data["y"] + event.y
        self.place(x=x, y=y)
        self._reorder()

    def _reorder(self):
        for child in self.parent.winfo_children():
            if isinstance(child, DraggableFrame) and child != self:
                if self.winfo_x() < child.winfo_x():
                    self.lower(child)
                else:
                    self.lift(child)

root = tk.Tk()
frames = []
for i in range(10):
    frame = DraggableFrame(root, text=f"Frame {i+1}", width=80, height=80, bd=1, relief=tk.SOLID)
    frame.place(x=i*80, y=10)
    frames.append(frame)