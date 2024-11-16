from tkinter import Tk, Button, Scale, Canvas, Label, StringVar, Entry, Toplevel, messagebox
from tkinter.colorchooser import askcolor
from PIL import Image
import os

class Filenappopup:
    def __init__(self, master):
        top = self.top = Toplevel(master, bg="#3b3b3b")
        self.lbl = Label(top, text='Choose a filename', bg="#3b3b3b", fg="white", font=("Arial", 12))
        self.lbl.pack(pady=5)
        self.ent_filename = Entry(top, font=("Arial", 12))
        self.ent_filename.pack(pady=5)
        self.btn_ok = Button(top, text='OK', command=self.cleanup, bg="#5a5a5a", fg="white", font=("Arial", 10))
        self.btn_ok.pack(pady=5)

    def cleanup(self):
        self.filename = self.ent_filename.get()
        self.top.destroy()

class Paint:
    DEFAULT_PENSIZE = 6.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.configure(bg="#3b3b3b")
        self.root.title("Paint - Godot Styled")

        self.setup_ui()
        self.setup()
        
        self.root.mainloop()

    def setup_ui(self):
        # Toolbar
        self.pen_button = self.create_button("Pen", self.use_pen, 0, 0)
        self.brush_button = self.create_button("Brush", self.use_brush, 0, 1)
        self.color_button = self.create_button("Color", self.choose_color, 0, 2)
        self.eraser_button = self.create_button("Eraser", self.use_eraser, 0, 3)
        self.size_scale = Scale(self.root, from_=1, to=10, orient='horizontal', bg="#5a5a5a", fg="white",
                                font=("Arial", 10), highlightbackground="#3b3b3b", troughcolor="#7a7a7a")
        self.size_scale.grid(row=0, column=4, padx=5, pady=5)

        self.line_button = self.create_button("Line", self.use_line, 1, 0)
        self.poly_button = self.create_button("Polygon", self.use_poly, 1, 1)
        self.clear_button = self.create_button("Clear", lambda: self.c.delete("all"), 1, 2)
        self.save_button = self.create_button("Save", self.save_file, 1, 3)

        # Canvas
        self.c = Canvas(self.root, bg="#2b2b2b", width=600, height=600, highlightthickness=0)
        self.c.grid(row=2, columnspan=5, pady=10)

        # Status Label
        self.var_status = StringVar(value='Selected: Pen')
        self.lbl_status = Label(self.root, textvariable=self.var_status, bg="#3b3b3b", fg="white",
                                font=("Arial", 10))
        self.lbl_status.grid(row=3, columnspan=5, pady=5)

    def create_button(self, text, command, row, column):
        button = Button(self.root, text=text, command=command, bg="#5a5a5a", fg="white",
                        font=("Arial", 10), activebackground="#7a7a7a", activeforeground="white")
        button.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        return button

    def setup(self):
        self.old_x, self.old_y = None, None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = None
        self.size_multiplier = 1

        self.set_active_button(self.pen_button)

        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('<Button-1>', self.point)
        self.root.bind('<Escape>', self.line_reset)
        self.line_start = (None, None)

    def use_pen(self):
        self.set_active_button(self.pen_button)
        self.size_multiplier = 1

    def use_brush(self):
        self.set_active_button(self.brush_button)
        self.size_multiplier = 2.5

    def use_line(self):
        self.set_active_button(self.line_button)

    def use_poly(self):
        self.set_active_button(self.poly_button)

    def choose_color(self):
        self.eraser_on = False
        color = askcolor(color=self.color)

        if color[1]:
            self.color = color[1]

    def use_eraser(self):
        self.set_active_button(self.eraser_button, eraser_mode=True)

    def set_active_button(self, button, eraser_mode=False):
        if self.active_button:
            self.active_button.config(relief='raised')
        button.config(relief='sunken')
        self.active_button = button
        self.eraser_on = eraser_mode
        self.var_status.set(f"Selected: {button['text']}")

    def paint(self, event):
        line_width = self.size_scale.get() * self.size_multiplier
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=line_width, fill=paint_color,
                               capstyle='round', smooth=True, splinesteps=36)
        self.old_x, self.old_y = event.x, event.y

    def point(self, event):
        self.old_x, self.old_y = event.x, event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def line_reset(self, event):
        self.line_start = (None, None)

    def save_file(self):
        self.popup = Filenappopup(self.root)
        self.root.wait_window(self.popup.top)

        filename = self.popup.filename + '.png'
        if not filename or (os.path.exists(filename) and not messagebox.askyesno("Overwrite?", "File exists. Overwrite?")):
            return

        postscript_file = filename.replace('.png', '.eps')
        self.c.postscript(file=postscript_file)
        Image.open(postscript_file).save(filename, 'png')
        os.remove(postscript_file)
        messagebox.showinfo("Save", "File saved successfully!")

if __name__ == '__main__':
    Paint()