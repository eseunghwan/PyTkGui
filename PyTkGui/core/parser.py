# -*- coding: utf-8 -*-
import os, random
from lxml import html as ET
from typing import Tuple, Dict, Any
from types import FunctionType, BuiltinFunctionType, MethodType


class Component:
    def __init__(self):
        attrib = {
            key: value
            for key, value in self.__class__.__dict__.items()
            if not key.startswith("__") and not key.endswith("__")
        }

        self.datas, self.methods = {}, []
        for key, value in attrib.items():
            if isinstance(value, (FunctionType, BuiltinFunctionType, MethodType)):
                self.methods.append(key)
            else:
                self.datas[key] = value

        del attrib


def parse_element_option(option:dict) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any]]:
    options, extras, pack_info = {}, {}, {}
    for key, value in option.items():
        try:
            value = eval(value.strip())
        except:
            value = value.strip()

        if key.startswith("pack."):
            pack_info[key[5:]] = value
        elif key == "command":
            extras["command"] = f"Eventer(self, \"{value}\")"
        elif key == "if":
            extras["cond"] = f"\"{value}\""
            extras["component"] = "self"
        elif key == "for":
            extras["sequence"], extras["iterator"] = [ f'"{item.strip()}"' for item in value.split("in") ]
            extras["component"] = "self"
        else:
            if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                options["variable"] = f"self.{value[1:-1]}_var"
            elif isinstance(value, str):
                options[key] = f'"{value}"'
            else:
                options[key] = value

    return options, extras, pack_info

def parse_element(element:ET.Element, master:str, tab_size:int = 2) -> str:
    if isinstance(element, ET.HtmlComment):
        return ""

    name:str = element.tag
    if "_" in name:
        spliteds = name.split("_")
        name = "_".join([ item.upper() for item in spliteds[:-1] ] + [ spliteds[-1].capitalize() ])
    else:
        name = name.capitalize()\
        .replace("Routerlink", "RouterLink").replace("Routerview", "RouterView")\
        .replace("Tableheader", "TableHeader").replace("Tablecolumn", "TableColumn").replace("Tablebody", "TableBody").replace("Tablerow", "TableRow").replace("Tableitem", "TableItem")\
        .replace("layout", "Layout")\
        .replace("box", "Box")\
        .replace("bar", "Bar")\
        .replace("button", "Button")\
        .replace("item", "Item")

    options = { key.lower(): value for key, value in element.attrib.items() }
    widget_id = options.pop("id", f"{name}_{random.randint(100, 999)}")

    tabs = "    " * 2
    template_code, pack_options = "", None
    
    if not master in ("self"):
        master = "self." + master

    for key, value in options.items():
        if isinstance(value, str):
            if os.path.isfile(value) or os.path.isdir(value):
                options[key] = os.path.abspath(value)

    options, extras, pack_options = parse_element_option(options)

    option_text = ", ".join([ f"{key} = {value}" for key, value in options.items() ])
    if not options == {}:
        option_text = ", " + option_text

    if not extras == {}:
        option_text += ", " + ", ".join([ f"{key} = {value}" for key, value in extras.items() ])

    if widget_id == "root":
        option_text += ", pack = comp_options.pop(\"pack\", {}), **comp_options"
    else:
        option_text += f", pack = {pack_options}"

    if name == "RouterLink":
        template_code += f"{tabs}self.{widget_id} = RouterLink({master}, self{option_text})\n"
    elif name == "RouterView":
        template_code += f"{tabs}self.router_view = RouterView({master}, self.master)\n"
        widget_id = "router_view"
        pack_options = { "fill": "both", "expand": True }
    elif name == "Slot":
        template_code += f"{tabs}self.slot = Slot({master})\n"
        widget_id = "slot"
        pack_options = { "fill": "both", "expand": True }
    elif name in ("If", "For"):
        template_code += f"{tabs}self.{widget_id} = {name}({master}{option_text}, component = self)\n"
    else:
        if name == "GroupBox" and not "text" in options.keys():
            options["text"] = options.pop("title", "")

        template_code += f"{tabs}self.{widget_id} = {name}({master}{option_text})\n"

    for child in element.getchildren():
        template_code += parse_element(child, widget_id, tab_size)

    return template_code

def parse_template(template:str, ui_type:str):
    root = ET.fromstring(template)

    root.attrib["Id"] = "root"
    root.attrib["Pack.Fill"] = "both"
    root.attrib["Pack.Expand"] = "True"

    return "\n        # template\n" + parse_element(root, "master")

def parse_style(style:str) -> str:
    if style == "":
        return ""

    styles = [ (item + "}").strip() for item in style.split("}") if not item.strip() == "" ]

    configures, maps = {}, {}
    for item in styles:
        style_name = item.split("\n")[0][:-1].strip()

        options = {}
        for line in item.split("\n")[1:-1]:
            key, value = line[:-1].strip().split(":")
            try:
                options[key.strip()] = eval(value.strip())
            except:
                options[key.strip()] = value.strip()

        if ":" in style_name:
            style_name, style_state = style_name.split(":")

            if not style_name in maps.keys():
                maps[style_name] = {}

            for key, value in options.items():
                if not key in maps[style_name].keys():
                    maps[style_name][key] = []

                maps[style_name][key].append((style_state, value))
        else:
            configures[style_name] = options

    configure_code = "\n".join(
        [
            f"""        style.configure("{key}", **{value})"""
            for key, value in configures.items()
        ]
    )
    map_code = "\n".join(
        [
            f"""        style.map("{key}", **{value})"""
            for key, value in maps.items()
        ]
    )

    return f"""
        # style
        style = ComponentStyle(self.master)
{configure_code}
{map_code}
        """

def parse_script(script:str) -> Tuple[str, str, str]:
    if script == "":
        return ""

    imports = [
        line.strip()
        for line in script.split("\n")
        if line.startswith("import") or (line.startswith("from") and "import" in line)
    ]
    for idx, line in enumerate(imports):
        script = script.replace(line, "").strip()

        if line.startswith("from ..views"):
            name = line.split("import")[1].strip()
            imports[idx] = "from ..views" + f".{name} import {name}"
        elif line.startswith("from ..components"):
            name = line.split("import")[1].strip()
            imports[idx] = "from ..components" + f".{name} import {name}"

    scripts = script.split("\n")
    cls_name = scripts[0][6:-12].strip()
    exec(script)
    obj = eval(cls_name)()

    data = []
    for key, value in obj.datas.items():
        if isinstance(value, str):
            data.append(f"""        Variable(self, master, "{key}", "{value}")""")
        else:
            data.append(f"""        Variable(self, master, "{key}", {value})""")

    method = []
    for key in obj.methods:
        method_code, method_idx, tab_size = "", 0, 0
        for idx, line in enumerate(scripts):
            if line.strip().startswith(f"def {key}"):
                method_code += line
                method_idx = idx + 1
                tab_size = len(line.replace(line.strip(), ""))
                break

        for line in scripts[method_idx:]:
            if line[tab_size:] == line.strip():
                break

            method_code += "\n" + line

        method.append(method_code + "\n")

    return "\n".join(imports) + "\n", "\n        # data\n" + "\n".join(data) + "\n", "\n    # methods\n" + "\n".join(method) + "\n"
