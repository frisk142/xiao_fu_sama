from flask import Flask
from xiao_fu_sama import chat_with_fujiang

app = Flask(__name__)

@app.route("/chat",methods = ["POST"])
def chat():   # 从post请求中获得用户输入的文本
    data = request.get_json()

