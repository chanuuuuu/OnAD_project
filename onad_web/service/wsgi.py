from flask import Flask, render_template

'''
1. 컴퓨터이름 한글로 하면 유니코드 에러남 ㅠㅠ
2. 서버 충돌시
   netstat -o -a
   Taskkill/PID ### /F
'''
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("simson.html")

app.run(debug=True)