# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Union
from tkinter import Tk, IntVar, DoubleVar, BooleanVar, StringVar
from tkinter.ttk import Style
from .utils import get_real_master


class Component:
    initialized:bool = False
    rendered:bool = False
    root = None
    data:list = []

    def __init__(self, master):
        self.master = master
        self.initialized = True
        self.rendered = False
        self.data = []

        self.created()

    def __repr__(self):
        return repr(self.root)

    def created(self):
        pass

    def mounted(self):
        pass

    def get_data(self, name:str):
        return getattr(self, name)

    def render(self, **options):
        self.root.render(**options)
        self.root.render_children()

        if not self.rendered:
            self.rendered = True
            self.mounted()

class Router:
    def __init__(self, route_info:List[Dict[str, Any]]):
        self.info = route_info

class Variable:
    def __init__(self, obj:Component, master, name:str, value):
        master = get_real_master(master)

        if isinstance(value, int):
            var = IntVar(master, value)
        elif isinstance(value, float):
            var = DoubleVar(master, value)
        elif isinstance(value, bool):
            var = BooleanVar(master, value)
        elif isinstance(value, str):
            var = StringVar(master, value)
        else:
            var = None

        obj.data.append(name)

        if var is None:
            setattr(obj, name, value)
        else:
            setattr(obj.__class__, name, property(lambda _: var.get(), lambda _,v: var.set(v)))
            setattr(obj, f"{name}_var", var)

class Eventer:
    def __init__(self, comp:Component, name:str):
        self.fn = getattr(comp, name)
        self.comp = comp

    def __call__(self):
        self.fn()
        self.comp.root.render_children()

class GlobalStyle(Style):
    def __init__(self, master:Tk):
        super().__init__(master)

        self.theme_use("default")
        font_size = int(master.winfo_screenheight() * 0.012)
        if font_size > 15:
            font_size = 15

        font_info = ("Arial", font_size)

        self.configure("TFrame", background = "white")
        self.configure("TLabelframe", background = "white")
        self.configure("TLabelframe.Label", background = "white", font = font_info)
        self.configure("TLabel", background = "white", foreground = "black", font = font_info)

        self.configure("TButton", background = "slategray", foreground = "white", font = font_info)
        self.map("TButton", background = [ ("active", "darkgray") ], foreground = [ ("active", "white") ])
        self.configure("TMenubutton", font = font_info)
        self.configure("TCheckbutton", background = "white", foreground = "black", font = font_info)
        self.map("TCheckbutton", background = [ ("!active", "white") ])
        self.configure("TRadiobutton", background = "white", foreground = "black", font = font_info)
        self.map("TRadiobutton", background = [ ("!active", "white") ])

        self.configure("TEntry", background = "white", fieldbackground = "white", foreground = "black", font = font_info)
        self.map("TEntry", fieldbackground = [ ("disabled", "white") ], foreground = [ ("disabled", "black") ])
        self.configure("TCombobox", fieldbackground = "white", selectbackground = "transparent", fieldforeground = "black", selectforeground = "black", font = font_info)
        self.map("TCombobox", fieldbackground = [ ("disabled", "white"), ("readonly", "white") ])

        self.configure("Treeview", background = "white", foreground = "black", rowheight = font_size + 10, font = font_info)
        self.map("Treeview", background = [ ("selected", "lightgray") ], foreground = [ ("selected", "black") ])
        self.configure("Treeview.Heading", background = "slateblue", foreground = "white", font = font_info)
        self.map("Treeview.Heading", background = [ ("!active", "slateblue") ])
        
        el_name, el_info = self.layout("TEntry")[0]
        el_info.pop("border", None)
        self.layout("TEntry", [ (el_name, el_info) ])

class ComponentStyle(Style):
    def __init__(self, master):
        super().__init__(get_real_master(master))

        self.theme_use("default")
