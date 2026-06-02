import json
import sys
from config.paths import KEY_FILE
import logging

log = logging.getLogger("XiaoFu")

def save_api_key(key):
    try:
        with open(KEY_FILE, "w" , encoding= "utf-8") as f:
            json.dump({"ds_api_key" : key}, f)
            log.info(f"api密钥保存成功,保存位置为{KEY_FILE}")
            return "api密钥保存成功"
    except IOError as e:
        log.error(f"保存api密钥时发生错误:{e}")
        return "保存api密钥时发生错误，请检查日志获取详细信息"

    # 加载api密钥    
def load_api_key():
    try:
        with open(KEY_FILE, "r", encoding = "utf-8") as f:
            api_data = json.load(f)
            log.debug("api密钥加载成功")
            return api_data.get("ds_api_key")
    except FileNotFoundError:
        log.warning("未能找到api文件，用户未绑定api密钥")
        return None