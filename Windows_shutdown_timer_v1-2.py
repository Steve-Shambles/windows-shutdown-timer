import tkinter as tk
import tkinter.messagebox
from tkinter import Spinbox
from tkinter.ttk import Combobox
import subprocess

# V1.1 fixed abort so can continue using prog rather than it just quit.
# V1.2 fixed abort bug where instead of shutdown it aborted, doh! idiot.

root = tk.Tk()
root.title("WSDT V.1.2")
root.resizable(False, False)

countdown_time = 0
aborted = False

def start_timer():
    global countdown_time
    
    hours = int(hours_spin_box.get())
    minutes = int(minutes_spin_box.get())
    countdown_time = (hours * 3600) + (minutes * 60)

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
    global countdown_time, aborted
    
    ask = tkinter.messagebox.askyesno('Abort Operation?', 'Are you sure?')
    if ask:
        countdown_time = 0
        hours_spin_box.configure(state=tk.NORMAL)
        minutes_spin_box.configure(state=tk.NORMAL)
        start_button.configure(state=tk.NORMAL)
        abort_button.configure(state=tk.DISABLED)
        action_combobox.configure(state=tk.NORMAL)
        aborted = True
        countdown_label.config(font=("helvewtica 12"), text="")


def shutdown():
    global action_combobox, aborted

    action = action_combobox.get()
    abort_button.configure(state=tk.DISABLED)
    countdown_label.config(text=action)

    if aborted:
        countdown_label.config(font=("helvewtica 12"),
                                     bg="black", fg="lightgreen",
                                     text="Aborted")
        subprocess.run(["shutdown", "-a"])
        aborted = False
        return

    if action == "Shutdown":
            subprocess.run(["shutdown", "-s"])

    elif action == "Restart":
            subprocess.call(["shutdown", "/r"])

    

def update_countdown():
    global countdown_time
    
    if countdown_time >= 0:
        hours = countdown_time // 3600
        minutes = (countdown_time % 3600) // 60
        seconds = countdown_time % 60

        countdown_label.config(font=("helvewtica 12"), fg="light green",
                               bg="black",
                               text="{:02d}:{:02d}:{:02d}".
                                    format(hours, minutes, seconds))
        countdown_time -= 1
        root.after(1000, update_countdown)

    else:
        action = action_combobox.get()
        countdown_label.config(text=action_combobox)

        shutdown()


def about():
    tk.messagebox.showinfo('Windows Shutdown Timer V1.2',
                    'By Steve Shambles Feb 2023\n'
                    '\nSimply select the hours and minutes\n'
                    'to go for when you want your PC\n'
                    'to automatically shutdown or restart,\n'
                    'then click start.\n\n'
                    'This is FREEWARE, but (c) Steve Shambles 2023')


# Create spin boxes for hours and minutes
hours_spin_box = tk.Spinbox(from_=0, to=99)
minutes_spin_box = tk.Spinbox(from_=0, to=59)

# Create labels for hours and minutes
hours_label = tk.Label(text="Hours")
minutes_label = tk.Label(text="Minutes")

# Create the action combobox
action_combobox = tk.ttk.Combobox(values=["Shutdown", "Restart"])
action_combobox.set("Shutdown")
action_label = tk.Label(text="Select Action")

# Create start button
start_button = tk.Button(text="Start", command=start_timer)
abort_button = tk.Button(text="Abort", command=abort_timer)

# Place the widgets on the window
hours_label.pack()
hours_spin_box.pack()
minutes_label.pack()
minutes_spin_box.pack()
action_label.pack()
action_combobox.pack()
start_button.pack(side='left', padx=5)
abort_button.pack(side='left')

abort_button.configure(state=tk.DISABLED)

# Create the countdown label
countdown_label = tk.Label(text="")
countdown_label.pack()

# Create drop down menu.
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Info', menu=file_menu)
file_menu.add_command(label='About', command=about)
# file_menu.add_separator()
root.config(menu=menu_bar)


root.mainloop()
