import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

def open_image():
    global img, tk_img, img_array
    filepath = filedialog.askopenfilename()
    if filepath:
        img = Image.open(filepath)
        img_array = np.array(img)
        tk_img = ImageTk.PhotoImage(img)
        img_label.config(image=tk_img)
        img_label.image = tk_img

def compress_image():
    global img, tk_img, img_array
    try:
        k = int(k_entry.get())
        compressed_img = compress_color_image(img_array, k)
        compressed_img_pil = Image.fromarray(compressed_img)
        tk_img = ImageTk.PhotoImage(compressed_img_pil)
        img_label.config(image=tk_img)
        img_label.image = tk_img
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid integer for k")

def compress_color_image(img_array, k):
    compressed_img = np.zeros_like(img_array)
    for channel in range(3):
        U, S, V = np.linalg.svd(img_array[:, :, channel], full_matrices=False)
        S = np.diag(S)
        compressed_img[:, :, channel] = np.dot(U[:, :k], np.dot(S[:k, :k], V[:k, :]))
    compressed_img = np.clip(compressed_img, 0, 255).astype(np.uint8)
    return compressed_img

app = tk.Tk()
app.title("Color Image Compression")

open_btn = tk.Button(app, text="Open Image", command=open_image)
open_btn.pack()

tk.Label(app, text="Enter k (number of singular values to retain):").pack()
k_entry = tk.Entry(app)
k_entry.pack()

compress_btn = tk.Button(app, text="Compress Image", command=compress_image)
compress_btn.pack()

img_label = tk.Label(app)
img_label.pack()

app.mainloop()
