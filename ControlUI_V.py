# -*- coding: utf-8 -*-
#vertical version of UI
"""
Have indicator for each button indicating whether value is at optimal level or
needs adjusting/attention

Have an option to save image of graph to file

Allow user to resize window maintaining aspect ratio

Add images to buttons
"""
import time
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Constants import *

def config_frame(mode, start=0, end=1, weighting=1, uniform=''):
    for x in range(start, end): #adjust column/row weighting - less repetitive
        mode(x, weight=weighting, uniform=uniform)
        
def on_click(btn, btns):
    for x in btns: x.config(relief='flat')
    btn.config(relief='sunken') #reenable other buttons

class BioreactorUI(tk.Frame):
    def __init__(self, parent, manager, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.manager = manager
        self.init_widgets()
        
    def init_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=10)
        self.rowconfigure(0, weight=1)
        self.menu_bar = MenuBar(self, self.manager, 0.1*self.width, self.height,
                                highlightthickness=0, bg=MENU)
        self.menu_options=MenuBtns(self, 0.2*self.width,  self.height-20,
                                   highlightthickness=0,bg=GREY)
        self.graph_display = GraphFrame(self,0.7*self.width-10,self.height-40,
                                        highlightthickness=1, bg='white',
                                        highlightbackground=MENU,
                                        highlightcolor=MENU)
        for widget in (self.menu_bar, self.menu_options, self.graph_display):
            widget.grid_propagate(0)

    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.menu_bar.grid(row=0, column=0, sticky='NEW')
        self.menu_options.grid(row=0, column=1, sticky='NESW')
        self.graph_display.grid(row=0,column=2,sticky='NESW',pady=20,padx=(0,20))
    
