#!/usr/bin/env python3
import IntroUI
import LoginUI
import ControlUI_V as C_UI
from Constants import *
import tkinter as tk

class UI_Manager:
    def __init__(self, parent):
        self.parent = parent
        self.loaded = False

    def load(self):
        self.close_all()
        self.load_screen=IntroUI.SplashScreen(self.parent, SCREENWIDTH,
                                              SCREENHEIGHT, bg=GREY,
                                              highlightthickness=0)
        self.load_screen.grid(row=0, column=0, sticky='nesw')
        self.load_screen.animate()

    def run(self):
        self.close_all()
        if not self.loaded:
            self.load()
            self.loaded = True
        self.open_login()

    def open_login(self):
        self.close_all()
        self.login=LoginUI.LoginMenu(self.parent,self,SCREENWIDTH,SCREENHEIGHT,
                                     bg=GREY, highlightthickness=0)
        self.login.grid(row=0, column=0, sticky='nesw')
        
    def check_login(self, event=None):
        username = self.login.user_entry.get()
        password = self.login.pass_entry.get()
        if username == 'ADMIN' and password == '12345':
            self.close_all()
            self.open_dashboard()
        else:
            msg = 'Your login details were incorrect, please try again'
            tk.messagebox.showwarning('Login unsuccessful', msg)
            self.open_login()
        
    def open_dashboard(self):
        self.close_all()
        self.dashboard=C_UI.BioreactorUI(self.parent,self,SCREENWIDTH,
                                         SCREENHEIGHT,  bg=GREY,
                                         highlightthickness=0)
        self.dashboard.grid(row=0, column=0, sticky='nesw')
        self.parent.update()

    def close_all(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

class Settings:
    def __init__(self, parent):
        self.parent = parent
        self.orientation = 'Horizontal'

    def change_orientation(self): #work in progress
        pass

def close_ui(win, event=None):
    try:
        if tk.messagebox.askokcancel('Quit?','Do you really want to close the UI?'):
            win.destroy()
    except AttributeError: win.destroy()
    
def centralise(win):
    win.update_idletasks() 
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def init_win():  
    win = tk.Tk(className='bioreactor UI')
    win.title('Bioreactor UI')
    #win.tk.call('wm', 'iconphoto', win._w, tk.PhotoImage(file='icon.gif'))
    #win.iconbitmap(bitmap='@icon.XBM')
    win.wm_iconbitmap(bitmap = "@icon.XBM")
    win.geometry('{}x{}'.format(SCREENWIDTH, SCREENHEIGHT))
    win.resizable(False, False)
    win.rowconfigure(1, weight=1)
    win.bind('<Escape>', lambda event, win=win: close_ui(win, event))
    centralise(win)
    return win

if __name__ == '__main__':
    win = init_win()
    #var = Settings()
    UI = UI_Manager(win)
    UI.run()
    win.mainloop()
