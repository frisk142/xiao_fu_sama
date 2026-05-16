import json
import sys
from config.paths import KEY_FILE
sys.stdout.reconfigure(encoding = "utf-8")

print(f"API密钥文件路径: {KEY_FILE}")

def save_api_key(key):
    with open(KEY_FILE, "w" , encoding= "utf-8") as f:
        json.dump({"ds_api_key" : key}, f)
    return "API 密钥已保存！小芙现在可以正常对话了"

    # 加载api密钥    
def load_api_key():
    try:
        with open(KEY_FILE, "r", encoding = "utf-8") as f:
            api_data = json.load(f)
            print(api_data.get("ds_api_key"))
            return api_data.get("ds_api_key")
    except FileNotFoundError:
        print("未找到api文件")
        return None