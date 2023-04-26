from tkinter import *
import os
import random
import tkinter as tk
from PIL import Image, ImageTk

root = Tk()
root.attributes("-fullscreen", True)  # Set window to full screen

# set the path to the directory containing the card image folders
card_dir = './spel_kort'

# create an empty list to store all the card filenames
card_filenames = []

# create a dictionary to store the number of images in each folder
num_images_dict = {}

# loop through each folder and add the filenames to the list
for foldername in os.listdir(card_dir):
    folderpath = os.path.join(card_dir, foldername)
    if os.path.isdir(folderpath):
        num_images = len([filename for filename in os.listdir(folderpath) if filename.endswith(".jpg")])
        num_images_dict[foldername] = num_images
        card_filenames.extend([os.path.join(foldername, filename) for filename in os.listdir(folderpath) if filename.endswith(".jpg")])

# calculate the total number of images and the number of folders
total_num_images = len(card_filenames)
num_folders = len(num_images_dict)

# calculate the number of images to select from each folder
num_images_per_folder = total_num_images // num_folders

# select 8 random filenames from the list
random_filenames = random.sample(card_filenames, 8)

# set the window background to black
root.configure(bg="black")

# get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# calculate the center coordinates for the card images
card_width = 100
card_height = 150
card_x = screen_width // 2 - (card_width * 4) // 2
card_y = screen_height - (card_height + 200)

# create a list to hold the card images and labels
card_images = []
card_labels = []

# initialize the copy label variable to None4
copy_label = None

def __main__():
    global random_filenames, card_images, card_labels, card_dir, card_width, card_height, card_x, card_y, screen_width, screen_height

# create a function to display a copy of the clicked card in the center of the window
def show_card_copy(event):
    global random_filenames, copy_label
    # get the index of the clicked label
    index = card_labels.index(event.widget)
    # create a copy of the clicked card image and resize it
    copy_image = Image.open(os.path.join(card_dir, random_filenames[index]))
    copy_image = copy_image.resize((400, 600), Image.LANCZOS)
    copy_photo = ImageTk.PhotoImage(copy_image)
    # check if the copy label already exists
    if copy_label:
        # update the existing copy label image with the new image
        copy_label.configure(image=copy_photo)
        copy_label.image = copy_photo # keep a reference to the image to prevent garbage collection
    else:
        # create a label for the copy image and place it in the center of the window
        copy_label = tk.Label(root, image=copy_photo, bg="black")
        copy_label.place(x=screen_width // 2 - 200, y=screen_height // 2 - 300)
        copy_label.image = copy_photo # keep a reference to the image to prevent garbage collection
        
    # bind a <Button-1> event to the copied card to move the original card to (100, 100) when clicked
    def move_original_card(event):
        foldername = os.path.basename(os.path.dirname(card_filenames[index]))
        print(foldername)
        global copy_label
        # set the position of the copied card based on the folder name
        if foldername == 'green':
            card_labels[index].place(x=100, y=200)
        elif foldername == 'yellow':
            card_labels[index].place(x=100, y=300)
        else:
            card_labels[index].place(x=100, y=100)
        copy_label.destroy()
        copy_label = None
        root.unbind("<Button-1>")
    copy_label.bind("<Button-1>", move_original_card)
    
    # bind a <Button-1> event to the root window to close the copied card if clicked outside
    root.bind("<Button-1>", close_card_copy)

def close_card_copy(event):
    global copy_label
    if copy_label:
        copy_label.destroy()
        copy_label = None
        root.unbind("<Button-1>")

# load each selected card image into a PIL Image object and then a tkinter PhotoImage object
for filename in random_filenames:
    image = Image.open(os.path.join(card_dir, filename))
    image = image.resize((card_width, card_height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    card_images.append(photo)

# create a tkinter Label widget for each card image and display it in the window
for i in range(8):
    label = tk.Label(root, image=card_images[i], bg="black")
    label.place(x=card_x + i % 4 * card_width, y=card_y + i // 4 * card_height)
    card_labels.append(label)
    # bind the show_card_copy function to the <Button-1> event of each card label
    label.bind("<Button-1>", show_card_copy)
    
# Load image and create a background canvas to display it
image_bg = Image.open("svart bg Spelplan.jpg")
width, height = root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2
image_bg = image_bg.resize((width, height))
photo_bg = ImageTk.PhotoImage(image_bg)
canvas_bg = Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0)
canvas_bg.create_image(width/2, height/2, image=photo_bg)
canvas_bg.pack()

def reset_cards():
    global random_filenames
    # remove existing card labels and images
    for label in card_labels:
        label.destroy()
    card_labels.clear()
    card_images.clear()

    # generate new random filenames
    random_filenames = random.sample(card_filenames, 8)

    # create new card images
    for filename in random_filenames:
        image = Image.open(os.path.join(card_dir, filename))
        image = image.resize((card_width, card_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        card_images.append(photo)

    # create new card labels and display them in the window
    for i in range(8):
        label = tk.Label(root, image=card_images[i], bg="black")
        label.place(x=card_x + i % 4 * card_width, y=card_y + i // 4 * card_height)
        card_labels.append(label)
        label.bind("<Button-1>", show_card_copy)
        
reset_button = tk.Button(root, text="Reset Cards", command=reset_cards)
reset_button.place(x=screen_width // 2 + 250, y=screen_height - 100)

# start the tkinter main loop to display the window
root.mainloop()
