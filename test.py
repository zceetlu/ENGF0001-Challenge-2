import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

SCREENWIDTH, SCREENHEIGHT = 1280, 720

class UI(tk.Frame):
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        for x in range(3): self.rowconfigure(x, weight=1)
        self.graph_display = GraphFrame(self, self.width-40, 0.7*self.height-15,
                                        highlightthickness=0, bg='white')

    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.graph_display.grid(row=2, sticky='NESW', padx=20, pady=(0, 20))

class GraphFrame(tk.Frame):
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        matplotlib.use("TkAgg")
        self.plot_graph()
        
    def plot_graph(self):
        figure = plt.Figure()
        graph_plot = figure.add_subplot(1, 1, 1)
        self.graph_canvas = FigureCanvasTkAgg(figure, self)
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, sticky='nesw', pady=20)

if __name__ == '__main__':
    win = tk.Tk()
    ui = UI(win,SCREENWIDTH,SCREENHEIGHT,bg='grey',highlightthickness=0)
    ui.grid(row=0, column=0, sticky='nesw')
    win.mainloop()
