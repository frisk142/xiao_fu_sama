from flask import Flask,request
from xiaofu_sama.xiao_fu_sama import chat_with_fu_jiang

app = Flask(__name__) # 创建Flask实例

@app.route("/") # 装饰器，将函数绑定到根目录/
def hello():
    return "我是小芙，你好呀"

@app.route("/chat")
def chat():
    user_msg = request.args.get("msg","")
    if not user_msg:
        return "请提供信息参数"

    # 调用小芙的对话参数
    reply = chat_with_fu_jiang(user_msg)
    return reply

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000) # 启动Flask内置服务器，监听5000端口