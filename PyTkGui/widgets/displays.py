# -*- coding: utf-8 -*-
import os
from tkinter import ttk
from PIL import Image as PILImage, ImageTk as PILImageTk
from ._base import Base


class Label(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Label, master, **options)

        self.set_configure("variable", "textvariable")

        if self.configures["textvariable"] is not None:
            self.options.pop("text", None)
        else:
            self.configures.pop("textvariable")

class Image(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Label, master, **options)

        self.source = os.path.abspath(self.options.pop("source"))
        self.img_size = ( self.options.pop("width", None), self.options.pop("height", None) )

    def render(self, **options):
        super().render(**options)

        if self.source is not None:
            size = ( self.winfo_reqwidth() if self.img_size[0] is None else self.img_size[0], self.winfo_reqheight() if self.img_size[1] is None else self.img_size[1] )
            image = PILImage.open(self.source).resize(size, PILImage.ANTIALIAS)
            self.image = PILImageTk.PhotoImage(image)
            self.configure(image = self.image)

class ProgressBar(Base):
    def __init__(self, master, **options):
        super().__init__(ttk.Progressbar, master, **options)

        self.set_configure("variable", "variable")
        self.set_configure("orient", "orient", "horizontal")
        self.set_configure("mode", "mode", "determinate")
        self.set_configure("maximum", "maximum", 100)
        self.set_configure("value", "value", 0)

        if self.configures["variable"] is not None:
            self.options.pop("value", None)
        else:
            self.configures.pop("variable")

class Separator(Base):
    def __init__(self, master, orient:str = "horizontal", **options):
        super().__init__(ttk.Separator, master, **options)

        self.options["orient"] = orient
