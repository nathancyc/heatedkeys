# heatmap.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# A Mac-style layout
keyboard_layout = [
    ["Esc", "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Del"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Ret"],
    ["ShftL", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "ShftR"],
    ["Fn", "CtrlL", "OptL", "CmdL", "Space", " ", " ", " ", " ", "CmdR", "OptR"]
]

def create_heatmap_matrix(layout, freq):
    """
    Build a 2D matrix of key-press counts.
    For cells that are placeholders (a single space " "),
    use the frequency of "Space".
    """
    max_cols = max(len(row) for row in layout)
    matrix = []
    for row in layout:
        matrix_row = []
        for key in row:
            if key == " ":
                # Placeholder cell for the wide space bar: use frequency of "Space"
                count = freq.get("Space", 0)
            else:
                # For normal keys, check both the key and its lowercase version.
                count = freq.get(key, 0) + freq.get(key.lower(), 0)
            matrix_row.append(count)
        matrix_row.extend([0] * (max_cols - len(matrix_row)))
        matrix.append(matrix_row)
    return np.array(matrix)

def show_heatmap(key_freq):
    matrix = create_heatmap_matrix(keyboard_layout, key_freq)

    # Custom colormap
    custom_cmap = LinearSegmentedColormap.from_list("IceRed", ["#b3ffff", "red"])

    plt.figure(figsize=(12, 5))
    plt.imshow(matrix, cmap=custom_cmap, interpolation='nearest')
    plt.colorbar(label='Key Press Frequency')

    for i, row in enumerate(keyboard_layout):
        for j, key in enumerate(row):
            if key.strip() == "":  # If the cell is a placeholder, skip labeling
                continue
            plt.text(j, i, key, ha="center", va="center", color="black", fontsize=8)

    plt.xticks([])
    plt.yticks([])
    plt.title("Heat Map")
    plt.show()
