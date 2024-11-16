from tkinter import Tk, Button, Scale, Canvas, Label, StringVar, Entry, Toplevel, messagebox
from tkinter.colorchooser import askcolor
from PIL import Image
import os
import PIL
print(PIL.__file__)

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
        self.setup()  

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0, sticky='ew')

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1, sticky='ew')

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2, sticky='ew')

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3, sticky='ew')

        self.size_scale = Scale(self.root, from_=1, to=10, orient='horizontal')
        self.size_scale.grid(row=0, column=4, sticky='ew')

        self.line_button = Button(self.root, text='Line', command=self.use_line)
        self.line_button.grid(row=1, column=0, sticky='ew')

        self.poly_button = Button(self.root, text='Polygon', command=self.use_poly)
        self.poly_button.grid(row=1, column=1, sticky='ew')

        self.black_button = Button(self.root, text='', bg='black', activebackground="black")
        self.black_button.grid(row=1, column=2, sticky='ew')

        self.clear_button = Button(self.root, text='clear', command=lambda: self.c.delete("all"))
        self.clear_button.grid(row=1, column=3, sticky='ew')

        self.save_button = Button(self.root, text='save', command=self.save_file)
        self.save_button.grid(row=1, column=4, sticky='ew')

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=2, columnspan=5)

        self.var_status = StringVar(value='selected: pen')
        self.lbl_status = Label(self.root, textvariable=self.var_status)
        self.lbl_status.grid(row=3, column=4, rowspan=3)

        
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

        if color is not None:
            self.color = color[1]

    def use_eraser(self):
        self.set_active_button(self.eraser_button, eraser_mode=True)
    
    def set_active_button(self, some_button, eraser_mode=False):
        self.set_status()

        if self.active_button:
            self.active_button.config(relief='raised')
        
        some_button.config(relief='sunken')
        self.active_button = some_button 
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.set_status(event.x, event.y)
        line_width = self.size_scale.get() * self.size_multiplier
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=line_width, fill=paint_color, capstyle='round', smooth=True, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def line(self, x, y):  
        line_width = self.size_scale.get() * self.size_multiplier
        paint_color = 'white' if self.eraser_on else self.color
        
        self.c.create_line(self.line_start[0], self.line_start[1], x, y, width=line_width, fill=paint_color, capstyle='round', smooth=True, splinesteps=36)
    
    def point(self, event):
        self.set_status(event.x, event.y)
        btn = self.active_button["text"]
        if btn in ("Line", "Polygon"):  
            self.size_multiplier = 1
            if any(self.line_start):
                self.line(event.x, event.y)
                self.line_start = ((None, None) if btn == 'Line' else (event.x, event.y))
            else:
                self.line_start = (event.x, event.y)

    def reset(self, event):
        self.old_x, self.old_y = None, None
    
    def line_reset(self, event):
        self.line_start = (None, None)

    def set_status(self, x=None, y=None):
        if self.active_button is None: 
            return
        
        btn = self.active_button["text"]
        oldxy = self.line_start if btn in ("Line", "Polygon") else (self.old_x, self.old_y)
        self.var_status.set(f"selected: {btn}\n" + 
                            ((f"Old (x,y): {oldxy}\n(x,y): ({x},{y})") if x is not None and y is not None else ""))

    def save_file(self):
        self.popup = Filenappopup(self.root)
        self.save_button["state"] = "disabled"
        self.root.wait_window(self.popup.top)

        filepng = self.popup.filename + '.png' 

        if not os.path.exists(filepng) or messagebox.askyesno("File already exists", "Overwrite?"):
            fileps = self.popup.filename + '.eps'
            self.c.postscript(file=fileps)
            img = Image.open(fileps)
            img.save(filepng, 'png')
            os.remove(fileps)

            self.save_button["state"] = "normal"
            messagebox.showinfo("File save", "File saved")
        else:
            messagebox.showwarning("File save", "File not saved")

        self.save_button["state"] = "normal"

if __name__ == '__main__':
    Paint()
