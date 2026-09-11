import json
import subprocess
from pathlib import Path

def find_sd_cards():
    out = subprocess.check_output(["lsblk" , "-J" , "-o" , "NAME,TYPE,RM,FSTYPE,MOUNTPOINT,PATH"] , text=True)
    tree = json.loads(out)

    cards = []

    def walk(devices):
        for d in devices:
            rm = d.get("rm")
            fstype = d.get("fstype")
            mnt = d.get("mountpoint")
            if d.get("type") == "part" and rm and fstype and mnt:
                cards.append((d["path"] , mnt))
            walk(d.get("children" , []))

    walk(tree["blockdevices"])
    return cards

for dev , mnt in find_sd_cards():
    print(f"\nCard {dev} mounted at {mnt}")
    for p in Path(mnt).iterdir():
        print("   " , p.name)