from tkinter import Tk, Button, Scale, Canvas, Label, StringVar, Entry, Toplevel, messagebox
from tkinter.colorchooser import askcolor
from PIL import Image
import os

class Filenappopup:
    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.title("Save File")
        self.lbl = Label(top, text='Choose a filename:', font=("Helvetica", 12))
        self.lbl.pack(pady=5)
        self.ent_filename = Entry(top, width=30, font=("Helvetica", 12))
        self.ent_filename.pack(pady=5)
        self.btn_ok = Button(top, text='OK', command=self.cleanup, bg="#4CAF50", fg="white", font=("Helvetica", 10))
        self.btn_ok.pack(pady=5)

    def cleanup(self):
        self.filename = self.ent_filename.get()
        self.top.destroy()

class Paint(object):
    DEFAULT_PENSIZE = 6.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("Smooth Paint Application")
        self.root.geometry("700x700")
        self.root.configure(bg="#f0f0f0")
        self.setup()

        button_style = {"font": ("Helvetica", 10), "bg": "#4CAF50", "fg": "white", "relief": "raised", "width": 8}
        
        self.pen_button = Button(self.root, text='Pen', command=self.use_pen, **button_style)
        self.pen_button.grid(row=0, column=0, padx=5, pady=5)

        self.brush_button = Button(self.root, text='Brush', command=self.use_brush, **button_style)
        self.brush_button.grid(row=0, column=1, padx=5, pady=5)

        self.color_button = Button(self.root, text='Color', command=self.choose_color, **button_style)
        self.color_button.grid(row=0, column=2, padx=5, pady=5)

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser, **button_style)
        self.eraser_button.grid(row=0, column=3, padx=5, pady=5)

        self.size_scale = Scale(self.root, from_=1, to=10, orient='horizontal', font=("Helvetica", 10), bg="#f0f0f0")
        self.size_scale.grid(row=0, column=4, padx=5, pady=5)

        self.line_button = Button(self.root, text='Line', command=self.use_line, **button_style)
        self.line_button.grid(row=1, column=0, padx=5, pady=5)

        self.poly_button = Button(self.root, text='Polygon', command=self.use_poly, **button_style)
        self.poly_button.grid(row=1, column=1, padx=5, pady=5)

        self.clear_button = Button(self.root, text='Clear', command=lambda: self.c.delete("all"), **button_style)
        self.clear_button.grid(row=1, column=2, padx=5, pady=5)

        self.save_button = Button(self.root, text='Save', command=self.save_file, **button_style)
        self.save_button.grid(row=1, column=3, padx=5, pady=5)

        self.c = Canvas(self.root, bg='white', width=600, height=600, highlightbackground="#cccccc", bd=0)
        self.c.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

        self.var_status = StringVar(value='Selected: Pen')
        self.lbl_status = Label(self.root, textvariable=self.var_status, font=("Helvetica", 10), bg="#f0f0f0")
        self.lbl_status.grid(row=3, column=0, columnspan=5, pady=5)

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
        if color[1]:
            self.color = color[1]

    def use_eraser(self):
        self.set_active_button(self.eraser_button, eraser_mode=True)

    def set_active_button(self, some_button, eraser_mode=False):
        if self.active_button:
            self.active_button.config(relief='raised')
        some_button.config(relief='sunken')
        self.active_button = some_button
        self.eraser_on = eraser_mode
        self.var_status.set(f"Selected: {some_button['text']}")

    def paint(self, event):
        line_width = self.size_scale.get() * self.size_multiplier
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=line_width, fill=paint_color, capstyle='round', smooth=True)
        self.old_x = event.x
        self.old_y = event.y

    def point(self, event):
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def line_reset(self, event):
        self.line_start = (None, None)

    def save_file(self):
        self.popup = Filenappopup(self.root)
        self.root.wait_window(self.popup.top)
        file_name = self.popup.filename + ".png"
        if not os.path.exists(file_name) or messagebox.askyesno("Overwrite?", "File exists. Overwrite?"):
            self.c.postscript(file="temp.eps")
            img = Image.open("temp.eps")
            img.save(file_name)
            os.remove("temp.eps")
            messagebox.showinfo("File Save", "File saved successfully.")

if __name__ == '__main__':
    Paint()