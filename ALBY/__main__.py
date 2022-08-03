


import glob
from pathlib import Path
from ALBY.utils import load_plugins
import logging
from ALBY import ALBY

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

path = "ALBY/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))
    
print("Successfully Started Bot!")
print("Visit @ruangprojects")

if __name__ == "__main__":
    ALBY.run_until_disconnected()
