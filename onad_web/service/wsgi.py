from flask import Flask, render_template

'''
<<구동 파일>>

error
1. 컴퓨터이름 한글로 하면 유니코드 에러남 ㅠㅠ
2. 서버 충돌시
   netstat -o -a
   Taskkill/PID ### /F
'''

app = Flask(__name__)


@app.route('/simson', methods=['GET', 'POST'])
def simson():
    return render_template("simson.html")

if __name__=='__main__':
    app.run(debug=True)