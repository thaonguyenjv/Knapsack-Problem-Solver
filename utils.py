import time
import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

def plot_convergence(history, algo_name):
    plt.plot(history)
    plt.title(f"Convergence - {algo_name}")
    plt.xlabel("Iteration")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.show()

def animate_convergence(history, root):
    win = tk.Toplevel(root)
    win.title("GA Convergence")
    c = tk.Canvas(win, width=600, height=300, bg="white")
    c.pack()

    for i in range(1, len(history)+1):
        c.delete("all")
        scale_x = 550 / len(history)
        scale_y = 250 / max(history)
        for j in range(1, i):
            x1, y1 = (j-1)*scale_x+25, 275 - history[j-1]*scale_y
            x2, y2 = j*scale_x+25, 275 - history[j]*scale_y
            c.create_line(x1, y1, x2, y2, fill="blue", width=2)
        c.create_text(50, 20, text=f"Gen {i}/{len(history)}", anchor="w")
        win.update()
        time.sleep(0.1)

def animate_particles(history, root):
    win = tk.Toplevel(root)
    win.title("PSO Animation")
    c = tk.Canvas(win, width=400, height=400, bg="white")
    c.pack()

    for frame in history:
        c.delete("all")
        for (x, y) in frame:
            c.create_oval(x*380, y*380, x*380+5, y*380+5, fill="red")
        win.update()
        time.sleep(0.1)

def timeit(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return end - start, result

def generate_random_items(n):
    return np.random.rand(n, 2)
