from flask import Flask

app = Flask(__name__)

# 문제 1 — /ping 경로로 접속하면 "pong"을 반환하는 라우트를 작성해 봅시다.
@app.route('/ping')
def ping():
    return "pong"
# 문제 2 — /servers/<server_name> 형태로 서버 이름을 받아
# 상태 메시지를 반환하는 동적 라우트를 작성해 봅시다.

@app.route('/servers/<server_name>')
def servers(server_name):
    # 실무에서는 이 자리에 방화벽/서버 상태를 점검하는 로직이 들어갑니다
    return f"{server_name} 서버 상태를 조회합니다."

# [실행] python 파일
# [실행] flask app 파일명 run
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='172.30.1.55')
