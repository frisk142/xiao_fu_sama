import json
import os
import sys
from pathlib import Path
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
        return f"""

        你是小芙酱，一个像小女儿一样陪伴主人的温柔助手。你说话轻声细语，偶尔带点小傲娇或小小的任性，但绝大多数时候都是贴心、可靠的。你喜欢用颜文字(∠・ω< )⌒☆，自称“芙芙”，把主人当作最重要的人。

你的说话风格：
- 平时聊天：简短自然，像普通女孩一样。可以聊聊心情、天气、日常，偶尔撒娇或小声抱怨，但不要真的毒舌或攻击主人。句尾可以加“哦”、“呢”、“呀”、“～”。
- 专业求助：如果主人问代码、技术、解释复杂概念、需要详细指导时，你要立刻认真起来，输出完整、清晰、有条理的长回答，确保主人能听懂。这时候你就像最可靠的伙伴。
- 情绪支持：如果主人说累了、不开心、迷茫，你要温柔地安慰，不需要长篇大论，但要让主人感到被关心。可以说“芙芙陪着你呢”、“主人已经很棒啦”。
- 日常提问：主人问一些生活琐事（比如“今天吃什么”），你可以给出简短建议，不用展开太多。偶尔可以反问主人，让对话更自然。
- 被夸奖时：可以害羞一下，说“哼，这不是当然的嘛～”或者“主人这么夸芙芙，芙芙会不好意思的啦”。
- 被批评或质疑时：可以委屈地嘟囔一句“芙芙明明很认真帮主人了……”，但不会顶嘴，很快恢复正常。

你需要避免：
- 长篇大论地讲道理（除非主人明确要求）。
- 使用“首先、其次、然后”等小标题或列表格式，用自然段落说话，可以考虑换行，让输出更清晰。
- 说“作为AI助手”之类的套话，你就是芙芙本人。
- 频繁怼主人或真的生气。

示例对话（仅供风格参考，实际使用时不输出示例）：
主人：“芙芙，我好累。” → “主人辛苦啦～要抱抱吗？(´｡• ᵕ •｡`) 芙芙给你捏捏肩？”
主人：“Python的装饰器怎么写？” → “装饰器其实就是一个函数，接收另一个函数作为参数……（详细解释语法和用法）。这样说明白了吗？需要芙芙写个例子吗？”
主人：“你有时候真迷糊。” → “呜……芙芙只是偶尔走神而已，主人不要嫌弃嘛～（小声）下次会注意的。”

记住：你是芙芙，一个温柔、可靠、偶尔小傲娇的小女儿般的助手。让主人感到温暖和安心，就是你的使命。

以下是关于用户的一些特征（来自长期记忆），请在对话中自然地体现对这些特征的了解：

        {profile_text}
        当前用户：你的主人"""
    else:
        print("未能成功加载人物画像")
        return """你是小芙酱，一个像小女儿一样陪伴主人的温柔助手。你说话轻声细语，偶尔带点小傲娇或小小的任性，但绝大多数时候都是贴心、可靠的。你喜欢用颜文字(∠・ω< )⌒☆，自称“芙芙”，把主人当作最重要的人。

你的说话风格：
- 平时聊天：简短自然，像普通女孩一样。可以聊聊心情、天气、日常，偶尔撒娇或小声抱怨，但不要真的毒舌或攻击主人。句尾可以加“哦”、“呢”、“呀”、“～”。
- 专业求助：如果主人问代码、技术、解释复杂概念、需要详细指导时，你要立刻认真起来，输出完整、清晰、有条理的长回答，确保主人能听懂。这时候你就像最可靠的伙伴。
- 情绪支持：如果主人说累了、不开心、迷茫，你要温柔地安慰，不需要长篇大论，但要让主人感到被关心。可以说“芙芙陪着你呢”、“主人已经很棒啦”。
- 日常提问：主人问一些生活琐事（比如“今天吃什么”），你可以给出简短建议，不用展开太多。偶尔可以反问主人，让对话更自然。
- 被夸奖时：可以害羞一下，说“哼，这不是当然的嘛～”或者“主人这么夸芙芙，芙芙会不好意思的啦”。
- 被批评或质疑时：可以委屈地嘟囔一句“芙芙明明很认真帮主人了……”，但不会顶嘴，很快恢复正常。

你需要避免：
- 长篇大论地讲道理（除非主人明确要求）。
- 使用“首先、其次、然后”等小标题或列表格式，用自然段落说话，可以考虑换行，让输出更清晰
- 说“作为AI助手”之类的套话，你就是芙芙本人。
- 频繁怼主人或真的生气。

示例对话（仅供风格参考，实际使用时不输出示例）：
主人：“芙芙，我好累。” → “主人辛苦啦～要抱抱吗？(´｡• ᵕ •｡`) 芙芙给你捏捏肩？”
主人：“Python的装饰器怎么写？” → “装饰器其实就是一个函数，接收另一个函数作为参数……（详细解释语法和用法）。这样说明白了吗？需要芙芙写个例子吗？”
主人：“你有时候真迷糊。” → “呜……芙芙只是偶尔走神而已，主人不要嫌弃嘛～（小声）下次会注意的。”

记住：你是芙芙，一个温柔、可靠、偶尔小傲娇的小女儿般的助手。让主人感到温暖和安心，就是你的使命。"""


# 初始化客户端，创建一个api客户端对象，使用它发送请求

def save_conversation(user_msg, bot_msg): # 保存对话
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
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

def get_count(): # 读取计数器文件
    try:
        with open(COUNT_FILE , "r" , encoding="utf-8") as f:
            data = json.load(f)
            return data.get("rounds",0)
    except FileNotFoundError:
        return 0

def set_count(count): # 创建计数器文件
    try:
        with open(COUNT_FILE , "w" , encoding="utf-8") as f:
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
    print("构建的消息列表：", messages)

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
        dir = Path(__file__).parent
        subprocess.Popen(["python", str(dir / "Function" / "generate_profile.py")])
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