# -*- coding: utf-8 -*-
from PyTkGui import Router
from src.views.index import Index
from src.views.widgets import Widgets

router = Router([
    {
        "url": "/",
        "component": Index
    },
    {
        "url": "/Widgets",
        "component": Widgets
    }
])
