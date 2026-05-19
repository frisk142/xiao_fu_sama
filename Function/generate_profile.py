import json
import os
import re
import sys
from openai import OpenAI
from datetime import datetime
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config.paths import  MEMORY_FILE, PROMPT_FILE
from config.api_key_manager import load_api_key
sys.stdout.reconfigure(encoding = "utf-8")



# 配置主要信息,选择调用前面创建的系统变量


BASE_URL = "https://api.deepseek.com/v1"

# 文件路径

api_key = load_api_key()
print(api_key)

client = OpenAI(api_key=api_key,base_url=BASE_URL)

def init_file():
    os.makedirs(os.path.dirname(PROMPT_FILE), exist_ok=True)
    if not os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE , "w" , encoding="utf-8") as f:
            json.dump({}, f)


    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE , "w" , encoding="utf-8") as f:
            pass



def load_all_conversations(): # 读取对话记录
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE , encoding="UTF-8") as f:
        return  [json.loads(line.strip()) for line in f]
    
def generate_summary(conversations):
    if not conversations :
        return {}
    recent =  conversations[-200:]

    # 将对话整理成文本
    text_for_summary = "\n".join([f"用户：{c['user']}\n小芙：{c['bot']}" for c in recent])

    prompt = f"""
    你是一个专业的数据分析师。下面是用户和AI助手“小芙酱”的对话记录，请从中提取用户的个人特征，用JSON格式输出，字段如下（可适当增减）：
    - name: 用户的名字（从对话中推断）
    - age: 年龄（推断）
    - occupation: 职业/身份
    - habits: 作息习惯、饮食偏好等
    - coding_style: 编程习惯（如常用变量名、喜欢用的库等）
    - speech_patterns: 口头禅、常用语气
    - interests: 兴趣爱好
    - dislikes: 讨厌的事物
    - important_dates: 重要日期（如果有）
    - personality: 性格特征（从对话中感知）

    请只输出JSON，不要其他解释。尽可能的详细
    必须闭合完整可直接json.loads解析

    对话记录：
    {text_for_summary}
    """

    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [{"role":"user","content":prompt}],
        timeout = 60,
        max_tokens = 8192,
    )
    summer_text = response.choices[0].message.content
    print(summer_text)

    summer_text = re.sub(r'^```json\s*', '', summer_text)
    summer_text = re.sub(r'\s*```$', '', summer_text)
    summer_text = summer_text.strip()

    try:
        profile = json.loads(summer_text)
    except json.JSONDecodeError:
        print("解析JSON失败，原始内容：",summer_text)
        profile = {"error":"解析失败","raw":summer_text}
    return profile

def update_profile(new_profile):
    # 加载目前的画像
    old_profile = {}
    try:
        with open(PROMPT_FILE , "r" ,encoding="utf-8") as f:
            old_profile = json.load(f)
    except FileNotFoundError:
        pass

    # 合并新旧画像
    merged = old_profile.copy()
    for key , value in new_profile.items():
        if key in merged:
            if isinstance(merged[key],list) and isinstance(value,list):
                merged[key] = list(set(merged[key] + value))
            elif isinstance(merged[key],str) and isinstance(value,str):
                if value not in merged[key]:
                    merged[key] = merged[key] + "`" + value
                else:
                    merged[key] = value
            else:
                merged[key] = value

    with open(PROMPT_FILE , "w" , encoding="utf-8") as f:
        json.dump(merged , f, ensure_ascii = False, indent = 2)




if __name__ == "__main__":
    init_file()
    print(f"[{datetime.now()}]开始生成用户画像")
    convs = load_all_conversations()
    if not(convs):
        print("没有对话记录")
    else:
        profile = generate_summary(convs)
        update_profile(profile)
        print(f"用户画像已保存至{PROMPT_FILE}")












