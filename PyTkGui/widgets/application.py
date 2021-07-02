# -*- coding: utf-8 -*-
import os, sys, importlib, glob
from tkinter import Tk, PhotoImage
from typing import Dict, Any
from .. import __path__
from ..core.loader import load_ui
from ..objects import Component, GlobalStyle


class Application(Tk):
    app_objs:Dict[str, Any] = {}
    config:object = None

    def __init__(self, args:list, icon:str = None):
        super().__init__()

        self.icon = os.path.join(__path__[0], "assets", "icon.png") if icon is None else icon

        project_dir = os.path.dirname(os.path.abspath(args[0]))
        sys.path.append(project_dir)

        src_files = os.listdir(os.path.join(project_dir, "src"))
        if "config.py" in src_files:
            self.config = importlib.import_module(".config", "src")

    def use(self, obj):
        self.app_objs[obj.__class__.__name__] = obj

        return self

    def run(self, app_component:Component):
        if not getattr(app_component, "initialized"):
            app_component = app_component(self)

        GlobalStyle(self)
        app_component.render(fill = "both", expand = True)

        self.iconphoto(True, PhotoImage(file = self.icon))
        self.title(app_component.__class__.__name__)
        self.geometry("+0+0")
        self.mainloop()
