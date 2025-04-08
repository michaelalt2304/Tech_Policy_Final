import os
import shutil
#### ADDITIONAL INSTRUCTIONS HERE ####
# Add an "elif" statement  for your OS if necessary
# Inside of the system-dependent block below, specify some unique environment variable
# to your computer (see all by printing out os.environ) and add the specification below the try block
######################################

#### HOW TO ADD A PACKAGE ####
# ADD package and most recent version to requirements.txt in folder
# DELETE virtual in this repository, if it's there
# Run this file with Python again
##############################

while not os.path.exists(".config"):
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
        elif os.system(f"{place} test.py"):
            print("Malformed python executable. Please try again.")
            continue
    with open(".config", mode="w") as f:
        f.write(place)
        
with open(".config", mode="r") as f:
    PYTHON = f.readline()

VIRTUAL_FOLDER = "virtual"
CONFIRM = os.path.join(VIRTUAL_FOLDER, "initialized.txt")
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
    if current_system == "Windows_NT":
        if os.system(f"virtual\\Scripts\\activate.bat"):
            print(f"virtual\\Scripts\\activate.bat")
            # shutil.rmtree(VIRTUAL_FOLDER)
            print("Please run from cmd, not Powershell")
            exit(1)
    if current_system == "Darwin":
        if os.system(f"source {VIRTUAL_FOLDER}/bin/activate"):
            shutil.rmtree(VIRTUAL_FOLDER)
            print("An unknown error occurred. Please contact Michael")
            exit(1)
        

if not os.path.exists(CONFIRM):
    status = os.system(f"{VIRTUAL_PIP} install -r requirements.txt")
    with open(CONFIRM, 'a') as f:
        f.write("All initialized in terms of packages, etc, should run smoothly. If not contact mjstraus2304@gmail.com")
status = os.system(f"{VIRTUAL_PYTHON} -m streamlit run main.py")
