import json
import os
from openai import OpenAI
from datetime import datetime
import re
import sys
sys.stdout.reconfigure(encoding = "utf-8")

# 配置主要信息,选择调用前面创建的系统变量
DEEPSEEK_API_KEY = os.environ.get("XIAO_FU_MEMORY")

BASE_URL = "https://api.deepseek.com/v1"

# 文件路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) # 定位至根目录

MEMORY_FILE = os.path.join(BASE_DIR, "xiao_fu_memory" ,"xiao_fu_memory.json") # 记忆文件位置

PROMPT_FILE = os.path.join(BASE_DIR, "prompt" , "prompt.json") # 配置文件保存
print(PROMPT_FILE)

client = OpenAI(api_key=DEEPSEEK_API_KEY,base_url=BASE_URL)

def load_all_conversations(): # 读取对话记录
    with open(MEMORY_FILE , encoding="UTF-8") as f:
        lines = f.readlines()
        conversations = [json.loads(line.strip()) for line in lines]
        return conversations
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
    print(f"[{datetime.now()}]开始生成用户画像")
    convs = load_all_conversations()
    if not(convs):
        print("没有对话记录")
    else:
        profile = generate_summary(convs)
        update_profile(profile)
        print(f"用户画像已保存至{PROMPT_FILE}")












