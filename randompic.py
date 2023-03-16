import os
import random
import tkinter as tk
from PIL import Image, ImageTk


class ImageViewer(tk.Frame):
    def __init__(self, master, root, pattern):
        super().__init__(master)
        self.master = master
        self.root = root
        self.pattern = pattern
        self.filelist = self.find_files()

        # Create the container frame with a fixed size
        self.image_frame = tk.Frame(self, width=700, height=700)
        self.image_frame.pack_propagate(0)

        # Create the button container frame and pack the buttons into it
        self.button_frame = tk.Frame(self)
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_image)
        self.delete_button.pack(side="left")
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.show_next_image)
        self.next_button.pack(side="left")
        self.rotate_button = tk.Button(self.button_frame, text="Rotate 90", command=self.rotate_image)
        self.rotate_button.pack(side="left")
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.quit)
        self.quit_button.pack(side="right")

        # Create the image label and pack it into the image frame
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill="none", expand=True)

        # Create the main container frame and pack the image and button frames into it
        self.container_frame = tk.Frame(self)
        self.button_frame.pack(side="top", fill="x")
        self.image_frame.pack(side="top", fill="both", expand=True)


        # Show the first image
        self.current_file = None
        self.show_next_image()


    def find_files(self):
        """Returns a list of files in root directory and subdirectories that match pattern"""
        filelist = []
        for path, subdirs, files in os.walk(self.root):
            for name in files:
                if name.endswith(self.pattern):
                    filelist.append(os.path.join(path, name))
        return filelist

    def show_next_image(self):
        """Shows the next image in the filelist"""
        # Check if there are any images left to show
        if len(self.filelist) == 0:
            self.image_label.configure(image=None)
            return

        # Choose a random image from the filelist
        self.current_file = random.choice(self.filelist)

        # Load the image and resize it to fit within a maximum size while preserving aspect ratio
        max_width, max_height = 700, 700
        image = Image.open(self.current_file)
        width, height = image.size
        aspect_ratio = width / height
        if width > max_width or height > max_height:
            if aspect_ratio > 1:
                new_width = max_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(new_height * aspect_ratio)
            resized_image = image.resize((new_width, new_height), resample=Image.LANCZOS)
        else:
            resized_image = image

        # Display the image in the image_label widget
        photo = ImageTk.PhotoImage(resized_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo


    def delete_image(self):
        """Deletes the current image"""
        if self.current_file is not None:
            os.remove(self.current_file)
            self.filelist.remove(self.current_file)
            self.show_next_image()

    def rotate_image(self):
        """Rotates the current image 90 degrees to the right"""
        if self.current_file is None:
            print("No image is currently loaded.")
            return
        
        try:
            # Open the current image file and rotate it
            image = Image.open(self.current_file)
            rotated_image = image.rotate(-90, resample=Image.BICUBIC)

            # Save the rotated image to a temporary file
            temp_filename = f"{os.path.splitext(self.current_file)[0]}_temp.jpg"
            rotated_image.save(temp_filename)

            # Replace the current file with the rotated image file
            os.replace(temp_filename, self.current_file)

            # Show the rotated image
            self.show_next_image()
            
        except Exception as e:
            print(f"Error rotating image: {e}")


if __name__ == '__main__':
    root = '/Users/ro/Pictures'
    pattern = ".jpg"

    # Create the main window
    root_window = tk.Tk()
    root_window.title("Image Viewer")

    # Create the image viewer widget
    image_viewer = ImageViewer(root_window, root, pattern)
    image_viewer.pack()

    # Center the window on the screen
    width = 800
    height = 600
    x = (root_window.winfo_screenwidth() // 2) - (width // 2)
    y = (root_window.winfo_screenheight() // 2) - (height // 2)
    root_window.geometry(f"{width}x{height}+{x}+{y}")

    # Run the main loop
    root_window.mainloop()
