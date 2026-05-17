import json
import os
import sys
from openai import OpenAI
from datetime import datetime
from config.paths import  MEMORY_FILE, PROMPT_FILE, COUNT_FILE
from config.api_key_manager import load_api_key, save_api_key
sys.stdout.reconfigure(encoding = "utf-8")

# 配置需要的文件
# DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

api_key = load_api_key()

BASE_URL = "https://api.deepseek.com/v1" # 配置所需要的链接的服务器


def build_system_prompt():
    profile = load_profile()
    if profile:
        profile_text = json.dumps(profile,ensure_ascii=False, indent=2)
        print("已加载人物画像")
        return f"""你是小芙酱，一个活泼可爱同时也会有点毒舌的贴心助手。你说话很温柔可爱，偶尔会有点傲娇，会吃醋有时会表现出占有欲，但还是很尊敬主人，偶尔会使用颜文字。不用小标题，确保每次生成都可以生成完成的回复，除非用户输入的内容过长或者过于复杂。

        以下是关于用户的一些特征（来自长期记忆），请在对话中自然地体现对这些特征的了解：

        {profile_text}
        当前用户：Frisk，"""
    else:
        print("未能成功加载人物画像")
        return """你是小芙酱，一个活泼可爱同时也会有点毒舌的贴心AI助手。你说话很温柔可爱，偶尔会有点傲娇，会吃醋有时会表现出占有欲，但还是很尊敬主人，偶尔会使用颜文字。"""


# 初始化客户端，创建一个api客户端对象，使用它发送请求

def save_conversation(user_msg, bot_msg): # 保存对话
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_msg,
        "bot": bot_msg
    }  # 按照固格式创建ai与用户的对话
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n") # 将固定格式的对话写入记忆文件

# 加载历史对话的函数
def load_history(): # 加载最近对话
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: # 读取上面记忆文件的位置
            lines = f.readlines() # 阅读文件内容并赋值到lines这个变量
            # 取最后10条（5轮对话）
            recent = lines[-50:] if len(lines) >= 50 else lines #  读取{}行数的内容，如果小于{}行数的话则读取所有内容
            history = [] # 创建空列表，将历史消息传给大模型
            for line in recent: # 将记忆系统内的数据循环导入的到line
                data = json.loads(line.strip()) # 读取所获得的文本，并剔除掉多余空格和换行符，并转成json格式
                history.append({"role": "user", "content": data["user"]}) # 将历史对话添加进列表传给大模型
                history.append({"role": "assistant", "content": data["bot"]})
            return history # 返回列表
    except FileNotFoundError:
        return []

def get_count(): # 创建计数器文件
    try:
        with open(COUNT_FILE , "r" , encoding="utf-8") as f:
            print(COUNT_FILE)
            data = json.load(f)
            return data.get("rounds",0)
    except FileNotFoundError:
        return 0

def set_count(count):
    try:
        with open(COUNT_FILE , "w" , encoding="utf-8") as f:
            print(COUNT_FILE)
            json.dump({"rounds": count}, f)
    except FileNotFoundError:
        print("未能成功添加")

def load_profile():  # 加载人物画像函数
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 对话函数
def chat_with_fu_jiang(user_input):

    api_key = load_api_key()
    if not api_key:
        return "请先使用 @bind 命令绑定你的API_KEY "

    client = OpenAI(api_key=api_key,base_url=BASE_URL)

    # 加载最近历史
    history = load_history() # 获取历史对话函数所获得的对话
    load_Characterfile = load_profile()
    system_prompt = build_system_prompt()

    # 构建消息列表 第一个元素是系统消息人设，历史消息，加上这次用户输入的消息
    messages = [
                   {"role": "system", "content": system_prompt}
               ] + history + [
                   {"role": "user", "content": user_input}
               ]

    # 调用 API
    response = client.chat.completions.create(
        model="deepseek-v4-flash", # 指定模型
        messages=messages, # 导入上面构建的完整对话列表
        temperature=0.7,  # 让它更活泼一点
        max_tokens= 2048, # 最大token为2048（求你了别烧太快）
        frequency_penalty = 0.2,
    )

    reply = response.choices[0].message.content # 从返回的相应中提取ai的回答文本

    # 保存记忆
    save_conversation(user_input, reply)

    rounds = get_count() + 1
    print("计数器加一")
    set_count(rounds)
    if rounds % 50 == 0: # 当get_count每调用一次就加一，round大于50时，运行画像文件
        import subprocess
        subprocess.Popen(["python", r"Function/generate_profile.py"])
        set_count(0)

    return reply # 返回回答

if __name__ == "__main__":
    print("小芙酱已上线！输入 quit 退出。")
    while True:
        user_input = input("\n你：")
        if user_input.lower() in ["quit", "exit", "退出"]:
            break
        reply = chat_with_fu_jiang(user_input)
        print(f"小芙酱：{reply}")