class MenuBar(tk.Frame):
    def __init__(self, parent, manager, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.manager = manager
        self.init_widgets()
        self.update_time()

    def init_widgets(self):
        self.rowconfigure(0, weight=50)
        config_frame(self.rowconfigure, start=1, end=4, weighting=1, uniform='3')
        self.columnconfigure(0, weight=1)
        
        self.lbls = tk.Frame(self,bg=MENU,width=self.width,highlightthickness=0)
        self.lbls.columnconfigure(0, weight=1)
        self.lbls.grid_propagate(0)
        self.watch = tk.Label(self.lbls,font=(FONT, MEDIUM),fg='white',bg=MENU)
        self.status = tk.Label(self.lbls,font=(FONT,MEDIUM),fg='white',bg=MENU,
                               text='Bioreactor\n[Online]')
        
        self.modify_btn = tk.Button(self, text='MODIFY', relief='flat',
                                    font=(FONT_BOLD,MEDIUM),fg='white',bg=GREEN,
                                    activebackground=GREEN,highlightthickness=0)
        self.logout_btn=tk.Button(self, text='LOGOUT', relief='flat',
                                  font=(FONT_BOLD,MEDIUM), fg='white',bg=YELLOW,
                                  activebackground=YELLOW,highlightthickness=0,
                                  command=self.manager.open_login)
        self.shutdown_btn = tk.Button(self, text='SHUTDOWN', relief='flat',
                                      font=(FONT_BOLD,MEDIUM),fg='white',bg=RED,
                                      activebackground=RED,highlightthickness=0)
    
    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.lbls.grid(row=0, column=0, sticky='nesw', pady=20, padx=10)
        self.watch.grid(row=0, column=0, sticky='new', pady=(0, 20))
        self.status.grid(row=1, column=0, sticky='new', pady=(0, 20))
        
        self.modify_btn.grid(row=2, column=0, sticky='nesw',pady=(0,20),padx=20)
        self.logout_btn.grid(row=3, column=0, sticky='nesw',pady=(0,20),padx=20)
        self.shutdown_btn.grid(row=4,column=0,sticky='nesw',pady=(0,20),padx=20)

    def update_time(self):
        current_time = time.strftime('%A\n%H:%M:%S')
        self.watch.config(text=current_time)
        self.after(200, self.update_time)
        
class MenuBtns(tk.Frame):
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        self.init_widgets()

    def init_widgets(self):
        self.columnconfigure(0, weight=1)
        config_frame(self.rowconfigure, start=0, end=4, weighting=1, uniform='4')
            
        self.info_frame = tk.Frame(self,bg=BLUE,highlightthickness=0)
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.rowconfigure(0, weight=3)
        self.info_frame.rowconfigure(1, weight=1)
        self.info_val = tk.Label(self.info_frame, text='ADMIN', bg=BLUE,
                                 fg='white', font=(FONT_BOLD, LARGE))
        self.info_lbl = tk.Label(self.info_frame, text='Logged in as ↑', bg=BLUE,
                                 fg='white', font=(FONT, FONTSIZE))
        self.info_btn = tk.Button(self.info_frame, bg=BLUE, relief='flat',
                                  activebackground=BLUE)

        self.ph_frame = tk.Frame(self, bg=GREEN, highlightthickness=0)
        self.ph_frame.columnconfigure(0, weight=1)
        self.ph_frame.rowconfigure(0, weight=3)
        self.ph_frame.rowconfigure(1, weight=1)
        self.ph_val = tk.Label(self.ph_frame, text='7', bg=GREEN, fg='white',
                              font=(FONT_BOLD, LARGE))
        self.ph_lbl = tk.Label(self.ph_frame, text='Current pH of Yeast', bg=GREEN,
                               fg='white', font=(FONT, FONTSIZE))
        self.ph_btn = tk.Button(self.ph_frame, bg=GREEN, relief='flat',
                                activebackground=GREEN, highlightthickness=0)

        self.temp_frame = tk.Frame(self, bg=YELLOW, highlightthickness=0)
        self.temp_frame.columnconfigure(0, weight=1)
        self.temp_frame.rowconfigure(0, weight=3)
        self.temp_frame.rowconfigure(1, weight=1)
        self.temp_val = tk.Label(self.temp_frame, text='32°C',bg=YELLOW,fg='white',
                                 font=(FONT_BOLD, LARGE))
        self.temp_lbl = tk.Label(self.temp_frame, text='Current Temperature',
                                 bg=YELLOW, fg='white', font=(FONT, FONTSIZE))
        self.temp_btn = tk.Button(self.temp_frame, bg=YELLOW, relief='flat',
                                  activebackground=YELLOW, highlightthickness=0)

        self.spd_frame = tk.Frame(self, bg=RED, highlightthickness=0)
        self.spd_frame.columnconfigure(0, weight=1)
        self.spd_frame.rowconfigure(0, weight=3)
        self.spd_frame.rowconfigure(1, weight=1)
        self.spd_val = tk.Label(self.spd_frame, text='1500 RPM', bg=RED,
                                fg='white', font=(FONT_BOLD, LARGE))
        self.spd_lbl = tk.Label(self.spd_frame, text='Current Motor Speed', bg=RED,
                                fg='white', font=(FONT, FONTSIZE))
        self.spd_btn = tk.Button(self.spd_frame, bg=RED, relief='flat',
                                 activebackground=RED, highlightthickness=0)

        self.info_btn.config(command=lambda btn=self.info_btn,
                             btns=[self.temp_btn, self.ph_btn, self.spd_btn]:
                             on_click(btn, btns))

        self.ph_btn.config(command=lambda btn=self.ph_btn,
                             btns=[self.info_btn, self.temp_btn, self.spd_btn]:
                             on_click(btn, btns))
        
        self.temp_btn.config(command=lambda btn=self.temp_btn,
                             btns=[self.info_btn, self.ph_btn, self.spd_btn]:
                             on_click(btn, btns))
        
        self.spd_btn.config(command=lambda btn=self.spd_btn,
                             btns=[self.info_btn, self.ph_btn, self.temp_btn]:
                             on_click(btn, btns))
        
        for widget in self.winfo_children():
            widget.grid_propagate(0)

    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        self.info_frame.grid(row=0, column=0, sticky='nesw',pady=(20,0),padx=20)
        self.info_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=10)
        self.info_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.info_btn.grid(row=0, column=0,columnspan=2,rowspan=2,sticky='nesw')
        self.info_btn.lower()
        
        self.ph_frame.grid(row=1, column=0, sticky='nesw', pady=(20,0), padx=20)
        self.ph_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=10)
        self.ph_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.ph_btn.grid(row=0, column=0, columnspan=2, rowspan=2,sticky='nesw')
        self.ph_btn.lower()
        
        self.temp_frame.grid(row=2, column=0, sticky='nesw',pady=(20,0),padx=20)
        self.temp_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=10)
        self.temp_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.temp_btn.grid(row=0,column=0,columnspan=2,rowspan=2,sticky='nesw')
        self.temp_btn.lower()
        
        self.spd_frame.grid(row=3, column=0, sticky='nesw', pady=20, padx=20)
        self.spd_val.grid(row=0, column=0, sticky='nsw', pady=10, padx=5)
        self.spd_lbl.grid(row=1, column=0, pady=10, sticky='nsw', padx=5)
        self.spd_btn.grid(row=0, column=0, columnspan=2,rowspan=2,sticky='nesw')
        self.spd_btn.lower()

class GraphFrame(tk.Frame):
    def __init__(self, parent, width, height, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.parent, self.width, self.height = parent, width, height
        matplotlib.use("TkAgg")
        self.init_widgets()
        self.plot_graph()
        
    def init_widgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

    def grid(self, **kwargs):
        super(tk.Frame, self).grid(**kwargs)

    def plot_graph(self):
        #setup
        figure = plt.Figure()
        graph_plot = figure.add_subplot(1, 1, 1)
        x = [60, 120, 180, 240]
        y = [29, 30, 32, 31]
        #plotting
        graph_plot.plot(x, y, color=RED)
        graph_plot.set_title('Temperature of yeast against time',fontsize=16,
                        color=RED, horizontalalignment='right', fontname=FONT)
        graph_plot.set_xlabel('Time (seconds)', fontsize=FONTSIZE, color=RED,
                              horizontalalignment='right', fontname=FONT)
        graph_plot.set_ylabel('Temperature (Celsius)',fontsize=FONTSIZE,color=RED,
                              verticalalignment='baseline', fontname=FONT)
        graph_plot.tick_params(color=MENU, labelcolor=MENU)
        for spine in graph_plot.spines.values():
            spine.set_edgecolor(MENU)
        #display using tk
        self.graph_canvas = FigureCanvasTkAgg(figure, self)
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, sticky='nesw',
                                               padx=(0, 10))
        self.graph_canvas.draw()
