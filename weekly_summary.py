import json
import os
from openai import OpenAI
from datetime import datetime

# 配置主要信息
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

BASE_URL = "https://api.deepseek.com/v1"

# 文件路径
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json") # 记忆文件位置

PROMPT_FILE = os.path.join(os.path.dirname(__file__), "prompt.json") # 配置文件保存

client = OpenAI(api_key=API_KYE,base_url=BASE_URL)

def load_all_conversations(): # 读取对话记录
    with open(MEMORY_FILE) as f:
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

    请只输出JSON，不要其他解释。

    对话记录：
    {text_for_summary}
    """

    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [{"role":"user","content":prompt}],
        timeout = 0.5,
        max_tokens = 300,
    )
    summer_text = response.choices[0].message.content

    # 清理可能的markdown标记
    if "```json" in summer_text:
        summer_text = summer_text.split("```json")[1].strip("```")[0]
    elif "```" in summer_text:
        summer_text = summer_text.split("```")[1].strip("```")[0]

    try:
        profile = json.loads(summer_text)
    except json.JSONDecodeError:
        print("解析JSON失败，原始内容：",summer_text)
        profile = {"error":"解析失败","raw":summer_text}
    return profile

def save_profile(profile):
    with open (PROMPT_FILE, "w",encoding = "utf-8") as f:
        json.dump(profile,f,ensure_ascii = False,indent = 2)

if __name__ == "__main__":
    print(f"[{datetime.now()}]开始生成用户画像")
    convs = load_all_conversations()
    if not(convs):
        print("没有对话记录")
    else:
        profile = generate_summary(convs)
        save_profile(profile)
        print(f"用户画像已保存至{PROMPT_FILE}")












