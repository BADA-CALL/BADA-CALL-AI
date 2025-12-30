import os
import sys

# 경로 자동 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

print("🔍 모델 로딩 시도 중...")

from risk_prediction.maritime_risk_model import build_bada_model, predict_bada_risk

acc_path = os.path.join(parent_dir, 'accident.csv')
buoy_path = os.path.join(parent_dir, 'weather.csv')

print(f"📂 사고 데이터 경로: {acc_path}")
print(f"📂 기상 데이터 경로: {buoy_path}")

if not os.path.exists(acc_path) or not os.path.exists(buoy_path):
    print("❌ 에러: CSV 파일이 프로젝트 폴더에 없습니다! 파일명을 확인해주세요.")
    sys.exit()

try:
    print("🧠 데이터 분석 및 AI 모델 빌드 중... (잠시만 기다려주세요)")
    model, features = build_bada_model(acc_path, buoy_path)
    print("✅ 모델 빌드 완료!\n")
except Exception as e:
    print(f"❌ 모델 로딩 중 에러 발생: {e}")
    sys.exit()

scenarios = [
    {"name": "매우 안전", "data": [2.0, 0.3, 0.2]},
    {"name": "주의보 수준", "data": [12.0, 2.5, 1.8]},
    {"name": "위험(폭풍우)", "data": [18.0, 5.0, 3.5]}
]

print(f"{'상황':<15} | {'풍속':<5} | {'파고':<5} | {'확률':<7} | {'등급'}")
print("-" * 55)

for s in scenarios:
    prob, level = predict_bada_risk(model, features, *s['data'])
    print(f"{s['name']:<15} | {s['data'][0]:>5.1f} | {s['data'][1]:>5.1f} | {prob:>5.1f}% | {level}")
