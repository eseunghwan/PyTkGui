# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from typing import List
from ._base import Base
from .layouts import RowLayout, ColumnLayout


class TableColumnTk(tk.Label, Base):
    def __init__(self, master, options:dict, extras:dict):
        tk.Label.__init__(self, self.get_real_master(master), background = "slategray", foreground = "white")
        Base.__init__(self, options, extras, { "anchor": [ "anchor", "center" ] })

        self.configure(**self.options)
        self.configure(**self.configures)

class TableColumn(Base):
    def __init__(self, master, options, **extras):
        super().__init__(options, extras)

        master.columns.append(self)

    def to_tk(self, master) -> TableColumnTk:
        widget = TableColumnTk(master, self.options, self.extras)
        # master.tk_widgets.append(widget)

        return widget

class TableHeader:
    columns:List[TableColumn] = []

    def __init__(self, master, options):
        self.table = master
        self.table.header = self

class TableItemTk(ttk.Label, Base):
    def __init__(self, master, options, extras):
        ttk.Label.__init__(self, self.get_real_master(master))
        Base.__init__(self, options, extras, { "value": [ "value", "" ] })

        self.value = self.configures.pop("value")
        self.configures["text"] = self.value

        self.configure(**self.options)
        self.configure(**self.configures)

class TableItem(Base):
    def __init__(self, master, options, **extras):
        super().__init__(options, extras)

        master.items.append(self)

    def to_tk(self, master) -> TableItemTk:
        widget = TableItemTk(master, self.options, self.extras)
        # master.tk_widgets.append(widget)

        return widget

class TableRow(Base):
    items:List[TableItem] = []

    def __init__(self, master, options, **extras):
        super().__init__(options, extras)

        self.__body = master
        self.table = master.table

        self.__body.rows.append(self)

class TableBody:
    rows:List[TableRow] = []

    def __init__(self, master, options):
        self.table = master
        self.table.body = self

class Table(ttk.Frame, Base):
    editable:bool = False
    header:TableHeader = None
    body:TableBody = None
    tk_widgets:List[ttk.Widget] = []

    def __init__(self, master, options:dict, **extras):
        ttk.Frame.__init__(self, master)
        Base.__init__(self, options, extras, { "editable": [ "editable", False ] })

        self.editable = self.configures.pop("editable", False)

        self.configure(**self.options)
        self.configure(**self.configures)
        self.configure(style = "Table.TFrame")

    def render(self):
        for child in self.tk_widgets:
            child.grid_forget()
            child.destroy()

        if self.header is not None:
            for cidx, column in enumerate(self.header.columns):
                if column.is_cond:
                    c = column.to_tk(self)
                    self.tk_widgets.append(c)
                    c.grid(row = 0, column = cidx, sticky = "nsew", padx = "0 1")

            if self.body is not None:
                rows = [ row for row in self.body.rows if row.is_cond ]
                for ridx, row in enumerate(rows):
                    items = [
                        item for column, item in zip(self.header.columns, row.items) if column.is_cond and item.is_cond
                    ]
                    for cidx, item in enumerate(items):
                        item.to_tk(self).grid(row = ridx + 1, column = cidx, sticky = "nsew")
        # if self.header is not None:
        #     self.configure(columns = [ f"#{idx}" for idx in range(len(self.header.columns)) ])

        #     for cidx, column in enumerate(self.header.columns):
        #         text = column.options.pop("text")
        #         self.column(f"#{cidx + 1}", **self.options)
        #         self.heading(f"#{cidx + 1}", text = text, **self.options)
        #         column.options["text"] = text

        #     if self.content is not None:
        #         self.configure(height = len(self.content.rows))
        #         for ridx, row in enumerate(self.content.rows):
        #             self.insert("", ridx, values = [ item.value for item in row.items ])
