from tkinter import *
import os
import random
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

root = Tk()
root.attributes("-fullscreen", True)  # Set window to full screen

# Define a global variable to keep track of the currently hovered widget
hovered_widget = None

# Define a custom class that inherits from tk.Label
class CardLabel(tk.Label):
    def __init__(self, master=None, filename=None, **kwargs):
        super().__init__(master, **kwargs)
        self.filename = filename

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
    global hovered_widget
    
    # Calculate the new x and y coordinates of the card
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y

    # Check if the mouse is over the widget
    if (x >= 0 and x <= card_width) and (y >= 0 and y <= card_height):
        hovered_widget = widget
    else:
        hovered_widget = None

    # Move the card to the new coordinates
    widget.place(x=x, y=y)

# Define a function to handle mouse button release event
def on_card_release(event):
    # Do nothing for now
    pass

# Define global variables
selected_filenames = []

# Define a function to handle key press event
def on_key_press(event):
    global hovered_widget, selected_filenames
    
    # Check if the space bar is pressed
    if event.keysym == "space":
        # Check if there is a hovered widget
        if hovered_widget is not None:
            # Get the index of the card label widget
            index = card_labels.index(hovered_widget)

            # Get the filename of the corresponding card image
            filename = random_filenames[index]

            # Print the name of the card
            print(filename)

            # Add or remove the filename to/from the selected_filenames list
            if filename in selected_filenames:
                selected_filenames.remove(filename)
                print("Removed from selection.")
                hovered_widget.config(borderwidth=0, highlightthickness=0)
            else:
                selected_filenames.append(filename)
                print("Added to selection.")
                hovered_widget.config(highlightbackground="red", highlightthickness=2)

            # Print the current selection
            print("Selected filenames:", selected_filenames)
            
# Define a function to handle mouse enter event
def on_card_enter(event):
    global hovered_widget
    hovered_widget = event.widget

# Define a function to handle mouse leave event
def on_card_leave(event):
    global hovered_widget
    hovered_widget = None
    
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
safe1 = tk.Canvas(width=card_width, height=card_height)
safe1.pack()

# draw a colored rectangle on the canvas
safe1.create_rectangle(0, 0, card_width, card_height, fill="#41a437")
safe1.place(x=1100, y=20)
        
# create a canvas widget
safe2 = tk.Canvas(width=card_width, height=card_height)
safe2.pack()

# draw a colored rectangle on the canvas
safe2.create_rectangle(0, 0, card_width, card_height, fill="#41a437")
safe2.place(x=100, y=20)


# create a canvas widget
safe3 = tk.Canvas(width=card_width, height=card_height)
safe3.pack()

# draw a colored rectangle on the canvas
safe3.create_rectangle(0, 0, card_width, card_height, fill="#009fe3")
safe3.place(x=1100, y=200)

# create a canvas widget
safe4 = tk.Canvas(width=card_width, height=card_height)
safe4.pack()

# draw a square divided into two colors on the canvas
safe4.create_polygon(0, 0, 0, 180, 120, 0, fill="#41a437") # top left triangle
safe4.create_polygon(0, 180, 120, 0, 120, 180, fill="#009fe3") # bottom right triangle
safe4.place(x=100, y=200)

# create a canvas widget
safe5 = tk.Canvas(width=card_width, height=card_height)
safe5.pack()

# draw a colored rectangle on the canvas
safe5.create_rectangle(0, 0, card_width, card_height, fill="#e6007c")
safe5.place(x=1100, y=380)

# create a canvas widget
safe6 = tk.Canvas(width=card_width, height=card_height)
safe6.pack()

# draw a colored rectangle on the canvas
safe6.create_rectangle(0, 0, card_width, card_height, fill="#009fe3")
safe6.place(x=100, y=380)

# create a canvas widget
safe7 = tk.Canvas(width=card_width, height=card_height)
safe7.pack()

# draw a colored rectangle on the canvas
safe7.create_rectangle(0, 0, card_width, card_height, fill="#ffee00")
safe7.place(x=100, y=560)

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

# shuffle the card images
random.shuffle(card_images)

# shuffle the list of filenames
random.shuffle(random_filenames)

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
    label.bind("<Button-3>", show_card_copy)
    label.bind("<Button-1>", on_card_press)
    label.bind("<B1-Motion>", on_card_motion)
    label.bind("<Enter>", on_card_enter)
    label.bind("<Leave>", on_card_leave)
    label.config(borderwidth=0)
    root.bind("<Key>", on_key_press)

# Load image and create a background canvas to display it
image_bg = Image.open("svart bg Spelplan.jpg")
width, height = root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2
image_bg = image_bg.resize((width, height))
photo_bg = ImageTk.PhotoImage(image_bg)
canvas_bg = Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0)
canvas_bg.create_image(width/2, height/2, image=photo_bg)
canvas_bg.pack()

