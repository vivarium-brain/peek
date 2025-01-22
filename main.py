import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as tk_fd

import visualiser

root = tk.Tk()
root.resizable(False, False)
root.geometry('800x600')

def openfile():
    filename = tk_fd.askopenfilename(
        parent=root,
        title='Open neurograph file',
        filetypes=(
            ('Neurograph', '*.ng'),
            ('All files', '*.*')
        )
    )
    visualiser.clear()
    if filename is tuple or not filename or filename == ():
        return
    visualiser.open(filename)

def savefile():
    filename = tk_fd.asksaveasfilename(
        parent=root,
        title='Save visualised render',
        defaultextension=".png",
        filetypes=(
            ('Bitmap Picture', '*.bmp'),
            ('Portable Network Graphics', '*.png'),
            ('Joint Photographic Experts Group', '*.jpeg'),
            ('Truevision Advanced Raster Graphics Adapter', '*.tga'),
            ('Web Picture', '*.webp')
        )
    )
    if filename is tuple or not filename or filename == ():
        return
    visualiser.save(filename)

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_command(label="Save", command=savefile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

h = ttk.Scrollbar(orient=tk.HORIZONTAL)
v = ttk.Scrollbar(orient=tk.VERTICAL)
root.canvas = tk.Canvas(scrollregion=(0, 0, 800-25, 600-25), bg="white", yscrollcommand=v.set, xscrollcommand=h.set)
h["command"] = root.canvas.xview
v["command"] = root.canvas.yview
 
root.canvas.grid(column=0, row=0, sticky=(tk.N,tk.W,tk.E,tk.S))
h.grid(column=0, row=1, sticky=(tk.W,tk.E))
v.grid(column=1, row=0, sticky=(tk.N,tk.S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

visualiser.init(root)

root.mainloop()