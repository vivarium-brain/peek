from neurograph import openng

import math
import os
import tkinter as tk
from PIL import Image

tk_root = None

def find_optimal_packing(num):
    if num <= 0:
         return (0,0)
    if num == 1:
        return (1, 1)

    sqrt_circles = math.sqrt(num)
    best_width = 1
    best_height = num
    min_aspect_diff = num
    min_area = num*num

    for width in range(1, int(math.ceil(sqrt_circles)) + 1):
        if num % width == 0:
            height = num // width
        else:
           height = num // width + 1
        area = width*height

        aspect_diff = abs(width - height)

        if aspect_diff < min_aspect_diff or (aspect_diff == min_aspect_diff and area < min_area):
            min_aspect_diff = aspect_diff
            min_area = area
            best_width = width
            best_height = height


    return (best_width, best_height)

def clear():
    tk_root.canvas.delete("all")

def open(filename):
    ng = openng(filename, 'r')
    index = ng.sections['index'][0]
    synaptic = ng.sections['synaptic'][0]
    total = len(index)

    width, height = find_optimal_packing(total)

    offx = 5
    offy = 5
    size = 50
    padx = 50
    pady = 50

    index_xy = [None] * total

    for x in range(width):
        for y in range(height):
            if x*height+y >= total: break
            index_xy[x*height+y] = (
                offx+x*size+x*padx+size/2,
                offy+y*size+y*pady+size/2
            )

    for idx,syn in synaptic.items():
        x1, y1 = index_xy[idx]
        for idx2,weight in syn.items():
            x2, y2 = index_xy[idx2]
            tk_root.canvas.create_line(x1+size/2, y1+size/2, x2+size/2, y2+size/2,
                                       fill="#33cc00" if weight > 0 else "#ff5c33",
                                       width=abs(weight/2))

    for idx in range(total):
        x, y = index_xy[idx]
        tk_root.canvas.create_oval(
            x, y, x+size, y+size,
        fill="#FFFFFF", outline="#00FF00")
        tk_root.canvas.create_text(x+size/2, y+size/2, text=index[idx], fill="#000000")

    tk_root.canvas.configure(
        scrollregion=tk_root.canvas.bbox("all")
    )

def save(filename):
    x, y, w, h = tk_root.canvas.bbox("all")
    tk_root.canvas.postscript(
        file=filename+'.eps',
        width=w-x, height=h-y)
    
    img = Image.open(filename+'.eps')
    # original = [float(d) for d in img.size]
    img.load(scale=3)

    # img = Image.open(filename+'.eps')
    # w, h = img.size
    # img = img.resize((w * 3, h * 3))
    img.save(filename, dpi=(500, 500))
    os.remove(filename+'.eps')

def init(root):
    global tk_root
    tk_root = root