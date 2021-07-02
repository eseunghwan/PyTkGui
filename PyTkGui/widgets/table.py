# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from typing import List, Any
from ._base import Base, _Base
from .layouts import RowLayout, ColumnLayout
from .controls import Input


class TableHeader(_Base):
    headers:List[str] = []

    def __init__(self, master, **_):
        super().__init__(master)
        self.headers = []

    def render_children(self):
        self.headers = []
        super().render_children()

        self.parent.headers = self.headers

class TableColumn(_Base):
    def __init__(self, master:TableHeader, **options):
        super().__init__(master, **options)

    def render(self, **_):
        super().render()

        if not self.has_iter:
            self.parent.headers.append(self.options["text"])

class TableBody(_Base):
    rows:List[List[Any]] = []

    def __init__(self, master, **_):
        super().__init__(master)
        self.rows = []

    def render_children(self):
        self.rows = []
        super().render_children()

        self.parent.rows = self.rows

class TableRow(_Base):
    row:List[Any] = []

    def __init__(self, master:TableBody, **options):
        super().__init__(master, **options)
        self.row = []

    def render(self, **_):
        super().render()

    def render_children(self):
        self.row = []
        super().render_children()

        if not self.has_iter:
            self.parent.rows.append(self.row)

class TableItem(_Base):
    def __init__(self, master:TableRow, **options):
        super().__init__(master, **options)

    def render(self, **_):
        super().render()

        if not self.has_iter:
            self.parent.row.append(str(self.options["value"]))


class Table(Base):
    editable:bool = False
    headers:List[str] = []
    rows:List[List[Any]] = []

    def __init__(self, master, **options):
        super().__init__(ttk.Treeview, master, **options)

        self.options["show"] = "headings"
        self.editable = self.options.pop("editable", False)

    def render(self, **options):
        super().render(**options)

        if self.editable:
            self.widget.bind("<Double-Button-1>", self.set_editable)

    def render_children(self):
        self.headers, self.rows = [], []
        self.widget.configure(columns = [])
        self.widget.delete(*self.widget.get_children())

        super().render_children()
        # print(self.headers, self.rows)

        self.widget.configure(columns = [ f"#{idx + 1}" for idx, _ in enumerate(self.headers) ])
        for hidx, header in enumerate(self.headers):
            self.widget.column(f"#{hidx + 1}")
            self.widget.heading(f"#{hidx + 1}", text = header)

        self.widget.configure(height = len(self.rows))
        for ridx, row in enumerate(self.rows):
            self.widget.insert("", ridx, values = row)

    
    def set_editable(self, event):
        _ridx = self.widget.identify_row(event.y)
        _cid = self.widget.identify_column(event.x)
        _cidx = int(_cid[1:]) - 1

        x, y, width, height = self.widget.bbox(_ridx, _cid)

        EditableItem(
            self.widget, ridx = _ridx, cidx = _cidx,
            value = self.widget.item(_ridx)["values"][_cidx]
        ).place(x = x, y = y, width = width, height = height, anchor = "nw")

class EditableItem(ttk.Entry):
    def __init__(self, master, **options):
        value = options.pop("value")
        self._ridx, self._cidx = options.pop("ridx"), options.pop("cidx")

        super().__init__(master, **options)

        self.insert(0, value)
        self.focus()

        self.bind("<Return>", self.apply_changed)
        self.bind("<Escape>", self.cancel_changed)

    def apply_changed(self, event):
        item_values = self.master.item(self._ridx)["values"]
        item_values[self._cidx] = self.get()
        self.master.item(self._ridx, values = item_values)

        self.cancel_changed(event)

    def cancel_changed(self, event):
        self.destroy()
