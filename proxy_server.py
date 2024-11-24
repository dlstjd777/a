from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "구름이 AI 서버가 실행 중이에요♥", 200

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    # 빈 응답을 반환하거나 실제 favicon.ico 파일 경로를 설정
    return jsonify({"message": "No favicon available"}), 204

@app.route('/ai', methods=['POST'])
def ai_response():
    try:
        # 요청 데이터 확인
        data = request.json
        print("요청 데이터:", data)

        user_input = data.get("input", "")
        if not user_input:
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
        ai_response = response['choices'][0]['message']['content']
        print("OpenAI 응답:", ai_response)
        return jsonify({"response": ai_response})

    except Exception as e:
        print("서버 오류 발생:", str(e))
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))








