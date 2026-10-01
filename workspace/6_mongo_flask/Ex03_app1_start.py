from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> 보안 현황 보기</h1>"

@app.route('/health')
def health_check():
    # 실무에서는 이 자리에 방화벽/서버 상태를 점검하는 로직이 들어갑니다
    return {"status": "OK", "service": "security-dashboard"}

#개발할때만 씀, 실제론 없음
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='172.30.1.55')