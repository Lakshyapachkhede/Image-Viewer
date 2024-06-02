from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.geometry("600x650")
root.resizable(False, False)
img_frame = None
img_list = []
img_index = 0
path = r""

img_frame_new = LabelFrame(root, padx=10, pady=5, bd=5, width=600, height=550)
img_frame_new.grid(row=1, column=0, columnspan=3, sticky=N)

def get_images():
    global img_list
    img_list = [i for i in os.listdir(path) if (i.endswith((".jpg", ".jpeg", ".png", "gif")))]

def open_folder():
    global path
    global img_index
    img_index = 0
    path = filedialog.askdirectory(initialdir=r"E:\coding\python\modules\requests")
    get_images()
    if(len(img_list) == 0):
        messagebox.showinfo("Imageviewer", "This directory has no images")
    else:
        buttons()
        img_show()

def next_image():
    global img_index
    img_index += 1
    img_show()
    buttons()

def previous_image():
    global img_index
    img_index -= 1
    img_show()
    buttons()

def del_file():
    choice = messagebox.askokcancel(f"Delete {path}", f"Do you want to delete {img_list[img_index]}")
    if choice and path != "":
        os.remove(os.path.join(path, img_list[img_index]))
        img_list.pop(img_index)
        previous_image()
    else:
        return

def rename_file():
    global new_frame
    new_frame = LabelFrame(root, text="Enter new name", width=10, font="comicsans 10")
    new_frame.grid(row=3, column=0, columnspan=3, sticky=W+E)
    new_name = Entry(new_frame, width=10, font="comicsans 16")
    new_name.grid(row=0, column=0)
    confirm = Button(new_frame, text="Change", command=lambda: change_name(new_name.get()))
    confirm.grid(row=0, column=1)

def change_name(new_name):
    global img_index, img_list, path
    old_name = img_list[img_index]
    try:
        _, extension = old_name.split(".")
        if not new_name.endswith(extension):
            new_name = new_name + "." + extension
        old_path = os.path.join(path, img_list[img_index])
        new_path = os.path.join(path, new_name)
        os.rename(old_path, new_path)
        img_list[img_index] = new_name
        img_show()
        buttons()
        new_frame.destroy()
        messagebox.showinfo("ImageViewer", f"{old_name} successfully renamed to {new_name}")
    except:
        new_frame.destroy()
        messagebox.showerror("ImageViewer", f"Cannot rename {img_list[img_index]}")

def status():
        status_lbl = Label(root, text=f"Image {img_index+1} of {len(img_list)}", bd=1, relief=SUNKEN, anchor=E)
        status_lbl.grid(row=3, column=0, columnspan=3, pady=10, sticky=E)

def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = width / height

    new_width = min(width, max_width)
    new_height = int(new_width / aspect_ratio)

    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    resized_image = image.resize((new_width, new_height))
    return resized_image

def buttons():
    if(img_index == len(img_list)-1):
        next_button = Button(root, text=">>", padx=20, pady=10, bg="#007FFF", fg="yellow", command=next_image, state=DISABLED)
        next_button.grid(row=2, column=2, sticky=W+E)
    else:
        next_button = Button(root, text=">>", padx=20, pady=10, bg="#007FFF", fg="yellow", command=next_image)
        next_button.grid(row=2, column=2, sticky=W+E)

    if(img_index == 0):
        previous_button = Button(root, text="<<", padx=20, pady=10, bg="#007FFF", fg="yellow", command=previous_image, state=DISABLED)
        previous_button.grid(row=2, column=0, sticky=W+E)

    else:    
        previous_button = Button(root, text="<<", padx=20, pady=10, bg="#007FFF", fg="yellow", command=previous_image)
        previous_button.grid(row=2, column=0, sticky=W+E)


        

    quit_button = Button(root, text="Quit", padx=20, pady=10, bg="#007FFF", fg="yellow", command=root.destroy)
    quit_button.grid(row=2, column=1, sticky=W+E)

    del_file_button = Button(root, text="Delete Image", padx=0, pady=10, bg="#FF4040", fg="yellow", command=del_file)
    del_file_button.grid(row=0, column=1, sticky=W+E)

    rename_file_button = Button(root, text="Rename Image", padx=0, pady=10, bg="#007FFF", fg="yellow", command=rename_file)
    rename_file_button.grid(row=0, column=2, sticky=W+E)
    


def img_show():
    global img_frame
    try:
        if img_frame:
            img_frame.destroy()

        if img_index < 0 or img_index >= len(img_list):
            raise ValueError("Invalid image index")
        

        img = Image.open(os.path.join(path, img_list[img_index]))
        root.title("ImageViewer" + "/" + path + "/" + img_list[img_index])

        img = resize_image(img, 550, 500)

        img_ = ImageTk.PhotoImage(img)

        img_frame = Label(img_frame_new, image=img_, bg="black")
        img_frame.image = img_
        img_frame.grid(row=0, column=0, columnspan=3, sticky=W+E+N+S)
        status()
    except Exception as e:
        messagebox.showerror("Image Viewer", f"Error: {str(e)}")


dir_open_button = Button(root, text="Open Folder", padx=57, pady=10, bg="#007FFF", fg="yellow", command=open_folder)
dir_open_button.grid(row=0, column=0, columnspan=3, sticky=W)

# Set weights for rows and columns
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
