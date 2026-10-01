# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    alerts = [
        "[High] 방화벽 정책 위반 탐지 - 10.0.0.5",
        "[Medium] 반복 로그인 실패 - 203.0.113.55",
    ]
    return render_template('index3.html', alerts=alerts)

@app.route("/check")
def check():
    blocked_ips = ["172.15.22.124", "5.5.5.5", "128.1.1.1"]
    server_name = "Bastion-01"
    return render_template('index2.html'
                           , blocked_ips=blocked_ips
                           , server_name=server_name)

if __name__ == "__main__":
    app.run(debug=True)