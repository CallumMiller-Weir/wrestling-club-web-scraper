import json
import os
import platform
import subprocess

def dump_json_to_file(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data saved to '{file_name}'")

def open_file_in_editor(file_name):
    current_os = platform.system()
    if current_os == "Windows":
        subprocess.run(["start", file_name], shell=True)
    elif current_os == "Linux":
        subprocess.run(["xdg-open", file_name])
    else:
        print(f"Unsupported OS: {current_os}")