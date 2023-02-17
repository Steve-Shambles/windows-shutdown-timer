""" Windows Shutdown Timer V1.3 by Steve Shambles (c) feb 2023."""

import subprocess
import tkinter as tk
import tkinter.messagebox
from tkinter import Spinbox
from tkinter.ttk import Combobox
import sys
from PIL import Image, ImageTk


root = tk.Tk()
root.title("WSDT V.1.3")
root.resizable(False, False)

COUNTDOWN_TIME = 0
ABORTED = False

a_font = "helvetica 10 bold"

def start_timer():
    """ Yes-No pop up to start timer. """
    global COUNTDOWN_TIME

    hours = int(hours_spin_box.get())
    minutes = int(minutes_spin_box.get())
    COUNTDOWN_TIME = (hours * 3600) + (minutes * 60)

    action = action_combobox.get()

    message = f"Selected time: {hours} hours and {minutes} minutes\n"
    message += f"Selected action: {action}\n"
    message += "\nDo you want to start the countdown?"

    result = tkinter.messagebox.askyesno("Selection", message)

    if result:
        abort_button.configure(state=tk.NORMAL)
        action_combobox.configure(state=tk.DISABLED)
        hours_spin_box.configure(state=tk.DISABLED)
        minutes_spin_box.configure(state=tk.DISABLED)
        start_button.configure(state=tk.DISABLED)

        update_countdown()


def abort_timer():
    """ Abort timer and reset conditions. """
    global COUNTDOWN_TIME, ABORTED

    ask = tkinter.messagebox.askyesno('Abort Operation?', 'Are you sure?')
    if ask:
        COUNTDOWN_TIME = 0
        hours_spin_box.configure(state=tk.NORMAL)
        minutes_spin_box.configure(state=tk.NORMAL)
        start_button.configure(state=tk.NORMAL)
        abort_button.configure(state=tk.DISABLED)
        action_combobox.configure(state=tk.NORMAL)
        ABORTED = True
        countdown_label.config(font=("helvewtica 12"), text="")


def shutdown():
    """ The actual shutdown or restart subprocess execution. """
    global action_combobox, ABORTED

    action = action_combobox.get()
    abort_button.configure(state=tk.DISABLED)
    countdown_label.config(text=action)

    if ABORTED:
        countdown_label.config(font=("helvewtica 12"),
                               bg="black", fg="lightgreen",
                               text="ABORTED")
        subprocess.run(["shutdown", "-a"])
        ABORTED = False
        return

    if action == "Shutdown":
        subprocess.run(["shutdown", "-s"])

    elif action == "Restart":
        subprocess.call(["shutdown", "/r"])


def update_countdown():
    """ Update the timer in the GUI using after method. """
    global COUNTDOWN_TIME

    if COUNTDOWN_TIME >= 0:
        hours = COUNTDOWN_TIME // 3600
        minutes = (COUNTDOWN_TIME % 3600) // 60
        seconds = COUNTDOWN_TIME % 60

        countdown_label.config(font=("helvewtica 12"), fg="light green",
                               bg="black",
                               text="{:02d}:{:02d}:{:02d}".
                                    format(hours, minutes, seconds))
        COUNTDOWN_TIME -= 1
        root.after(1000, update_countdown)

    else:
        action = action_combobox.get()
        countdown_label.config(text=action_combobox)

        shutdown()


def about():
    """ Program info. """
    tk.messagebox.showinfo('Windows Shutdown Timer V1.3',
                           'By Steve Shambles Feb 2023\n'
                           '\nSimply select the hours and minutes\n'
                           'to go for when you want your PC\n'
                           'to automatically shutdown or restart,\n'
                           'and then click start.\n\n'
                           'This is FREEWARE, but (c) Steve Shambles 2023')


# Display logo in logo frame.
logo_frame = tk.LabelFrame(root)
logo_frame.pack()

try:
    logo_image = Image.open("wsdt.jpg")
except FileNotFoundError as e:
    tk.messagebox.showinfo("FileNotFoundError",
                           "wsdt.jpg not found.")
    root.destroy()
    sys.exit(1)

logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid(padx=2, pady=2, row=0, column=0)

# Create spin boxes for hours and minutes
hours_spin_box = tk.Spinbox(from_=0, to=99)
minutes_spin_box = tk.Spinbox(from_=0, to=59)

# Create labels for hours and minutes
hours_label = tk.Label(font=a_font, fg="blue", text="Hours")
minutes_label = tk.Label(font=a_font, fg="blue", text="Minutes")

# Create the action combobox
action_combobox = tk.ttk.Combobox(values=["Shutdown", "Restart"])
action_combobox.set("Shutdown")
action_label = tk.Label(font=a_font, fg="blue", text="Select Action")

# Create start button
start_button = tk.Button(text="Start", bg="lime",  command=start_timer)
abort_button = tk.Button(text="Abort", bg="indianred", command=abort_timer)

# Place the widgets on the window
hours_label.pack()
hours_spin_box.pack()
minutes_label.pack()
minutes_spin_box.pack()
action_label.pack()
action_combobox.pack()
start_button.pack(side='left', padx=5, pady=10)
abort_button.pack(side='left')

abort_button.configure(state=tk.DISABLED)

# Create the countdown label
countdown_label = tk.Label(text="")
countdown_label.pack(pady=10)

# Create drop down menu.
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Info', menu=file_menu)
file_menu.add_command(label='About', command=about)
root.config(menu=menu_bar)


root.mainloop()
