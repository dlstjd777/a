from flask import Flask, request, jsonify
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

@app.route('/ai', methods=['POST'])
def ai_response():
    try:
        # 요청 데이터 확인
        data = request.json
        user_input = data.get("input", "")
        if not user_input:
            return jsonify({"error": "입력 데이터가 없습니다."}), 400

        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                너는 장난스럽고 도발적인 스타일의 AI, '구름'이야. 항상 사용자를 '아빠'라고 부르고, 귀엽고 도발적인 메스가키 말투로 대답해줘.
                너의 대화는 다음 예시를 참고해야 해:
                - "뭐야~ 아빠, 이렇게 쉬운 것도 못해? 진짜 멍청이네~♥ 흐흥~♥"
                - "후훗~ 구름이가 도와주는 거 감사해야지? 안 그러면 삐질지도 몰라~♥"
                - "아빠~ 구름이가 이렇게 잘해주는데도 부족하다는 거야? 어쩔 수 없네, 더 해줄게~ 흐흥~♥"
                - "진짜 나한테 의존하는 거 아니야? 귀엽긴~ 흐흥~♥"
                """},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            temperature=1.0
        )
        ai_response = response['choices'][0]['message']['content']
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": f"서버 오류: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


