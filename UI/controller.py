#!/usr/bin/env python3
'''
Uses alot of cpu - 100% of 3/8 cores
Tk error when messagebox is open and user closes UI - check if dialogbox is open
before closing
Fix serial error handling-user unplugs device, user plugs in device after login
'''
import IntroUI, LoginUI, Utilities, Serial, Bioreactor, Updater, serial
import c_ui_v2 as C_UI
from Constants import *
import tkinter as tk

class UI_Manager:
    def __init__(self, parent):
        self.parent, self.connected, self.logged_in = parent, False, False
        self.loaded, self.graph_colour, self.serial = False, None, None
        self.vals = {'pH': [], 'temperature': [], 'speed': []}
        self.current_graph = ''

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
        self.logged_in = False
        self.close_all()
        self.login=LoginUI.LoginMenu(self.parent,self,SCREENWIDTH,SCREENHEIGHT,
                                     bg=GREY, highlightthickness=0)
        self.login.grid(row=0, column=0, sticky='nesw')
        
    def check_login(self, event=None):
        username = self.login.user_entry.get()
        password = self.login.pass_entry.get()
        if username == USERNAME and password == PASSWORD:
            self.close_all()
            self.open_dashboard('ADMIN')
        else:
            msg = 'Your login details were incorrect, please try again'
            tk.messagebox.showwarning('Login unsuccessful', msg)
            self.open_login()
        
    def open_dashboard(self, user='GUEST'):
        self.close_all()
        self.logged_in = True
        self.dashboard=C_UI.BioreactorUI(self.parent,self, user, SCREENWIDTH,
                                         SCREENHEIGHT, bg=GREY,
                                         highlightthickness=0)
        self.dashboard.grid(row=0, column=0, sticky='nesw')
        self.parent.update()
        self.run_dashboard()

    def run_dashboard(self):
        self.dashboard.graph_display.default_screen()
        self.connected = self.serial_connect()
        if self.connected:
            reactor.serial_port = self.serial
            self.graph_setup()
            if self.read_from_serial_port():
                self.dashboard.graph_display.anim.event_source.stop()
                self.close_serial_port()
                self.dashboard.graph_display.default_screen()

    def config_updater(self):
        self.updater_win = tk.Toplevel(win)
        self.updater_win.geometry('{}x{}'.format(int(0.5*SCREENWIDTH), int(0.5*SCREENHEIGHT)))
        self.updater_win.title('Alter pH, Temperature and Stirring Speed of bioreactor')
        self.updater_win.columnconfigure(0, weight=1)
        self.updater_win.rowconfigure(0, weight=1)
        self.updater_win.attributes('-topmost',True)
        self.updater_win.update()
        self.updater_win.attributes('-topmost',False)
        Utilities.centralise(self.updater_win)

    def open_updater(self):
        self.config_updater()
        self.modify_ui = Updater.UpdaterUI(self.updater_win, reactor,
                                           width=0.5*SCREENWIDTH,
                                           height=0.5*SCREENHEIGHT)
        self.modify_ui.grid(row=0, column=0, sticky='nesw')
        
    def serial_connect(self):
        try:
            self.serial = Serial.SerialPort(port=PORT, baud_rate=BAUD_RATE)
            return True
        except (OSError, serial.serialutil.SerialException):
            Utilities.error_msg('No connection established',
                                'Board is not connected! Cannot read serial data from it.')
            self.parent.update_idletasks()
            if self.logged_in: #wait 1s before checking for connection again
                self.parent.after(RETRY_DELAY, self.serial_connect) 

    def graph_setup(self):
        self.dashboard.graph_display.setup_graph()
        self.change_graph('Stirring Speed', 'Stirring Speed (RPM)', RED,
                          self.dashboard.menu_options.spd_canv, 'speed')
        self.dashboard.graph_display.run_animation()
        
    def read_from_serial_port(self):
        if self.serial is None: return True
        subsystem, value, elapsed_time = self.serial.read_value()
        if len([x for x in (subsystem, value, elapsed_time) if x == False]) > 0:
            return True #fix ending
        if (len([x for x in (subsystem, value, elapsed_time) if x is None]) == 0
            and subsystem in self.vals.keys()):
            self.vals[subsystem] = Utilities.truncate(self.vals[subsystem])
            self.vals[subsystem].append((elapsed_time, value))
        self.update_data()
        self.parent.after(SERIAL_DELAY, self.read_from_serial_port)
            
    def toggle_btns(self, active):
        btns=[self.dashboard.menu_options.ph_canv,
              self.dashboard.menu_options.temp_canv,
              self.dashboard.menu_options.spd_canv]
        for btn in btns:
            if btn == active:
                btn.config(highlightbackground='black', highlightthicknes=3)
            else: btn.config(highlightbackground=MENU, highlightthicknes=0)

    def update_data(self):
        reactor.ph = self.vals['pH'][-1][1]
        reaactor.temperature = self.vals['temperature'][-1][1]
        reactor.speed = self.vals['speed'][-1][1]
        self.dashboard.graph_display.xs = [x[0] for x in self.vals[self.current_graph]]
        self.dashboard.graph_display.ys = [y[1] for y in self.vals[self.current_graph]]
        self.dashboard.menu_options.update_lbls()
        self.dashboard.menu_bar.update_status()
        
    def change_graph(self, title, y_axis, colour, btn, graph, event=None):
        self.toggle_btns(btn)
        self.current_graph = graph
        self.dashboard.graph_display.graph_title = title
        self.update_data()
        self.dashboard.graph_display.y_axis = y_axis
        self.dashboard.graph_display.graph_colour = colour
        self.dashboard.graph_display.update_graph_axes()

    def close_serial_port(self):
        if self.serial is not None:
            self.serial.running = False
            self.serial.close()
            self.serial = None
            
    def shutdown(self):
        if tk.messagebox.askyesno('Confirm shutdown', 'Shutdown bioreactor?'):
            self.close_serial_port()
        self.open_login()
        
    def close_all(self):
        self.close_serial_port()
        self.__init__(self.parent)
        for widget in self.parent.winfo_children():
            widget.destroy()

def close_ui(win, event=None):
    try:
        if tk.messagebox.askokcancel('Quit?','Do you really want to close the UI?'):
            win.quit() #stop mainloop before destroying window
            win.destroy()
    except AttributeError:
        win.quit()
        win.destroy()

def init_win():  
    win = tk.Tk(className='bioreactor UI')
    win.title('Bioreactor UI')
    win.wm_iconbitmap(bitmap = "@icon.XBM")
    win.geometry('{}x{}'.format(SCREENWIDTH, SCREENHEIGHT))
    win.resizable(False, False)
    win.rowconfigure(1, weight=1)
    win.bind('<Escape>', lambda event, win=win: close_ui(win, event))
    win.protocol("WM_DELETE_WINDOW", lambda win=win: close_ui(win))
    Utilities.centralise(win)
    return win

if __name__ == '__main__':
    reactor = Bioreactor.Bioreactor()
    win = init_win()
    UI = UI_Manager(win)
    #UI.run()
    #UI.open_login()
    UI.open_dashboard()
    win.mainloop()