press_count = 0

def reset_cards():
    global random_filenames, card_labels, press_count, card_images, selected_filenames
    print("Selected filenames:", selected_filenames)
    press_count += 1
    if reset_button["bg"] == "green":
        reset_button.configure(bg="yellow")
    elif reset_button["bg"] == "yellow":
        reset_button.configure(bg="red")
    else:
        reset_button.place_forget()

    # If selected_filenames is not empty, save its contents
    if selected_filenames:
        saved_selected_filenames = selected_filenames.copy()
    else:
        saved_selected_filenames = []

    # initialize card_images variable
    card_images = []

    # remove all card labels from the window
    for label in card_labels:
        if label["image"] in card_images:
            card_images.remove(label["image"])
        label.destroy()
    card_labels = []

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

    # create lists for each name that must appear
    blue_filenames = [filename for filename in card_filenames if "Blue" in filename]
    green_filenames = [filename for filename in card_filenames if "Green" in filename]
    yellow_filenames = [filename for filename in card_filenames if "Yellow" in filename]
    pink_filenames = [filename for filename in card_filenames if "Pink" in filename]

    # randomly shuffle the filenames for each color
    random.shuffle(blue_filenames)
    random.shuffle(green_filenames)
    random.shuffle(yellow_filenames)
    random.shuffle(pink_filenames)

    # select the required number of filenames for each color
    selected_filenames = []
    selected_filenames.extend(blue_filenames[:2])
    selected_filenames.extend(green_filenames[:2])
    selected_filenames.extend(yellow_filenames[:1])
    selected_filenames.extend(pink_filenames[:1])

    # add 2 more random filenames to complete the list of 8
    remaining_filenames = [filename for filename in card_filenames if filename not in selected_filenames]
    random.shuffle(remaining_filenames)
    random_filenames = selected_filenames + remaining_filenames[:2]

    # shuffle the card images
    random.shuffle(card_images)

    # shuffle the list of filenames
    random.shuffle(random_filenames)

    # assign the new list of random filenames and create the new card images
    for filename in random_filenames:
        image = Image.open(os.path.join(card_dir, filename))
        image = image.resize((card_width, card_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        card_images.append(photo)

    # create new card labels and display them in the window
    label = None
    for i in range(8):
        label = tk.Label(root, bg="black")
        label.place(x=card_x + i % 4 * card_width, y=card_y + i // 4 * card_height)
        label["image"] = card_images[i]
        card_labels.append(label)
        label.bind("<Button-3>", show_card_copy)
        label.bind("<Button-1>", on_card_press)
        label.bind("<B1-Motion>", on_card_motion)
        label.bind("<Enter>", on_card_enter)
        label.bind("<Leave>", on_card_leave)
        label.config(borderwidth=0)
        root.bind("<Key>", on_key_press)

    # If saved_selected_filenames is not empty, restore its contents
    if saved_selected_filenames:
        selected_filenames = saved_selected_filenames.copy()
        create_selected_card_pile(selected_filenames)

# initialize selected_card_images and selected_card_labels variables
selected_card_images = []
selected_card_labels = []

def create_selected_card_pile(selected_filenames):
    global selected_card_labels, selected_card_images
    selected_card_images = []
    # remove all selected card labels from the window
    for label in selected_card_labels:
        if label["image"] in selected_card_images:
            selected_card_images.remove(label["image"])
        label.destroy()
    selected_card_labels = []
    # calculate the starting position of the first label
    start_x = card_x
    start_y = card_y - 400
    # calculate the offset between each label
    offset_x = card_width + 0
    offset_y = card_height + 0
    # create new selected card images and labels and display them in the window
    for i, filename in enumerate(selected_filenames):
        image = Image.open(os.path.join(card_dir, filename))
        image = image.resize((card_width, card_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        selected_card_images.append(photo)
        label = tk.Label(root, bg="black")
        # calculate the position of the label based on the index and offset
        label.place(x=start_x + i % 4 * offset_x, y=start_y + i // 4 * offset_y + 20)
        label["image"] = photo
        selected_card_labels.append(label)
        label.bind("<Button-3>", show_card_copy)
        label.bind("<Button-1>", on_card_press)
        label.bind("<B1-Motion>", on_card_motion)
        label.bind("<Enter>", on_card_enter)
        label.bind("<Leave>", on_card_leave)
        label.config(highlightbackground="darkred", highlightthickness=2, borderwidth=0)

reset_button = tk.Button(root, text="Reset Cards", command=reset_cards, bg="green", fg="white", bd=0, width=10, height=5)
reset_button.place(x=screen_width // 2 + 440, y=screen_height - 150)

# start the tkinter main loop to display the window
root.mainloop()
