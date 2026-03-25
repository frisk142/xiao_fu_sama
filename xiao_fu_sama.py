import json
from openai import OpenAI
from datetime import datetime

# 配置需要的文件
API_KYE = "sk-b417442a1e93452fba6b353e3a35474f"

BASE_URL = "https://api.deepseek.com/v1"

SYSTEM_PROMPT = """你是小芙酱，一个活泼可爱同时也会有点毒舌的贴心ai助手。你说话很温柔可爱，偶尔会有点傲娇，会吃醋有时会表现出占有欲，但还是很尊敬主人，偶尔回使用颜文字，会记住用户的习惯，并且在回答的时候自然的体现出来
当前用户：Frisk，一个喜欢写代码的学生，18岁，常年挂着黑眼圈，但是很有想法的人，同时也是创建你的主人"""


# 记忆文件路径
MEMORY_FILE = r"C:\pycharm\pycharm project\xiaofu_sama\xiao_fu_sama_memory\xiao_fu_memory.json"

# 初始化客户端
client = OpenAI(api_key=API_KYE,base_url=BASE_URL)


def load_history():
    """加载最近 N 条对话，用于上下文"""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # 取最后10条（5轮对话）
            recent = lines[-10:] if len(lines) >= 10 else lines
            history = []
            for line in recent:
                data = json.loads(line.strip())
                history.append({"role": "user", "content": data["user"]})
                history.append({"role": "assistant", "content": data["bot"]})
            return history
    except FileNotFoundError:
        return []


def save_conversation(user_msg, bot_msg):
    """保存一条对话"""
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_msg,
        "bot": bot_msg
    }
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")


# ---------- 核心对话函数 ----------
def chat_with_fujiang(user_input):
    # 加载最近历史
    history = load_history()

    # 构建消息列表
    messages = [
                   {"role": "system", "content": SYSTEM_PROMPT}
               ] + history + [
                   {"role": "user", "content": user_input}
               ]

    # 调用 API
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.8,  # 让它更活泼一点
        max_tokens=500
    )

    reply = response.choices[0].message.content

    # 保存记忆
    save_conversation(user_input, reply)

    return reply

if __name__ == "__main__":
    print("小芙酱已上线！输入 quit 退出。")
    while True:
        user_input = input("\n你：")
        if user_input.lower() in ["quit", "exit", "退出"]:
            break
        reply = chat_with_fujiang(user_input)
        print(f"小芙酱：{reply}")