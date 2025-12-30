import os
from flask import Flask, request, jsonify
import numpy as np
from pyngrok import ngrok

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)

print("🚀 BADA-CALL-AI 서버 초기화 중...")

interpreter = None

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True)
    vals = {'x_acc': 0.0, 'y_acc': 9.8, 'z_acc': 0.0}

    if data and 'payload' in data:
        for item in data['payload']:
            if item['name'] in ['gravity', 'accelerometer', 'linear_acceleration']:
                p = item['values']
                vals['x_acc'], vals['y_acc'], vals['z_acc'] = p.get('x',0), p.get('y',0), p.get('z',0)

    max_acc = max(abs(vals['x_acc']), abs(vals['y_acc']), abs(vals['z_acc']))
    ai_prob = 0.0

    # 충격량이 15.0 m/s² (약 1.5G)를 넘으면 사고로 간주
    is_accident = 1 if max_acc > 15.0 else 0

    msg = "🚨 사고 감지!" if is_accident else "✅ 정상"
    print(f"📊 실시간 수신 - 충격량(Acc): {max_acc:4.1f} | 상태: {msg}")

    return jsonify({
        'is_accident': is_accident,
        'confidence': float(ai_prob),
        'message': msg
    })

if __name__ == '__main__':
    print("🌐 Ngrok 터널 개설 중...")
    try:
        ngrok_token = os.getenv('NGROK_AUTH_TOKEN')
        if not ngrok_token:
            print("⚠️ 경고: NGROK_AUTH_TOKEN 환경변수가 설정되지 않았습니다.")
            print("   .env 파일을 생성하거나 환경변수를 설정해주세요.")
            print("   예: export NGROK_AUTH_TOKEN='your_token_here'")
        else:
            ngrok.set_auth_token(ngrok_token)

        public_url = ngrok.connect(5000)
        print(f"\n🌍 외부 접속 주소 생성 성공!")
        print(f"🔗 Sensor Logger 앱 URL: {public_url}/predict")
        print(f"\n[서버 대기 중... 스마트폰에서 데이터를 보내주세요]")

        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"❌ 서버 실행 실패: {e}")
