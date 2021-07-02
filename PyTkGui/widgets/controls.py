# -*- coding: utf-8 -*-
from PyTkGui.utils import get_real_master
import tkinter as tk
from tkinter import ttk
from ._base import Base, _Base
from .layouts import RowLayout


class Input(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Entry, master, **options)

        self.set_configure("variable", "textvariable")
        self.set_configure("type", "type", "normal")

        show_type = self.configures.pop("type", "normal")
        if show_type == "password":
            self.configures["show"] = "*"

        if self.configures["textvariable"] is not None:
            self.options.pop("text", None)
        else:
            self.widget.delete(0, "end")
            self.widget.insert(0, self.options.pop("text"))

class Button(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Button, master, **options)

class CheckButton(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Checkbutton, master, **options)

        self.set_configure("variable", "textvariable")

        if "textvariable" in self.configures.keys() and self.configures["textvariable"] is not None:
            self.configures.pop("text", None)

class RadioButton(Base):
    value = None

    def __init__(self, master, **options):
        super().__init__(ttk.Radiobutton, master, **options)

        self.set_configure("value", "value", 0)

    def render(self, **options):
        super().render(**options)

        radios = [ child for child in self.parent.children if isinstance(child, RadioButton) ]
        self.configure(value = radios.index(self))

        if not radios[0] == self:
            self.value = radios[0].value
        else:
            self.value = tk.IntVar()
            self.value.set(0)

        self.configure(variable = self.value)
            

class Range(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Scale, master, **options)

        self.set_configure("from", "from_", 0)
        self.set_configure("to", "to", 100)
        self.set_configure("value", "value", 0)
        self.set_configure("orient", "orient", "horizontal")

class Select(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Combobox, master, **options)

        self.defaults = {
            "index": self.options.pop("index", None),
            "value": self.options.pop("value", None)
        }

        self.widget.delete(0, "end")
        self.widget.configure(values = [], state = "readonly")

    @property
    def value(self) -> list:
        return list(self.widget["value"])
    
    @value.setter
    def value(self, new_value:list):
        self.widget.delete(0, "end")
        self.widget.configure(values = new_value)

    def render_children(self):
        self.widget.delete(0, "end")
        self.widget.configure(values = [])

        super().render_children()

class SelectItem(_Base):
    def __init__(self, master:Select, **options):
        super().__init__(master, **options)

    def render(self):
        super().render()

        if not self.has_iter:
            self.parent.value = self.parent.value + [ self.options["value"] ]
            if self.parent.defaults["index"] is not None:
                self.parent.widget.current(self.parent.defaults["index"])


class MenuBar(RowLayout):
    def __init__(self, master, **options):
        super().__init__(master, **options)

    def render(self, **options):
        options.pop("fill", None)
        options.pop("expand", None)

        super().render(**options)

class Menu(Base):
    def __init__(self, master:MenuBar, **options):
        super().__init__(ttk.Menubutton, master, **options)

        self.tk_menu = SubMenuFrame(self)
        self.configures["menu"] = self.tk_menu

    def render_children(self):
        super().render_children()

        self.tk_menu.render()

class SubMenuFrame(tk.Menu):
    menuitems = []

    def __init__(self, master:Menu):
        super().__init__(master.widget)

        self.configure(background = "white", tearoff = False)

    def render(self):
        for menuitem in self.menuitems:
            try:
                self.delete(menuitem.options["label"])
            except:
                pass

            self.add_command(background = "white", foreground = "black", **menuitem.options)

class MenuItem(_Base):
    def __init__(self, master:Menu, **options):
        super().__init__(master, **options)

        self.options = {
            "label": options.pop("text", "")
        }
        if "command" in options.keys():
            self.options["command"] = options["command"]

    def render(self, **_):
        self.parent.tk_menu.menuitems.append(self)
