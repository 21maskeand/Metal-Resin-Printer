import json , os , tempfile
from dataclasses import fields , asdict
import subprocess
from pathlib import Path
from lmm_printer.core.types import Result , State , Printer_State

def return_RM_Drives():
    """
    Searches for and returns a result variable with the result of the process.

    Returns:
        Result: A dataclass decribing the outcomes with fields:
            value: The 
    """
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

def get_Files(drives):
    file_names = []
    file_mnts = []
    for dev , mnt in drives:
        root = Path(mnt)
        for file in root.iterdir():
            file_names.append(file.name)
            file_mnts.append(mnt)

    return file_names , file_mnts

def save_Dict(path , data):
    d = os.path.dirname(path)
    fd , temp = tempfile.mkstemp(dir = d)
    try:
        with os.fdopen(fd , "w") as f:
            json.dump(data , f)
        os.replace(temp , path)
    except Exception:
        os.unlink(temp)
        raise

def load_Dict(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        raise

def save_Printer_State(path , data):
    save_Dict(path , asdict(data))

def load_Printer_State(path):
    if not path.exists():
        state = Printer_State()
        save_Printer_State(path , state)
        return state
    state_dict = load_Dict(path)
    known = {f.name for f in fields(Printer_State)}
    return Printer_State(**{k: v for k , v in state_dict.items() if k in known})
