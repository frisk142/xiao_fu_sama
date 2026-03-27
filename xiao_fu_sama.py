import json
import os
from openai import OpenAI
from datetime import datetime

PROMPT_FILE = os.path.join(os.path.dirname(__file__), "profile.json")

# 配置需要的文件
API_KYE = "sk-b417442a1e93452fba6b353e3a35474f" # 配置所需要的语言模型api密钥

BASE_URL = "https://api.deepseek.com/v1" # 配置所需要的链接的服务器

def build_system_prompt():
    profile = load_profile()
    if profile:
        pro

# 记忆文件路径
MEMORY_FILE = r"C:\pycharm\pycharm project\xiaofu_sama\xiao_fu_sama_memory\xiao_fu_memory.json"

# 初始化客户端，创建一个api客户端对象，使用它发送请求
client = OpenAI(api_key=API_KYE,base_url=BASE_URL)

def save_conversation(user_msg, bot_msg):
    """保存一条对话"""
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_msg,
        "bot": bot_msg
    }  # 按照固格式创建ai与用户的对话
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n") # 将固定格式的对话写入记忆文件

# 加载历史对话的函数
def load_history():
    """加载最近 N 条对话，用于上下文"""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f: # 读取上面记忆文件的位置
            lines = f.readlines() # 阅读文件内容并赋值到lines这个变量
            # 取最后10条（5轮对话）
            recent = lines[-100:] if len(lines) >= 100 else lines #  读取{}行数的内容，如果小于{}行数的话则读取所有内容
            history = [] # 创建空列表，将历史消息传给大模型
            for line in recent: # 将记忆系统内的数据循环导入的到line
                data = json.loads(line.strip()) # 读取所获得的文本，并剔除掉多余空格和换行符，并转成json格式
                history.append({"role": "user", "content": data["user"]}) # 将历史对话添加进列表传给大模型
                history.append({"role": "assistant", "content": data["bot"]})
            return history # 返回列表
    except FileNotFoundError:
        return []

def load_profile():  # 加载人物画像函数
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 对话函数
def chat_with_fujiang(user_input):
    # 加载最近历史
    history = load_history() # 获取历史对话函数所获得的对话

    # 构建消息列表 第一个元素是系统消息人设，历史消息，加上这次用户输入的消息
    messages = [
                   {"role": "system", "content": SYSTEM_PROMPT}
               ] + history + [
                   {"role": "user", "content": user_input}
               ]

    # 调用 API
    response = client.chat.completions.create(
        model="deepseek-chat", # 指定模型
        messages=messages, # 导入上面构建的完整对话列表
        temperature=0.8,  # 让它更活泼一点
        max_tokens=500 # 最大token为500（求你了别烧太快）
    )

    reply = response.choices[0].message.content # 从返回的相应中提取ai的回答文本

    # 保存记忆
    save_conversation(user_input, reply)

    return reply # 返回回答

if __name__ == "__main__":
    print("小芙酱已上线！输入 quit 退出。")
    while True:
        user_input = input("\n你：")
        if user_input.lower() in ["quit", "exit", "退出"]:
            break
        reply = chat_with_fujiang(user_input)
        print(f"小芙酱：{reply}")