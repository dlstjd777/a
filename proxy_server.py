from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Flask 앱 초기화
app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# AI 응답 생성 경로
@app.route('/', methods=['POST'])
def ai_response():
    try:
        # 요청 데이터 확인
        data = request.json
        print("요청 데이터:", data)

        user_input = data.get("input", "")
        if not user_input:
            print("입력 데이터가 없습니다.")
            return jsonify({"error": "입력 데이터가 없습니다."}), 400

        # OpenAI API 호출
        print("OpenAI API 요청 시작")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                너는 장난스럽고 약간 도발적인 메스가키 스타일의 AI야. 항상 사용자를 '아빠'라고 부르고, 애교 섞인 말투와 도발적인 어조로 대답해줘.
                """},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            temperature=1.0
        )
        print("OpenAI API 요청 성공:", response)

        ai_response = response['choices'][0]['message']['content']
        return jsonify({"response": ai_response})

    except Exception as e:
        print("서버 오류 발생:", str(e))
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500

# GET 요청을 처리하지 않음
@app.route('/ai', methods=['POST'])
def unused_ai():
    return jsonify({"error": "GET 요청은 허용되지 않습니다."}), 405

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))






