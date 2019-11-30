import tkinter as tk
from threading import Thread
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from random import randint

class Animation:
    def __init__(self):
        matplotlib.use("TkAgg")
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.x = 0
        self.xs, self.ys = [], []
        self.graph_canvas = FigureCanvasTkAgg(self.fig, win)
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, sticky='nesw',
                                               padx=10)

    def animate(self, i):
        y = randint(1400, 1600)
        self.xs.append(self.x)
        self.ys.append(y)
        
        self.ax.clear()
        self.ax.plot(self.xs, self.ys)
        
        self.x += 0.5

    def run(self):
        anim = animation.FuncAnimation(self.fig, self.animate,interval=250)
        self.graph_canvas.draw()
        win.update()

win = tk.Tk()
Anim = Animation()
Anim.run()
win.mainloop()
