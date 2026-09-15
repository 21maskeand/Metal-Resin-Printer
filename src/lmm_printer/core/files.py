import json
import subprocess
from pathlib import Path
from lmm_printer.core.types import Result , State

def return_RM_Drives():
    out = subprocess.check_output(["lsblk" , "-J" , "-o" , "NAME,TYPE,RM,FSTYPE,MOUNTPOINT,PATH"] , text=True)
    tree = json.loads(out)

    drives = []

    def walk(devices):
        for d in devices:
            rm = d.get("rm")
            fstype = d.get("fstype")
            mnt = d.get("mountpoint")
            if d.get("type") == "part" and rm and fstype and mnt:
                drives.append((d["path"] , mnt))
            walk(d.get("children" , []))

    walk(tree["blockdevices"])

    if len(drives) == 0:
        drives = Result(value = None , state = State.ERROR , message = "No removable drives found.")
    else:
        drives = Result(value = drives , state = State.SUCCESS , message = "Found drives: " + ", ".join(mnt for dev , mnt in drives))
    return drives

def cli_Choose_File(drives):
    print("")
    print("Printable Files Found on Removable Drives: ")

    file_names = []
    file_mnts = []
    for dev , mnt in drives.value:
        root = Path(mnt)
        for file in root.iterdir():
            file_names.append(file.name)
            file_mnts.append(mnt)
            print(file_names[-1])
    
    print("")
    response = input("Choose file by entering name.extension or press enter to exit. ")

    if response.strip() == "":
        raise SystemExit(1)
    else:
        response = response.strip()
        if response in file_names:
            index = file_names.index(response)
            mnt = file_mnts[index]
            return Result(value = Path(mnt) / response , state = State.SUCCESS , message = "Successfully chose file: " + response + ", at mount: " + mnt + ".")
        else:
            print("File name invalid.")
            return cli_Choose_File(drives)

