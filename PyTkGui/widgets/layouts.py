# -*- coding: utf-8 -*-
from tkinter import ttk
from ._base import Base


class RowLayout(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Frame, master, **options)

    def render_children(self):
        super().render_children()

        for child in self.children:
            child.pack_options["side"] = "left"
            if not "fill" in child.pack_options.keys() or not child.pack_options["fill"] == "both":
                child.pack_options["fill"] = "y"

            child.widget.pack_configure(**child.pack_options)

class ColumnLayout(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Frame, master, **options)

    def render_children(self):
        super().render_children()

        for child in self.children:
            child.pack_options["side"] = "top"
            if not "fill" in child.pack_options.keys() or not child.pack_options["fill"] == "both":
                child.pack_options["fill"] = "x"

            child.widget.pack_configure(**child.pack_options)

class GroupBox(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Labelframe, master, **options)

        self.set_configure("title", "text", "")

    def render_children(self):
        if not len(self.children) == 1:
            raise RuntimeError("Groupbox have only 1 child layout!")

        super().render_children()

        self.widget.winfo_children()[0].pack_configure(fill = "both", expand = True)

class Slot(Base):
    def __init__(self, master):
        super().__init__(ttk.Frame, master)
