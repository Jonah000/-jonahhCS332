from tkinter import Tk, Button, Scale, Canvas, Label, StringVar, Entry, Toplevel, messagebox, Listbox, Scrollbar, PhotoImage
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw, ImageTk
from PIL import Image as PILImage
from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtCore import Qt
import os

class Paint:
    DEFAULT_COLOR = 'black'
    GRID_SIZE = 16
    PIXEL_SIZE = 30

    def __init__(self):
        self.root = Tk()
        self.root.title("GoDraw Sprite Editor")

        # Initialize attributes
        self.layers = []  # List of canvases for layers
        self.active_layer_index = 0
        self.color = self.DEFAULT_COLOR
        self.canvas_width = self.GRID_SIZE * self.PIXEL_SIZE
        self.canvas_height = self.GRID_SIZE * self.PIXEL_SIZE
        self.canvas_size = (self.canvas_width, self.canvas_height)

        self.logo_path = r"C:\Users\J. Jonah Gamerson\OneDrive\Documents\Logo.png"
        self.logo_image = None

        # GUI Setup
        self.setup_ui()

        # Create the first (base) layer
        self.add_layer()

        self.root.mainloop()

    def setup_ui(self):
        """Setup UI components."""

        try:
            self.logo_image = Image.open(self.logo_path)
            self.logo_image = self.logo_image.resize((200, 100), Image.LANCZOS)  # Adjust size as needed
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = Label(self.root, image=self.logo_photo)
            self.logo_label.grid(row=0, column=4, columnspan=5, pady=10)  # Adjust columnspan and pady as needed
        except Exception as e:
            print(f"Error loading logo image: {e}")
        
        self.pen_button = Button(self.root, text='Pen', command=self.use_pen, bg="#5C9EAD", fg="white")
        self.pen_button.grid(row=0, column=0, sticky='ew')

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser, bg="#5C9EAD", fg="white")
        self.eraser_button.grid(row=0, column=1, sticky='ew')

        self.color_button = Button(self.root, text='Color', command=self.choose_color, bg="#5C9EAD", fg="white")
        self.color_button.grid(row=1, column=0, sticky='ew')

        self.size_scale = Scale(self.root, from_=1, to=10, orient='horizontal', bg="#5C9EAD", fg="white")
        self.size_scale.grid(row=1, column=1, sticky='ew')

        self.add_layer_button = Button(self.root, text='Add Layer', command=self.add_layer, bg="#5C9EAD", fg="white")
        self.add_layer_button.grid(row=2, column=0, sticky='ew')

        self.clear_button = Button(self.root, text='Clear Layer', command=self.clear_canvas, bg="#5C9EAD", fg="white")
        self.clear_button.grid(row=2, column=1, sticky='ew')

        self.save_button = Button(self.root, text='Save', command=self.save_file, bg="#5C9EAD", fg="white")
        self.save_button.grid(row=3, column=0, sticky='ew')

        self.merge_button = Button(self.root, text='Merge Layers', command=self.merge_layers, bg="#5C9EAD", fg="white")
        self.merge_button.grid(row=3, column=1, sticky='ew')

        self.flood_fill_button = Button(self.root, text='Flood Fill', command=self.use_flood_fill, bg="#5C9EAD", fg="white")
        self.flood_fill_button.grid(row=4, column=0, sticky='ew')

        # Listbox for layer selection
        self.layer_listbox = Listbox(self.root, height=5)
        self.layer_listbox.grid(row=5, column=0, sticky='nsew')
        self.layer_listbox.bind('<<ListboxSelect>>', self.switch_layer)

        # Status label
        self.var_status = StringVar(value='Selected Tool: Pen')
        self.lbl_status = Label(self.root, textvariable=self.var_status)
        self.lbl_status.grid(row=0, column=10, columnspan=4, sticky='ew')

        self.save_frame_button = Button(self.root, text="Save Frame", command=self.save_frame, bg="#5C9EAD", fg="white")
        self.save_frame_button.grid(row=1, column=10, sticky='ew')

        self.play_button = Button(self.root, text="Play Animation", command=self.play_animation, bg="#5C9EAD", fg="white")
        self.play_button.grid(row=2, column=10, sticky='ew')

        self.stop_button = Button(self.root, text="Stop Animation", command=self.stop_animation, bg="#5C9EAD", fg="white")
        self.stop_button.grid(row=3, column=10, sticky='ew')

        self.export_button = Button(self.root, text="Export GIF", command=self.export_as_gif, bg="#5C9EAD", fg="white")
        self.export_button.grid(row=4, column=10, sticky='ew')

        # Frame listbox for management
        self.frames = []  # List to store frame file paths
        self.frame_listbox = Listbox(self.root, height=5)
        self.frame_listbox.grid(row=6, column=0, columnspan=4, sticky='nsew')
        frame_panel = Canvas(self.root, width=150, height=self.canvas_height, bg="lightgray")
        frame_panel.grid(row=3, column=4, rowspan=2, sticky='nsew')
        scrollbar = Scrollbar(self.root, orient="vertical", command=frame_panel.yview)
        scrollbar.grid(row=5, column=3, rowspan=2, sticky='ns')
        frame_panel.configure(yscrollcommand=scrollbar.set)
        self.frame_panel = frame_panel
        self.frame_thumbnails = []  # To store thumbnails
        self.frame_panel.bind('<Button-1>', self.select_frame)
        

    def draw_grid(self, canvas):
        """Draw the grid on a given canvas."""
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x1 = col * self.PIXEL_SIZE
                y1 = row * self.PIXEL_SIZE
                x2 = x1 + self.PIXEL_SIZE
                y2 = y1 + self.PIXEL_SIZE
                canvas.create_rectangle(x1, y1, x2, y2, outline="lightgray", fill="white",
                                        tags=(f"pixel-{row}-{col}", "grid"))
    
    def add_layer(self):
        """Adds a new layer to the application."""
        # Create a new canvas (layer)
        new_canvas = Canvas(self.root, width=self.GRID_SIZE * self.PIXEL_SIZE,
                            height=self.GRID_SIZE * self.PIXEL_SIZE, bg="white")

        # Hide the current active layer (if any)
        if self.layers:
            self.layers[self.active_layer_index].grid_remove()

        # Add the new layer to the list and make it active
        self.layers.append(new_canvas)
        self.active_layer_index = len(self.layers) - 1
        new_canvas.grid(row=3, column=6, columnspan=4)

        # Add layer name to listbox
        self.layer_listbox.insert("end", f"Layer {len(self.layers)}")

        # Draw grid on the new layer
        self.draw_grid(new_canvas)

        # Bind events to the new canvas
        self.bind_canvas_events(new_canvas)

    def bind_canvas_events(self, canvas):
        """Bind events to the canvas for painting."""
        canvas.bind('<B1-Motion>', self.paint_pixel)  # Bind for painting while dragging
        canvas.bind('<Button-1>', self.paint_pixel)   # Bind for painting on click


    def switch_layer(self, event):
        """Switch to a selected layer."""
        selected_index = self.layer_listbox.curselection()
        if not selected_index:
            return

        # Hide the current layer
        if self.layers:
            self.layers[self.active_layer_index].grid_remove()

        # Show the selected layer
        self.active_layer_index = selected_index[0]
        self.layers[self.active_layer_index].grid(row=3, column=0, columnspan=4)


    
    def merge_layers(self):
        """Merge all layers into the active layer on the canvas."""
        if not self.layers:
            messagebox.showinfo("Merge Layers", "No layers to merge.")
            return

        # Get the active layer to merge everything onto
        active_canvas = self.layers[self.active_layer_index]

        # Loop through all layers and merge their contents onto the active canvas
        for i, canvas in enumerate(self.layers):
            if i == self.active_layer_index:
                continue  # Skip the active layer itself

            # Copy each pixel from this layer to the active layer
            for item in canvas.find_withtag("grid"):
                coords = canvas.coords(item)
                if len(coords) == 4:  # Only process rectangle items
                    x1, y1, x2, y2 = map(int, coords)
                    color = canvas.itemcget(item, "fill")
                    if color != "white":  # Ignore white pixels
                        active_canvas.itemconfig(f"pixel-{y1 // self.PIXEL_SIZE}-{x1 // self.PIXEL_SIZE}", fill=color)

        # Clear all other layers and keep only the active one
        for i, canvas in enumerate(self.layers):
            if i != self.active_layer_index:
                canvas.delete("all")

        # Reset layers list to only contain the active layer
        self.layers = [active_canvas]
        self.layer_listbox.delete(0, "end")
        self.layer_listbox.insert("end", "Merged Layer")
        self.active_layer_index = 0
        messagebox.showinfo("Merge Layers", "All layers merged into the active layer.")




    def bind_canvas_events(self, canvas):
        canvas.bind('<B1-Motion>', self.paint_pixel)
        canvas.bind('<Button-1>', self.paint_pixel)

    def paint_pixel(self, event):
        """Paint pixels on the canvas."""
        canvas = self.layers[self.active_layer_index]
        col = event.x // self.PIXEL_SIZE
        row = event.y // self.PIXEL_SIZE

        brush_size = self.size_scale.get()  # Get the brush size from the scale
        color = self.color if not self.eraser_on else "white"

        # Draw multiple pixels based on brush size
        for r in range(row, row + brush_size):
            for c in range(col, col + brush_size):
                # Ensure the drawn pixel is within the grid bounds
                if 0 <= c < self.GRID_SIZE and 0 <= r < self.GRID_SIZE:
                    canvas.itemconfig(f"pixel-{r}-{c}", fill=color)
    def rebind_canvas_events(self):
        """Reset canvas bindings to the default paint behavior."""
        for canvas in self.layers:
            self.bind_canvas_events(canvas)


    def clear_canvas(self):
        """Clear the entire current layer including the grid and any drawn pixels."""
        canvas = self.layers[self.active_layer_index]
        
        # Delete all items on the canvas (both grid and drawn pixels)
        canvas.delete("all")
        
        # Redraw the grid to the cleared canvas
        self.draw_grid(canvas)

    def flood_fill(self, event):
        """Flood-fill operation starting from the clicked pixel."""
        canvas = self.layers[self.active_layer_index]
        col = event.x // self.PIXEL_SIZE
        row = event.y // self.PIXEL_SIZE

    # Get the color of the starting pixel
        start_pixel_tag = f"pixel-{row}-{col}"
        start_color = canvas.itemcget(start_pixel_tag, "fill")

    # If the starting pixel is already the target color, do nothing
        if start_color == self.color:
            return

    # Stack for storing pixels to process
        stack = [(row, col)]

        while stack:
            r, c = stack.pop()
            pixel_tag = f"pixel-{r}-{c}"

            # Skip if pixel is out of bounds or already the target color
            if not (0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE):
                continue
            if canvas.itemcget(pixel_tag, "fill") != start_color:
                continue

            # Change the color of the current pixel
            canvas.itemconfig(pixel_tag, fill=self.color)

            # Add neighboring pixels to the stack
            stack.extend([(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)])
        
    def use_flood_fill(self):
        """Activate the flood-fill tool."""
        self.eraser_on = False
        self.var_status.set("Selected Tool: Flood Fill")
        for canvas in self.layers:
            canvas.bind('<Button-1>', self.flood_fill)

    def choose_color(self):
            """Choose a new drawing color."""
            self.eraser_on = False
            color = askcolor(color=self.color)
            if color[1]:
                self.color = color[1]
        
    def use_pen(self):
        """Switch to pen tool."""
        self.eraser_on = False
        self.var_status.set("Selected Tool: Pen")
        self.rebind_canvas_events()

    def use_eraser(self):
        """Switch to eraser tool."""
        self.eraser_on = True
        self.var_status.set("Selected Tool: Eraser")
        self.rebind_canvas_events()

