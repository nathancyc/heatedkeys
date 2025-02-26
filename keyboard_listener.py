# keyboard_listener.py

import time
import threading
from collections import deque
from pynput.keyboard import Key, Listener

# Sliding window size in seconds for WPM calculation
window_seconds = 10

# Shared data
timestamps = deque()
key_frequency = {}
data_lock = threading.Lock()

special_key_map = {
    Key.shift_l: "ShftL",
    Key.shift_r: "ShftR",
    Key.ctrl_l: "CtrlL",
    Key.ctrl_r: "CtrlR",
    Key.alt_l: "OptL",
    Key.alt_r: "OptR",
    Key.cmd_l: "CmdL",
    Key.cmd_r: "CmdR",
    Key.space:  "Space",
    Key.backspace: "Del",
    Key.delete:    "Del",
    Key.enter:     "Ret",
    Key.tab:       "Tab",
    Key.caps_lock: "Caps",
    Key.esc:       "Esc"
    # Add function keys, arrow keys, if needed
}

def on_press(key):
    now = time.time()
    with data_lock:
        if isinstance(key, Key):
            k = special_key_map.get(key, str(key))
        else:
            k = key.char.lower()

        key_frequency[k] = key_frequency.get(k, 0) + 1

        # Keep track of timestamps for WPM
        timestamps.append(now)
        # Remove any timestamps older than window_seconds
        while timestamps and now - timestamps[0] > window_seconds:
            timestamps.popleft()

def start_key_listener():
    listener = Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    return listener

def calculate_wpm():
    """Compute WPM over the last 'window_seconds' seconds"""
    now = time.time()
    with data_lock:
        # Remove old timestamps
        while timestamps and now - timestamps[0] > window_seconds:
            timestamps.popleft()
        count = len(timestamps)

    if count == 0:
        return 0

    # Effective duration is from the oldest keystroke to now
    effective_duration = now - timestamps[0]
    if effective_duration < 0.5:
        effective_duration = 0.5

    wpm = (count / 6) / (effective_duration / 60)
    return round(wpm, 2)

def get_key_frequency():
    with data_lock:
        return key_frequency.copy()
