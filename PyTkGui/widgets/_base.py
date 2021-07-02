# -*- coding: utf-8 -*-
import gc
from tkinter import ttk
from typing import List
from ..utils import get_real_master



class _Base:
    iter_num = 0

    def __init__(self, parent, **options):
        self.parent = parent
        self.options = options
        self.configures = {}
        self.pack_options = options.pop("pack", {})
        self.ptg_children:List[_Base] = []

        self.component = self.options.pop("component", None)

        self.has_iter = "iterator" in self.options.keys()
        self.seq = self.options.pop("sequence", None)
        self.iter = self.options.pop("iterator", None)
        self.ptg_iters = []

        self.append_method = self.options.pop("append_method", "append")
        self.insert_idx = self.options.pop("insert_idx", 0)

        if hasattr(self.parent, "iter_num"):
            if self.parent.has_iter:
                self.iter_num = self.parent.iter_num + 1
            else:
                self.iter_num = self.parent.iter_num
        else:
            self.iter_num = 0

        self.has_cond = "cond" in self.options.keys()
        self.cond = self.options.pop("cond", None)

        if options.pop("append_to_parent", True) and isinstance(self.parent, _Base):
            self.parent.ptg_children.append(self)

    def set_configure(self, opt_name:str, conf_name:str, default = None):
        self.configures[conf_name] = self.options.pop(opt_name, default)

    def render(self):
        if self.component is not None:
            for name in self.component.data:
                value = getattr(self.component, name)
                exec(f"global {name}; {name} = value")

        if self.has_iter and self.iter is not None:
            for widget in self.ptg_iters:
                widget.destroy()

            self.ptg_iters.clear()

            if self.parent.has_iter:
                _p_seq_idx = 0
                p_seqs = [ item.strip() for item in self.parent.seq.split(",") ]
                for _sequence in eval(self.parent.iter):
                    exec(f"global {self.parent.seq}; {self.parent.seq} = _sequence")

                    self.render_iters(
                        self.parent.ptg_iters[_p_seq_idx],
                        {
                            seq: eval(seq)
                            for seq in p_seqs
                        }
                    )
                    _p_seq_idx += 1
            else:
                self.render_iters()
        else:
            self.configure(**self.options)
            self.configure(**self.configures)

            if self.has_cond and not eval(self.cond):
                self.derender()

    def render_children(self):
        for child in self.ptg_children:
            child.render()
            child.render_children()

    def render_iters(self, parent = None, parent_seq:dict = {}):
        parent = self.parent if parent is None else parent

        insert_idx = self.destroy()

        if parent.has_iter:
            _p_seq_idx = 0
            p_seqs = [ item.strip() for item in self.parent.seq.split(",") ]
            for _sequence in eval(self.parent.iter):
                exec(f"global {self.parent.seq}; {self.parent.seq} = _sequence")

                self.render_iters(
                    self.parent.ptg_iters[_p_seq_idx],
                    {
                        seq: eval(seq)
                        for seq in p_seqs
                    }
                )
                _p_seq_idx += 1
        else:
            for key, value in parent_seq.items():
                exec(f"{key} = value")

            for _sequence in eval(self.iter):
                exec(f"{self.seq} = _sequence")
                
                options = { key: value for key, value in self.options.items() if not key in ("component", "iterator", "sequence") }
                options["append_to_parent"] = False

                for key, value in options.items():
                    if isinstance(value, str) and ("{" in value and "}" in value):
                        options[key] = eval('f"{}"'.format(value))

                if isinstance(self, Base):
                    options["insert_idx"] = insert_idx
                    options["append_method"] = "insert"
                    insert_idx += 1

                widget = self.__class__(parent, **options)
                self.ptg_iters.append(widget)
                widget.render(**self.pack_options)
                widget.render_children()

            exec(f"del {self.seq}")
            for key in parent_seq.keys():
                exec(f"del {key}")

        gc.collect()

    def configure(self, **options):
        pass

    def derender(self):
        pass

    def destroy(self) -> int:
        return 0

class Base(_Base):
    def __init__(self, tk_cls, parent, **options):
        options["append_to_parent"] = False

        super().__init__(parent, **options)

        self.tk_cls = tk_cls
        self.children:List[Base] = []

        if isinstance(self.parent, Base):
            if self.append_method == "append":
                self.parent.children.append(self)
            else:
                self.parent.children.insert(self.insert_idx, self)

        self.widget:ttk.Widget = self.tk_cls(get_real_master(self.parent))

    def configure(self, **options):
        self.widget.configure(**options)

    def update_configures(self, options:dict, extras:dict):
        self.options, self.configures = options, {}
        for opt_name, value in extras.items():
            if isinstance(value, list):
                conf_name, default = value
            else:
                conf_name, default = value, None

            self.set_configure(opt_name, conf_name, default)

        self.configure(**self.options)
        self.configure(**self.configures)

    def clear(self, destroy_me:bool = True):
        for child in self.children:
            child.clear()

        self.children.clear()

        if destroy_me:
            self.widget.destroy()

    def render(self, **render_options):
        if self.widget == None:
            self.widget = self.tk_cls(get_real_master(self.parent))

        self.widget.pack(**render_options)

        self.pack_options = self.widget.pack_info()
        self.pack_options.pop("in", None)

        super().render()

        return self.widget

    def render_children(self):
        super().render_children()

        for child in self.children:
            if not child.has_iter:
                child.derender()

            child.render(**child.pack_options)
            child.render_children()

    def derender(self):
        self.widget.pack_forget()

    def destroy(self) -> int:
        self.widget.destroy()
        insert_idx = self.parent.children.index(self)
        self.parent.children.remove(self)

        return insert_idx
