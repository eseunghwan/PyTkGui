# -*- coding: utf-8 -*-
from copy import deepcopy
from ._base import Base
from ..objects import Component
from tkinter import Frame


class If(Base):
    def __init__(self, master, cond:str, component:Component):
        super().__init__(Frame, master)

        self.cond, self.component = cond, component

    def render(self, **options):
        for child in self.children:
            if child.pack_options["expand"] == True:
                options["expand"] = True
                break

        super().render(**options)

        for name in self.component.data:
            value = getattr(self.component, name)
            exec(f"global {name}; {name} = value")

        if not eval(self.cond):
            self.widget.pack_forget()

    def render_children(self):
        for child in self.children:
            options = child.pack_options
            options["fill"] = self.pack_options["fill"]

            child.derender()
            child.render(**options)

class For(Base):
    def __init__(self, master, iter:str, component:Component):
        super().__init__(Frame, master)

        self.iter, self.component = iter, component
        self.is_first_render = True

    def render(self, **options):
        if self.is_first_render:
            self.is_first_render = False
            for child in self.children:
                child.destroy()

        for child in self.children:
            if child.pack_options["expand"] == True:
                options["expand"] = True
                break

        super().render(**options)

        for name in self.component.data:
            value = getattr(self.component, name)
            exec(f"global {name}; {name} = value")

        exec(f"""
for {self.iter}:
    self.render_children()
""")

    def render_children(self):
        for child in self.children:
            options = deepcopy(child.options)
            options.update(child.configures)
            exec(f"{child.__class__.__name__}(self, **{options})")
