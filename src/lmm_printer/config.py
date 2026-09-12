import yaml

def load_Config(path = "config/config.yaml"):
    with open(path , "r") as file:
        cnfg = yaml.safe_load(file)
    return cnfg