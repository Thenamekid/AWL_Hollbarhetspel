from tkinter import *
import os
import random
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

root = Tk()
root.attributes("-fullscreen", True)  # Set window to full screen

# Define a function to handle mouse button press event
def on_card_press(event):
    # Store the x and y coordinates of the mouse pointer
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

    # Bring the card to the front
    widget.lift()

# Define a function to handle mouse motion event
def on_card_motion(event):
    # Calculate the new x and y coordinates of the card
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y

    # Move the card to the new coordinates
    widget.place(x=x, y=y)

# Define a function to handle mouse button release event
def on_card_release(event):
    # Do nothing for now
    pass

# set the path to the directory containing the card image folders
card_dir = './spel_kort'

# define the names that must appear in the filenames
names_to_include = {'Blue': 2, 'Green': 2, 'Pink': 1, 'Yellow': 1}

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

# randomly shuffle the filenames
random.shuffle(card_filenames)

# create lists for each name that must appear
included_filenames = []
for name, count in names_to_include.items():
    matching_filenames = [filename for filename in card_filenames if name in filename]
    if len(matching_filenames) < count:
        raise ValueError(f"Not enough filenames with '{name}' in their name.")
    random.shuffle(matching_filenames) # shuffle the matching filenames
    included_filenames.extend(matching_filenames[:count])
    card_filenames = [filename for filename in card_filenames if filename not in included_filenames]

# add 2 more random filenames to complete the list of 8
random.shuffle(card_filenames) # shuffle the remaining filenames
random_filenames = included_filenames + random.sample(card_filenames, 2)

# set the window background to black
root.configure(bg="black")

# get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# calculate the center coordinates for the card images
card_width = 120
card_height = 180
card_x = screen_width // 2 - (card_width * 4) // 2
card_y = screen_height - (card_height + 200)

# create a canvas widget
canvas1 = tk.Canvas(width=card_width, height=card_height)
canvas1.pack()

# draw a colored rectangle on the canvas
canvas1.create_rectangle(0, 0, card_width, card_height, fill="#41a437")
canvas1.place(x=1100, y=20)

# create a canvas widget
canvas2 = tk.Canvas(width=card_width, height=card_height)
canvas2.pack()

# draw a colored rectangle on the canvas
canvas2.create_rectangle(0, 0, card_width, card_height, fill="#41a437")
canvas2.place(x=100, y=20)


# create a canvas widget
canvas3 = tk.Canvas(width=card_width, height=card_height)
canvas3.pack()

# draw a colored rectangle on the canvas
canvas3.create_rectangle(0, 0, card_width, card_height, fill="#009fe3")
canvas3.place(x=1100, y=200)

# create a canvas widget
canvas4 = tk.Canvas(width=card_width, height=card_height)
canvas4.pack()

# draw a square divided into two colors on the canvas
canvas4.create_polygon(0, 0, 0, 180, 120, 0, fill="#41a437") # top left triangle
canvas4.create_polygon(0, 180, 120, 0, 120, 180, fill="#009fe3") # bottom right triangle
canvas4.place(x=100, y=200)

# create a canvas widget
canvas5 = tk.Canvas(width=card_width, height=card_height)
canvas5.pack()

# draw a colored rectangle on the canvas
canvas5.create_rectangle(0, 0, card_width, card_height, fill="#e6007c")
canvas5.place(x=1100, y=380)

# create a canvas widget
canvas6 = tk.Canvas(width=card_width, height=card_height)
canvas6.pack()

# draw a colored rectangle on the canvas
canvas6.create_rectangle(0, 0, card_width, card_height, fill="#009fe3")
canvas6.place(x=100, y=380)

# create a canvas widget
canvas7 = tk.Canvas(width=card_width, height=card_height)
canvas7.pack()

# draw a colored rectangle on the canvas
canvas7.create_rectangle(0, 0, card_width, card_height, fill="#ffee00")
canvas7.place(x=100, y=560)

# create a list to hold the card images and labels
card_images = []
card_labels = []

