#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

def swap_pixels(image: Image.Image) -> Image.Image:
    pixels = list(image.getdata())
    pixels.reverse()
    img2 = Image.new(image.mode, image.size)
    img2.putdata(pixels)
    return img2

def xor_pixels(image: Image.Image, key: int) -> Image.Image:
    if not (0 <= key <= 255):
        raise ValueError("Key must be in the range 0–255 for XOR mode.")
    pixels = list(image.getdata())
    new_pixels = []
    for p in pixels:
        if len(p) >= 3:
            r, g, b = p[:3]
            new_pixels.append((r ^ key, g ^ key, b ^ key))
        else:
            new_pixels.append(p)
    img2 = Image.new(image.mode, image.size)
    img2.putdata(new_pixels)
    return img2

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encrypt/Decrypt Tool")
        self.root.geometry("600x450")

        # File paths and image
        self.input_path = ""
        self.output_image = None

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Method:").grid(column=0, row=0, sticky="w")
        self.method_var = tk.StringVar(value="swap")
        ttk.Combobox(frm, textvariable=self.method_var,
                     values=["swap", "xor"], state="readonly").grid(column=1, row=0)

        ttk.Label(frm, text="Mode:").grid(column=0, row=1, sticky="w")
        self.mode_var = tk.StringVar(value="encrypt")
        ttk.Combobox(frm, textvariable=self.mode_var,
                     values=["encrypt", "decrypt"], state="readonly").grid(column=1, row=1)

        ttk.Label(frm, text="XOR Key (0–255):").grid(column=0, row=2, sticky="w")
        self.key_entry = ttk.Entry(frm)
        self.key_entry.grid(column=1, row=2)

        ttk.Button(frm, text="Open Image", command=self.open_image).grid(column=0, row=3, columnspan=2, pady=5)
        self.image_label = ttk.Label(frm)
        self.image_label.grid(column=0, row=4, columnspan=2)

        ttk.Button(frm, text="Run", command=self.run).grid(column=0, row=5, columnspan=2, pady=10)

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            try:
                img = Image.open(path).convert("RGB")
                self.input_image = img
                self.input_path = path
                self.display_image(img)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")

    def display_image(self, img: Image.Image):
        img.thumbnail((200, 200))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

    def run(self):
        if not self.input_path:
            messagebox.showwarning("Warning", "Please open an image first.")
            return

        method = self.method_var.get()
        mode = self.mode_var.get()
        key = self.key_entry.get()

        try:
            image = self.input_image.copy()

            if method == "swap":
                result = swap_pixels(image)
            elif method == "xor":
                if not key.isdigit() or not (0 <= int(key) <= 255):
                    raise ValueError("Key must be an integer between 0 and 255.")
                result = xor_pixels(image, int(key))
            else:
                raise ValueError("Unknown method.")

            # Save file dialog
            output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                       filetypes=[("PNG files", "*.png")])
            if output_path:
                result.save(output_path)
                self.display_image(result)
                messagebox.showinfo("Success", f"{mode.title()}ion complete!\nSaved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Operation failed:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
