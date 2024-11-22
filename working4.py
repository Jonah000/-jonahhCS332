from tkinter import Frame, Tk, Button, Scale, Canvas, Label, StringVar, Entry, Toplevel, messagebox
from tkinter.colorchooser import askcolor
from PIL import Image
import os

class Filenappopup:
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.lbl = Label(top, text='choose a filename')
        self.lbl.pack()
        self.ent_filename = Entry(top)
        self.ent_filename.pack()
        self.btn_ok = Button(top, text='ok', command=self.cleanup)
        self.btn_ok.pack()

    def cleanup(self):
        self.filename = self.ent_filename.get()
        self.top.destroy()

class Paint(object):
    DEFAULT_PENSIZE = 6.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("Paint Application")

        self.setup()

        # Create a frame for the buttons on the left side
        self.button_frame = Frame(self.root, bg="#5C9EAD")
        self.button_frame.grid(row=0, column=0, sticky='ns')

        # Buttons and controls
        self.pen_button = Button(self.button_frame, text='Pen', command=self.use_pen, bg="#5C9EAD", fg="white")
        self.pen_button.grid(row=0, column=0, sticky='ew')

        self.brush_button = Button(self.button_frame, text='Brush', command=self.use_brush, bg="#5C9EAD", fg="white")
        self.brush_button.grid(row=1, column=0, sticky='ew')

        self.color_button = Button(self.button_frame, text='Color', command=self.choose_color, bg="#5C9EAD", fg="white")
        self.color_button.grid(row=2, column=0, sticky='ew')

        self.eraser_button = Button(self.button_frame, text='Eraser', command=self.use_eraser, bg="#5C9EAD", fg="white")
        self.eraser_button.grid(row=3, column=0, sticky='ew')

        self.size_scale = Scale(self.button_frame, from_=1, to=10, orient='horizontal', bg="#5C9EAD", fg="white")
        self.size_scale.grid(row=4, column=0, sticky='ew')

        self.line_button = Button(self.button_frame, text='Line', command=self.use_line, bg="#5C9EAD", fg="white")
        self.line_button.grid(row=5, column=0, sticky='ew')

        self.poly_button = Button(self.button_frame, text='Polygon', command=self.use_poly, bg="#5C9EAD", fg="white")
        self.poly_button.grid(row=6, column=0, sticky='ew')

        self.clear_button = Button(self.button_frame, text='Clear', command=lambda: self.c.delete("all"), bg="#5C9EAD", fg="white")
        self.clear_button.grid(row=7, column=0, sticky='ew')

        self.save_button = Button(self.button_frame, text='Save', command=self.save_file, bg="#5C9EAD", fg="white")
        self.save_button.grid(row=8, column=0, sticky='ew')

        # Canvas
        self.c = Canvas(self.root, bg="#D9D9D9", width=600, height=600)
        self.c.grid(row=0, column=1)

        self.var_status = StringVar(value='Selected: Pen')
        self.lbl_status = Label(self.root, textvariable=self.var_status, bg="#D9D9D9")
        self.lbl_status.grid(row=1, column=1, sticky='ew')

        self.set_active_button(self.pen_button)

        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('<Button-1>', self.point)
        self.root.bind('<Escape>', self.line_reset)
        self.line_start = (None, None)

        self.root.mainloop()

    def setup(self):
        self.old_x, self.old_y = None, None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = None
        self.size_multiplier = 1

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
        if color[1] is not None:
            self.color = color[1]

    def use_eraser(self):
        self.set_active_button(self.eraser_button, eraser_mode=True)

    def set_active_button(self, some_button, eraser_mode=False):
        if self.active_button:
            self.active_button.config(relief='raised')
        some_button.config(relief='sunken')
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        line_width = self.size_scale.get() * self.size_multiplier
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=line_width, fill=paint_color, capstyle='round', smooth=True, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def point(self, event):
        pass

    def save_file(self):
        pass

    def line_reset(self, event):
        pass


if __name__ == '__main__':
    Paint()