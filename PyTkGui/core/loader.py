# -*- coding: utf-8 -*-
import os
from typing import Union
from .parser import parse_template, parse_style, parse_script
from ..static import view_code, comp_code

def load_ui(ui_file:str, ui_type:str = "view", save_to_file:bool = True, output_path:str = None) -> Union[str, None]:
    ui_file = os.path.abspath(ui_file)
    output_path = os.path.splitext(ui_file)[0] + ".py" if output_path is None else output_path
    ui_name = os.path.splitext(os.path.basename(ui_file))[0]
    if ui_name.lower() == ui_name:
        ui_name = ui_name.capitalize()

    with open(ui_file, "r", encoding = "utf-8") as uir:
        uit = uir.read()

        template = parse_template(uit.split("<template>")[1].split("</template>")[0].strip(), ui_type)

        if "<style>" in uit and "</style>" in uit:
            style = parse_style(uit.split("<style>")[1].split("</style>")[0].strip())
        else:
            style = ""

        if "<script>" in uit and "</script>" in uit:
            imports, data, method = parse_script(uit.split("<script>")[1].split("</script>")[0].strip())
        else:
            imports, data, method = "", "", ""

    base_code = view_code if ui_type == "view" else comp_code
    result_code = base_code.format(
        name = ui_name,
        template_code = template, style_code = style,
        import_code = imports,
        data_code = data,
        method_code = method
    )

    if save_to_file:
        with open(output_path, "w", encoding = "utf-8") as uiw:
            uiw.write(result_code)
    else:
        return result_code
