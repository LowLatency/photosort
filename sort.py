from tkinter import Tk, Button, Label
from PIL import ImageTk, Image
import logging
import os
import shutil

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()])
logger = logging.getLogger()

sourceDir = "sample/dataset/"
dirA = "sample/dirA/"
dirB = "sample/dirB/"
photo_format = ['.jpg', '.png', '.jpeg']
size = (800, 500)

entry: os.DirEntry
source_files = iter([entry.path for entry in os.scandir(sourceDir) if entry.path.endswith(tuple(photo_format))])
process_count = 1


def button_move(source: str, dest: str):
    logger.info(f"Moving {source} to {dest}")
    shutil.move(source, dest)
    update_image()


def update_image():
    try:
        global file
        global process_count
        file = next(source_files)
        process_count += 1
        root.title(process_count)
    except StopIteration:
        logger.info("No more images available!")
        root.destroy()
        del file
        return

    with Image.open(file) as image:
        image_res.configure(text=image.size)

        image.thumbnail(size, Image.LANCZOS)
        img = ImageTk.PhotoImage(image=image)

    label.configure(image=img)
    label.image = img
    image_path.configure(text=file)
    logger.debug(f"Image: {file}")


def skip():
    logger.info(f"Skipping file: {file}")
    update_image()


if __name__ == "__main__":
    root = Tk()
    root.title(process_count)
    root.geometry(f"{size[0]}x{size[1] + 50}")

    # Setup first image
    file = next(source_files)
    with Image.open(file) as photo:
        res = photo.size
        photo.thumbnail(size, Image.LANCZOS)
        img = ImageTk.PhotoImage(image=photo)

    # Image information
    image_res = Label(root, text=res)
    image_res.grid(row=1, column=0)

    # Image
    label = Label(root, image=img)
    label.grid(row=0, column=0)

    # Image path
    image_path = Label(root, text=file)
    image_path.grid(row=2, column=0)

    # Left button
    left_button = Button(root, text=dirA, command=lambda e: button_move(file, dirA))
    left_button.grid(row=3, column=0)

    # Right button
    right_button = Button(root, text=dirB, command=lambda e: button_move(file, dirB))
    right_button.grid(row=3, column=1)

    # Key bindings
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<s>", lambda e: skip())
    root.bind("<Left>", lambda e: button_move(file, dirA))
    root.bind("<Right>", lambda e: button_move(file, dirB))

    root.mainloop()
