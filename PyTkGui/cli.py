"""Console script for PyTkGui."""
import os, sys
import zipfile, shutil, glob, subprocess
from .core.loader import load_ui
from . import __path__


def create_project(project_dir:str):
    project_dir = os.path.abspath(project_dir)
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
    
    with zipfile.ZipFile(os.path.join(__path__[0], "assets", "template.zip"), "r") as zip:
        zip.extractall(project_dir)

def build_project(build_dir:str) -> str:
    project_dir = os.getcwd()
    sys.path.append(project_dir)

    build_dir = os.path.abspath(build_dir)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    os.mkdir(build_dir)

    project_files = os.listdir(project_dir)
    if not "src" in project_files:
        raise RuntimeError("source directory must exists!")

    os.mkdir(os.path.join(build_dir, "src"))
    shutil.copyfile(os.path.join(project_dir, "src", "__init__.py"), os.path.join(build_dir, "src", "__init__.py"))

    shutil.copyfile(os.path.join(project_dir, "main.py"), os.path.join(build_dir, "main.py"))
    load_ui(os.path.join(project_dir, "App.ui"), output_path = os.path.join(build_dir, "App.py"))

    src_files = os.listdir(os.path.join(project_dir, "src"))
    if "assets" in src_files:
        shutil.copytree(os.path.join(project_dir, "src", "assets"), os.path.join(build_dir, "src", "assets"))

    if "components" in src_files:
        os.mkdir(os.path.join(build_dir, "src", "components"))
        os.chdir(os.path.join(build_dir, "src", "components"))
        for ui_file in glob.glob(os.path.join(project_dir, "src", "components", "*.ui")):
            ui_name = os.path.splitext(os.path.basename(ui_file))[0]
            load_ui(ui_file, "component", output_path = os.path.join(build_dir, "src", "components", f"{ui_name}.py"))

    if "router" in src_files:
        shutil.copytree(os.path.join(project_dir, "src", "router"), os.path.join(build_dir, "src", "router"))
    
    os.mkdir(os.path.join(build_dir, "src", "views"))
    os.chdir(os.path.join(build_dir, "src", "views"))
    for ui_file in glob.glob(os.path.join(project_dir, "src", "views", "*.ui")):
        ui_name = os.path.splitext(os.path.basename(ui_file))[0]
        load_ui(ui_file, output_path = os.path.join(build_dir, "src", "views", f"{ui_name}.py"))

    return build_dir

def run_project(build_dir:str):
    build_dir = build_project(build_dir)
    subprocess.run([sys.executable, os.path.join(build_dir, "main.py")], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)


def main():
    args = sys.argv[1:]

    if args in ([], ["run"]):
        return main(["help"])
    elif args[0] == "init":
        try:
            project_dir = args[1]
        except:
            project_dir = "./"

        create_project(project_dir)
    elif args[0] == "run":
        try:
            build_dir = args[2]
        except:
            build_dir = "./build"

        if args[1] == "dev":
            run_project(build_dir)
        elif args[1] == "build":
            build_project(build_dir)
        else:
            return main(["help"])
    elif args[0] == "help":
        print("""
Usage: PyTkGui [OPTIONS]

    PyTkGui cli service

Options:
    run dev [build_dir=./build]     build project and run
    run build [build_dir=./build]   build project to [build_dir]
    help                            Show this message and exit.
""")

    return 0
