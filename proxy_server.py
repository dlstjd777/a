from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os  # os 모듈 임포트!

app = Flask(__name__)
CORS(app)  # 모든 출처에서의 요청 허용

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")  # os.getenv로 환경 변수 읽기

# 기본 경로 확인용
@app.route('/')
def home():
    return "구름이 AI 서버가 실행 중이에요♥", 200

# /ai 경로: 로블록스 요청 처리
@app.route('/ai', methods=['POST'])
def ai_response():
    try:
        data = request.json
        user_input = data.get("input", "")

        # 입력 데이터가 없으면 오류 반환
        if not user_input:
            return jsonify({"error": "입력 데이터가 없습니다."}), 400

        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                너는 장난스럽고 약간 도발적인 메스가키 스타일의 AI야. 항상 사용자를 "아빠"라고 부르고, 애교 섞인 말투와 도발적인 어조로 대답해줘.
                """},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            temperature=1.0
        )

        # 응답 생성
        ai_response = response['choices'][0]['message']['content']
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)





