# main.py

import tkinter as tk
from keyboard_listener import start_key_listener, calculate_wpm, get_key_frequency
from heatmap import show_heatmap

def update_wpm_label():
    wpm = int(calculate_wpm())
    wpm_value.config(text=f"{wpm}")
    root.after(500, update_wpm_label)

def show_heatmap_callback():
    key_freq = get_key_frequency()
    show_heatmap(key_freq)

def initialize_key_listener():
    start_key_listener()

# Main window
root = tk.Tk()
root.title("Heated Keys - Typing Monitor")
root.geometry("250x150")
root.configure(bg="black")

# Frame
wpm_frame = tk.Frame(root, bg="black", width=200, height=80)
wpm_frame.pack(pady=(20, 10))
wpm_frame.pack_propagate(False)

wpm_value = tk.Label(wpm_frame, text="0", font=("Courier", 48, "bold"), fg="white", bg="black")
wpm_value.pack(expand=True)

wpm_unit = tk.Label(wpm_frame, text="wpm", font=("Helvetica", 12), fg="white", bg="black")
wpm_unit.place(relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

# Heat map button
heatmap_button = tk.Button(root, text="HEAT MAP", command=show_heatmap_callback,
                           font=("Helvetica", 10, "bold"), fg="black", bg="white", relief="flat")
heatmap_button.pack(pady=(0, 10))

# Start the key listener and update the WPM display.
root.after(100, initialize_key_listener)
update_wpm_label()

root.mainloop()
