from tkinter import Tk, Button, Canvas, Label, Scale, filedialog, colorchooser
from PIL import Image, ImageDraw, ImageTk
import os

class Paint:
    DEFAULT_PENSIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("Paint")
        self.color = self.DEFAULT_COLOR
        self.brush_size = self.DEFAULT_PENSIZE
        self.setup_gui()
        self.setup_canvas()
        self.old_x, self.old_y = None, None
        self.draw = None  # For saving images
        self.root.mainloop()

    def setup_gui(self):
        # Toolbar for tools
        self.toolbar = Canvas(self.root, height=40, bg="lightgray")
        self.toolbar.pack(side='top', fill='x')

        self.pen_button = Button(self.toolbar, text='🖊️', command=self.use_pen, width=2)
        self.pen_button.grid(row=0, column=0, padx=5)

        self.brush_button = Button(self.toolbar, text='🖌️', command=self.use_brush, width=2)
        self.brush_button.grid(row=0, column=1, padx=5)

        self.color_button = Button(self.toolbar, text='🎨', command=self.choose_color, width=2)
        self.color_button.grid(row=0, column=2, padx=5)

        self.eraser_button = Button(self.toolbar, text='🧽', command=self.use_eraser, width=2)
        self.eraser_button.grid(row=0, column=3, padx=5)

        self.clear_button = Button(self.toolbar, text='🗑️', command=self.clear_canvas, width=2)
        self.clear_button.grid(row=0, column=4, padx=5)

        self.save_button = Button(self.toolbar, text='💾', command=self.save_image, width=2)
        self.save_button.grid(row=0, column=5, padx=5)

        self.size_scale = Scale(self.toolbar, from_=1, to=10, orient='horizontal', label='Size')
        self.size_scale.grid(row=0, column=6, padx=10)

        # Add a color palette
        self.palette_frame = Canvas(self.root, height=40, bg="white")
        self.palette_frame.pack(side='top', fill='x')

        colors = ["black", "gray", "red", "green", "blue", "yellow", "orange", "purple"]
        for idx, color in enumerate(colors):
            btn = Button(self.palette_frame, bg=color, width=2, command=lambda col=color: self.set_color(col))
            btn.grid(row=0, column=idx, padx=5)

    def setup_canvas(self):
        # Main drawing canvas
        self.canvas = Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack(fill='both', expand=True)

        # Set up mouse bindings
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset_position)

        # Image setup for saving
        self.image = Image.new('RGB', (800, 600), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def use_pen(self):
        self.set_active_tool('pen')

    def use_brush(self):
        self.set_active_tool('brush')

    def use_eraser(self):
        self.set_active_tool('eraser')

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.color = color_code

    def set_color(self, color):
        self.color = color

    def set_active_tool(self, tool):
        self.active_tool = tool

    def paint(self, event):
        x, y = event.x, event.y
        size = self.size_scale.get()
        if self.old_x and self.old_y:
            fill_color = 'white' if self.active_tool == 'eraser' else self.color
            self.canvas.create_line(self.old_x, self.old_y, x, y, width=size, fill=fill_color, capstyle='round')
            self.draw.line([self.old_x, self.old_y, x, y], fill=fill_color, width=size)
        self.old_x, self.old_y = x, y

    def reset_position(self, event):
        self.old_x, self.old_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, 800, 600], fill="white")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)

if __name__ == '__main__':
    Paint()