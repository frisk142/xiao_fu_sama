import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    base_dir = Path(sys._MEIPASS)
else:
    base_dir = Path(__file__).parent.parent


INDEX_FILE = str(base_dir / "Function" / "index.html")
PROMPT_FILE = str(base_dir / "prompt" / "prompt.json")
MEMORY_FILE = str(base_dir / "xiao_fu_memory" / "xiao_fu_memory.json")
KEY_FILE = str(base_dir / "config" / "api_key.json")
COUNT_FILE = str(base_dir / "config" / "COUNT_file")
DESKTOP_PET_FILE = str(base_dir / "Function" / "desktop_pet.py")
ICON = str(base_dir / "icon" / "xiaofu_sama.ico")
LOG = Path(base_dir)
