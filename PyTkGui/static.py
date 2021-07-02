# -*- coding: utf-8 -*-

view_code = """# -*- coding: utf-8 -*-
from PyTkGui.widgets import *
from PyTkGui import Component, ComponentStyle, Variable, Eventer
{import_code}

class {name}(Component):
    def __init__(self, master, **comp_options):
        super().__init__(master)
{data_code}{style_code}{template_code}{method_code}"""

comp_code = """# -*- coding: utf-8 -*-
from PyTkGui.widgets import *
from PyTkGui import Component, ComponentStyle, Variable, Eventer
{import_code}

class {name}(Component):
    def __init__(self, master, **comp_options):
        super().__init__(master)
{data_code}{style_code}{template_code}{method_code}"""
