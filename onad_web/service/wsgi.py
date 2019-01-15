from flask import Flask, request, render_template

app = Flask(__name__)
import json
yapyap_data = "./static/storage/report_data/yapyap30_190105.json"  # 웹에 올릴 데이터 로드

with open(yapyap_data, 'r', encoding='utf-8') as fp:
    data = json.loads(fp.read())

cnt_viewer_per_10min = data['data']['cnt_viewer_per_10min']
print(cnt_viewer_per_10min)
@app.route('/', methods=['GET', 'POST'])
def home():
    import json
    yapyap_data = "./static/storage/report_data/yapyap30_190105.json"  # 웹에 올릴 데이터 로드

    with open(yapyap_data, 'r', encoding='utf-8') as fp:
        data = json.loads(fp.read())

    cnt_viewer_per_10min = data['data']['cnt_viewer_per_10min']
    print(cnt_viewer_per_10min)
    
    return render_template("home.html", data=data, mydata=cnt_viewer_per_10min)

app.run(debug=True)