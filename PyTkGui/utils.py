# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

def get_real_master(master):
    if isinstance(master, (tk.Tk, tk.Widget, ttk.Widget)):
        real_master = master
    elif hasattr(master, "widget"):
        real_master = getattr(master, "widget")
    elif hasattr(master, "initialized"):
        if hasattr(master, "socket"):
            real_master = getattr(master, "socket")
        else:
            real_master = getattr(master, "root")

    return real_master
