import tkinter as tk
from Constants import *

def error_msg(title='', msg=''):
    tk.messagebox.showerror(title, msg)
    return

def truncate(array):
    if len(array) == MAX_DATA_POINTS:
        del array[0]
    return array
