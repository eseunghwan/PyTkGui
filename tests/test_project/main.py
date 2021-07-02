# -*- coding: utf-8 -*-
import sys
from PyTkGui import Application
from App import App
from src.router import router

Application(sys.argv).use(router).run(App)
