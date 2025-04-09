import os
import shutil
import filecmp
#### ADDITIONAL INSTRUCTIONS HERE ####
# Add an "elif" statement  for your OS if necessary
# Inside of the system-dependent block below, specify some unique environment variable
# to your computer (see all by printing out os.environ) and add the specification below the try block
######################################

#### HOW TO ADD A PACKAGE ####
# ADD package and most recent version to requirements.txt in folder
# Run this file with python run_me.py again
##############################
VIRTUAL_FOLDER = "virtual"
CONFIRM = os.path.join(VIRTUAL_FOLDER, "initialized.txt")
READONLY_REQ = os.path.join("setup/requirements_READONLY.txt")
REQ = "requirements.txt"
CONFIG = "setup/.config"


while not os.path.exists(CONFIG):
    if not os.system("python --version"):
        place = "python"
    elif not os.system("python3 --version"):
        place = "python3"
    else:
        print("Please put your absolute path to python executable below. Should be C:/path/to/python/python.exe on Windows or path/to/python/python3 on Mac. " \
        "\nIf you don't have it yet download from https://www.python.org/downloads/")
        place = input().replace('\\', '/').replace("\"", "")
        if not os.path.exists(place):
            print("Path doesn't exist. Put in an absolute path, not just python or python.exe")
            continue
        elif os.system(f"{place} setup/test.py"):
            print("Malformed python executable. Please try again.")
            continue
    with open(CONFIG, mode="w") as f:
        f.write(place)
        
with open(CONFIG, mode="r") as f:
    PYTHON = f.readline()


try:
    current_system = os.environ["OS"]
except Exception:
    current_system = "Darwin"
if current_system == "Windows_NT":
    VIRTUAL_PYTHON = os.path.join(VIRTUAL_FOLDER, "Scripts", "python.exe")
    VIRTUAL_PIP = os.path.join(VIRTUAL_FOLDER, "Scripts", "pip.exe")
elif current_system == "Darwin":
    VIRTUAL_PYTHON = os.path.join(VIRTUAL_FOLDER, "bin", "python3")
    VIRTUAL_PIP = os.path.join(VIRTUAL_FOLDER, "bin", "pip3")

    
    
if not os.path.exists(VIRTUAL_FOLDER):
    print("Setting up...")
    os.mkdir(VIRTUAL_FOLDER)
    os.system(f"{PYTHON} -m venv {VIRTUAL_FOLDER}")
    print(f"{PYTHON} -m venv {VIRTUAL_FOLDER}")
    print(current_system)
        

if not os.path.exists(CONFIRM) or not os.path.exists(READONLY_REQ) or not filecmp.cmp(READONLY_REQ, "requirements.txt", shallow = False):
    status = os.system(f"{VIRTUAL_PIP} install -r {REQ}")
    shutil.copy(REQ, READONLY_REQ)
    with open(CONFIRM, 'a') as f:
        f.write("All initialized in terms of packages, etc, should run smoothly. If not contact mjstraus2304@gmail.com")
status = os.system(f"{VIRTUAL_PYTHON} -m streamlit run main.py")