# initialize the copy label variable to None
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
    copy_image = copy_image.resize((300, 400), Image.LANCZOS)
    copy_photo = ImageTk.PhotoImage(copy_image)
    # check if the copy label already exists
    if copy_label:
        # update the existing copy label image with the new image
        copy_label.configure(image=copy_photo)
        copy_label.image = copy_photo # keep a reference to the image to prevent garbage collection
    else:
        # create a label for the copy image and place it in the center of the window
        copy_label = tk.Label(root, image=copy_photo, bg="black")
        copy_label.place(x=screen_width // 2 - 150, y=screen_height // 2 - 400)
        copy_label.image = copy_photo # keep a reference to the image to prevent garbage collection
    
    # bind a <Button-1> event to the root window to close the copied card if clicked outside
    root.bind("<Button-3>", close_card_copy)

def close_card_copy(event):
    global copy_label
    if copy_label:
        copy_label.destroy()
        copy_label = None
        root.unbind("<Button-3>")

# load each selected card image into a PIL Image object and then a tkinter PhotoImage object
for filename in random_filenames:
    image = Image.open(os.path.join(card_dir, filename))
    image = image.resize((card_width, card_height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    card_images.append(photo)

# shuffle the card images
random.shuffle(card_images)

# create a tkinter Label widget for each card image and display it in the window
for i in range(8):
    label = tk.Label(root, image=card_images[i], bg="black")
    label.place(x=card_x + i % 4 * card_width, y=card_y + i // 4 * card_height)
    card_labels.append(label)
    # bind the show_card_copy function to the <Button-3> event of each card label
    label.bind("<Button-3>", show_card_copy)
    # bind the on_card_press function to the <Button-1> event of each card label
    label.bind("<Button-1>", on_card_press)
    # bind the on_card_motion function to the <B1-Motion> event of each card label
    label.bind("<B1-Motion>", on_card_motion)
    
# Load image and create a background canvas to display it
image_bg = Image.open("svart bg Spelplan.jpg")
width, height = root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2
image_bg = image_bg.resize((width, height))
photo_bg = ImageTk.PhotoImage(image_bg)
canvas_bg = Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0)
canvas_bg.create_image(width/2, height/2, image=photo_bg)
canvas_bg.pack()

def reset_cards():
    global random_filenames, card_labels

    # loop over all seven canvas widgets
    for i in range(1, 8):
        # get the coordinates of the canvas widget
        canvas = globals()['canvas{}'.format(i)]
        canvas_bbox = canvas.bbox(tk.ALL)

        # remove existing card labels that are not touching the canvas
        new_card_labels = []
        for label in card_labels:
            # get the coordinates of the bounding box of the label
            label_bbox = label.bbox(tk.ALL)

            # check if the label is overlapping with the canvas widget
            if label_bbox and canvas_bbox and label_bbox[0] < canvas_bbox[2] and label_bbox[2] > canvas_bbox[0] and label_bbox[1] < canvas_bbox[3] and label_bbox[3] > canvas_bbox[1]:
                # add the label to the list of new card labels
                new_card_labels.append(label)
            else:
                # keep the image attached to the label and remove the label from the canvas
                card_images.remove(label["image"])
                label.destroy()
                card_labels.remove(label)
        card_labels = new_card_labels

    # create a list of available card filenames excluding the ones already selected
    available_filenames = card_filenames.copy()
    available_filenames = [filename for filename in available_filenames if filename not in random_filenames]

    # create a dictionary to store the number of available images for each color
    available_colors = {'Blue': 0, 'Green': 0, 'Pink': 0, 'Yellow': 0}
    for filename in available_filenames:
        for color in available_colors:
            if color in filename:
                available_colors[color] += 1

    # check if there are enough available filenames for each required color
    for color, count in names_to_include.items():
        if available_colors[color] < count:
            raise ValueError(f"Not enough filenames with '{color}' in their name.")

    # randomly select the required number of filenames for each color
    selected_filenames = []
    for color, count in names_to_include.items():
        matching_filenames = [filename for filename in available_filenames if color in filename]
        selected_filenames += random.sample(matching_filenames, count)

    # select the remaining filenames at random
    remaining_filenames = [filename for filename in available_filenames if filename not in selected_filenames]
    selected_filenames += random.sample(remaining_filenames, 8 - len(selected_filenames))

    # assign the new list of random filenames and create the new card images
    random_filenames = selected_filenames
    for filename in random_filenames:
        image = Image.open(os.path.join(card_dir, filename))
        image = image.resize((card_width, card_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        card_images.append(photo)

    # shuffle the card images
    random.shuffle(card_images)

    # create new card labels and display them in the window
    for i in range(8):
        label = tk.Label(root, bg="black")
        label.place(x=card_x + i % 4 * card_width, y=card_y + i // 4 * card_height)
        label["image"] = card_images[i]
        card_labels.append(label)
        label.bind("<Button-3>", show_card_copy)
        label.bind("<Button-1>", on_card_press)
        label.bind("<B1-Motion>", on_card_motion)
        
reset_button = tk.Button(root, text="Reset Cards", command=reset_cards, bg="gray", fg="white", bd=0, width=10, height=5)
reset_button.place(x=screen_width // 2 + 440, y=screen_height - 150)

# start the tkinter main loop to display the window
root.mainloop()
