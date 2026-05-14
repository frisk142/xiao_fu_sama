import os

data_dir = os.path.dirname(os.path.dirname(__file__))

KEY_FILE = os.path.join(data_dir, "config","api_key.json")

COUNT_FILE = os.path.join(data_dir, "config", "COUNT_file")

PROMPT_FILE = os.path.join(data_dir, "prompt", "prompt.json")

MEMORY_FILE = os.path.join(data_dir, "xiao_fu_memory", "xiao_fu_memory.json")

INDEX_FILE = os.path.join(data_dir, "Function", "index.html")

DESKTOP_PET_FILE = os.path.join(data_dir, "Function", "desktop_pet.py")




