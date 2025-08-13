# Simple Notepad GUI Application

import tkinter as tk
from tkinter import filedialog, messagebox

def new_file():
    text.delete(1.0, tk.END)
    root.title("Notepad - New File")

def open_file():
    file = filedialog.askopenfilename(defaultextension=".txt",
                                      filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "r") as f:
            text.delete(1.0, tk.END)
            text.insert(tk.END, f.read())
        root.title(f"Notepad - {file}")

def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "w") as f:
            f.write(text.get(1.0, tk.END))
        root.title(f"Notepad - {file}")

def quit_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root = tk.Tk()
root.title("Notepad")
root.geometry("600x400")

text = tk.Text(root, undo=True)
text.pack(expand=True, fill=tk.BOTH)

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_command(label="Save As...", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit_app)

root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()