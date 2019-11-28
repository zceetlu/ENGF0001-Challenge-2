import tkinter as tk

class FlashableLabel(tk.Label):
    def Flash(self, Count):
        bg = self.cget('bg')
        fg = self.cget('fg')
        if 'white' not in (bg, fg): fg='white'
        self.config(bg=fg, fg=bg)
        Count +=1
        if (Count < 6): self.after(165, lambda Count=Count: self.Flash(Count))
        
class GradientFrame(tk.Canvas):
    def __init__(self, parent, Color1="red", Color2="black", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1, self._color2 = Color1, Color2
        self.bind("<Configure>", self._draw_gradient)
    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width, height = self.winfo_width(), self.winfo_height()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")
        
class RoundedEntry(tk.Frame):
    def __init__(self, Parent, _font='Arial', _fg='black', width=300, height=25, cursor_colour='black', **kwargs):
        tk.Frame.__init__(self, Parent, **kwargs)
        #tk.Entry.__init__(self, Parent, relief='flat', state='readonly', **kwargs)
        self._width, self._height = width, height   
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self._Background = tk.Canvas(self, width=self._width,height=self._height,
                                     highlightthickness=0, bg=Parent.cget('bg'))
        self._Entry = tk.Text(self, font=_font, fg=_fg, relief='flat', height=self._height//25, insertbackground=cursor_colour,
                              width=self._width//6, wrap='none', **kwargs)
        self._Entry.grid_propagate(False)
        self._Background.grid_propagate(False)
        self.grid_propagate(False)
        #self._Background.bind('<Configure>', self.inner_resize) 
        self._Entry.bind("<Key>", self.check_key)
        self.bind = self._Entry.bind
        self.config = self._Entry.config
        self.delete = self._Entry.delete
        #self.icursor = self._Entry.icursor
        self.index = self._Entry.index
        self.scan_dragto = self._Entry.scan_dragto
        self.scan_mark = self._Entry.scan_mark
       # self.select_adjust = self._Entry.select_adjust
       # self.select_clear = self._Entry.select_clear
       # self.select_from = self._Entry.select_from
       # self.select_present = self._Entry.select_present
       # self.select_range = self._Entry.select_range
       # self.select_to = self._Entry.select_to
        self.xview = self._Entry.xview
        self.xview_moveto = self._Entry.xview_moveto
        self.xview_scroll = self._Entry.xview_scroll       

    def check_key(self, event):
        if event.keysym == "Return": return "break"
    def get(self, **kwargs): return self._Entry.get(1.0, 'end')[:-1]
    def insert(self, Text, **kwargs): return self._Entry.insert(1.0, str(Text))
    
    def grid(self, radius=25, fill='black', **kwargs):
        super(tk.Frame, self).grid(**kwargs)
        x1, y1, x2, y2 = 0, 0, self._width, self._height
        self._Background.grid(row=0, column=0, sticky='nesw')
        self._Entry.grid(row=0, column=0,sticky='n',padx=radius//2, pady=(2,0))
        points = (x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1)
        return self._Background.create_polygon(points, fill=fill, smooth=True, tags='edge')

class ScrolledFrame(tk.Frame): #when using frame, place child widgets in frame.inner
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._canvas = tk.Canvas(self)
        self.inner = tk.Frame(self._canvas)
        self._window = self._canvas.create_window((0, 0), window=self.inner, anchor='nw')
        self.inner.bind('<Configure>', self.resize)
        self.resize_width = self.resize_height = False
        self._canvas.bind('<Configure>', self.inner_resize)        
        self._vertical_bar = tk.Scrollbar(self, orient='vertical', command=self._canvas.yview)    
        self._canvas.configure(yscrollcommand=self._vertical_bar.set)
        self._horizontal_bar = tk.Scrollbar(self, orient='horizontal', command=self._canvas.xview)
        self._canvas.configure(xscrollcommand=self._horizontal_bar.set)

    def grid(self, vertical=True, horizontal=False, **kwargs):
        super().grid(**kwargs)
        self.display(vertical, horizontal)

    def pack(self, vertical=True, horizontal=False, **kwargs):
        super().pack(**kwargs)
        self.display(vertical, horizontal)
        
    def display(self, vertical, horizontal):
        columns, rows = self.inner.grid_size()
        self._canvas.grid(row=0, column=0, sticky='news')
        if vertical: self._vertical_bar.grid(row=0, column=columns, sticky='ns', rowspan=rows)        
        if horizontal: self._horizontal_bar.grid(row=rows,column=0,sticky='wes', columnspan=columns )
    def resize(self, event=None): self._canvas.configure(scrollregion=self._canvas.bbox('all'))
    def inner_resize(self, event):
        if self.resize_width: self._canvas.itemconfig(self._window, width=event.width)
        if self.resize_height: self._canvas.itemconfig(self._window, height=event.height)      