#-------------------------------------------------- Frame/Animation Functionality --------------------------------------------

    def create_frame_thumbnail(self):
        """Generate a thumbnail from the current canvas."""
        # Get the current canvas
        canvas = self.layers[self.active_layer_index]
        
        # Create a blank PIL image to represent the canvas
        thumbnail_size = (128, 128)  # Thumbnail dimensions
        thumbnail_image = Image.new("RGB", self.canvas_size, "white")

        # Render the canvas onto the PIL image
        for item in canvas.find_withtag("grid"):
            coords = canvas.coords(item)
            if len(coords) == 4:
                x1, y1, x2, y2 = map(int, coords)
                color = canvas.itemcget(item, "fill")
                if color != "white":  # Ignore white pixels
                    thumbnail_image.paste(color, (x1, y1, x2, y2))

        # Resize the image to thumbnail size
        thumbnail_image = thumbnail_image.resize(thumbnail_size, Image.ANTIALIAS)

        # Convert the PIL image to a PhotoImage for use in Tkinter
        return ImageTk.PhotoImage(thumbnail_image)

    def save_frame(self):
        """Save the current canvas state as an in-memory frame."""
        canvas = self.layers[self.active_layer_index]
        frame_pixel_data = {}
        image = Image.new("RGBA", (self.canvas_width, self.canvas_height), "white")
        draw = ImageDraw.Draw(image)

        # Draw canvas items on the image
        for item in canvas.find_withtag("grid"):
            coords = canvas.coords(item)
            if len(coords) == 4:  # Handle rectangle items
                x1, y1, x2, y2 = map(int, coords)
                color = canvas.itemcget(item, "fill")
                if color != "white":
                    row = y1
                    col = x1
                    frame_pixel_data[(row, col)] = color
                    draw.rectangle([x1, y1, x2, y2], fill=color)

        self.frames.append({"image": thumbnail_image, "pixel_data": frame_pixel_data})

        # Save the image in the in-memory list
        self.frames.append(image)
        self.update_frame_panel()

        messagebox.showinfo("Save Frame", f"Frame {len(self.frames)} saved.")
    def delete_frame(self):
        """Delete a selected frame."""
        selected = self.frame_listbox.curselection()
        if selected:
            index = selected[0]
            os.remove(self.frames[index])  # Remove file
            del self.frames[index]  # Remove from list
            self.update_frame_list()


    def play_animation(self):
        """Play saved frames as an animation."""
        if not self.frames:
            messagebox.showinfo("Animation", "No frames to play.")
            return

        self.is_playing = True
        self.current_frame_index = 0
        self.animate_frames()

    def animate_frames(self):
        """Loop through frames for animation."""
        if not self.is_playing or self.current_frame_index >= len(self.frames):
            self.is_playing = False
            return

        # Convert the frame to a Tkinter-compatible image and display it
        frame_image = ImageTk.PhotoImage(self.frames[self.current_frame_index])
        canvas = self.layers[self.active_layer_index]
        canvas.delete("all")  # Clear canvas
        canvas.create_image(0, 0, image=frame_image, anchor="nw")
        self.current_frame_display = frame_image  # Keep reference to avoid garbage collection

        # Proceed to the next frame
        self.current_frame_index += 1
        self.root.after(100, self.animate_frames)  # Adjust speed as needed


    def stop_animation(self):
        """Stop the animation playback."""
        self.is_playing = False

    def update_frame_panel(self):
        """Update the frame panel with thumbnails of all frames."""
        self.frame_panel.delete("all")  # Clear the panel
        self.frame_thumbnails.clear()

        for i, frame in enumerate(self.frames):
            thumbnail = frame.copy()
            thumbnail.thumbnail((100, 100))  # Resize for thumbnail
            tk_image = ImageTk.PhotoImage(thumbnail)
            self.frame_thumbnails.append(tk_image)

            # Display thumbnail with a tag
            x, y = 10, 10 + i * 110  # Position each thumbnail
            self.frame_panel.create_image(x, y, image=tk_image, anchor="nw", tags=f"frame-{i}")
            self.frame_panel.create_text(x + 50, y + 100, text=f"Frame {i+1}", anchor="center", tags=f"frame-{i}")

        # Adjust scrolling region
        self.frame_panel.configure(scrollregion=self.frame_panel.bbox("all"))

    def move_frame_up(self):
        """Move the selected frame up in the order."""
        if self.selected_frame_index > 0:
            idx = self.selected_frame_index
            self.frames[idx], self.frames[idx-1] = self.frames[idx-1], self.frames[idx]
            self.selected_frame_index -= 1
            self.update_frame_panel()

    def move_frame_down(self):
        """Move the selected frame down in the order."""
        if self.selected_frame_index < len(self.frames) - 1:
            idx = self.selected_frame_index
            self.frames[idx], self.frames[idx+1] = self.frames[idx+1], self.frames[idx]
            self.selected_frame_index += 1
            self.update_frame_panel()

    def select_frame(self, event):
        """Select a frame when its thumbnail is clicked."""
        item = self.frame_panel.find_closest(event.x, event.y)
        tags = self.frame_panel.gettags(item)
        for tag in tags:
            if tag.startswith("frame-"):
                self.selected_frame_index = int(tag.split("-")[1])
                messagebox.showinfo("Frame Selected", f"Selected Frame {self.selected_frame_index + 1}")
                break




    def save_file(self):
        """Save the current layer as an image using PyQt5."""
        # Create a QImage to capture the canvas drawing
        image = QImage(self.canvas_width, self.canvas_height, QImage.Format_ARGB32)
        image.fill(Qt.white)  # Set background to white        

            # Use QPainter to render the current canvas to the QImage
        painter = QPainter(image)
        current_canvas = self.layers[self.active_layer_index]

            # Loop through each pixel and draw it using the painter
        for item in current_canvas.find_withtag("grid"):
            coords = current_canvas.coords(item)
            if len(coords) == 4:  # Only handle rectangle items
                x1, y1, x2, y2 = map(int, coords)
                color = current_canvas.itemcget(item, "fill")
                if color != "white":  # Only draw non-white pixels
                    painter.fillRect(x1, y1, x2 - x1, y2 - y1, QColor(color))

        painter.end()

            # Save the image as a PNG file
        file_name = "layer_output.png"
        image.save(file_name)
        messagebox.showinfo("Save", f"Layer saved as {file_name}")

    def export_as_gif(self):
        """Export all frames as a GIF."""
        if not self.frames:
            messagebox.showinfo("Export", "No frames to export.")
            return

        gif_file = "animation.gif"
        self.frames[0].save(
            gif_file,
            save_all=True,
            append_images=self.frames[1:],
            duration=100,
            loop=0
        )
        messagebox.showinfo("Export", f"Animation saved as {gif_file}")

if __name__ == '__main__':
    Paint()
