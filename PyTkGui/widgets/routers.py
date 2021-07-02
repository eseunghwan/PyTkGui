# -*- coding: utf-8 -*-
from tkinter import ttk
from typing import List, Dict, Any
from ._base import Base
from ..objects import Component


class RouterLink(Base):
    def __init__(self, master, comp, to:str, **options):
        super().__init__(ttk.Label, master, **options)

        self.comp, self.to = comp, to

    def link_to(self, event):
        self.comp.router_view.switch_view(self.to)

    def render(self, **options):
        super().render(**options)

        self.widget.bind("<Button-1>", self.link_to)

class RouterView(Base):
    routes:List[Dict[str, Component]] = []

    def __init__(self, master, root):
        super().__init__(ttk.Frame, master)

        if hasattr(root, "app_objs") and "Router" in getattr(root, "app_objs"):
            self.routes = getattr(root, "app_objs")["Router"].info
        else:
            self.routes = []

    def switch_view(self, url:str):
        for child in self.widget.winfo_children():
            child.destroy()

        for route in self.routes:
            if route["url"] == url:
                route["component"](self).render(fill = "both", expand = True)

    def render(self, **options):
        super().render(**options)

        default_comp:Component = None
        for route in self.routes:
            if route["url"] == "/":
                default_comp = route["component"](self)

        if default_comp is None and len(self.routes) > 0:
            default_comp = self.routes[0]["component"](self)

        if default_comp is not None:
            default_comp.render(fill = "both", expand = True)
            default_comp.root.render_children()
