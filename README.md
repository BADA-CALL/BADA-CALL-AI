# 🌊 BADA-CALL-AI: Maritime Safety Intelligence System

**BADA-CALL-AI**는 인공지능을 활용하여 해양 사고를 사전에 예측하고, 사고 발생 시 실시간으로 감지하여 신속한 구조를 돕는 통합 안전 솔루션입니다.

## 🚀 Key Features

1. **Smart Accident Detection**: 스마트폰 센서 데이터를 딥러닝(TFLite)으로 분석하여 선박 전복 및 낙상 사고 실시간 감지.
2. **Maritime Risk Prediction**: 공공데이터(기상청 부이, 해양사고 통계)를 기반으로 현재 기상 상황에 따른 사고 확률 도출.

## 📂 Project Structure

- `/smart_detection`: 스마트폰 센서 기반 실시간 사고 감지 서버 및 학습 코드.
- `/risk_prediction`: 과거 사고 통계와 기상을 결합한 사고 예측 모델.

## 🛠 Tech Stack

- **Language**: Python 3.x
- **AI/ML**: TensorFlow (TFLite), Scikit-learn (RandomForest)
- **Server**: Flask, Ngrok
- **Data**: Kaggle Human Activity Dataset, 해양수산부 사고 통계현황, 기상청 부이 데이터

## ⚙️ 환경 설정

### Smart Detection 모듈 사용 시

Ngrok 토큰이 필요합니다. 다음 중 하나의 방법으로 설정하세요:

1. **환경변수로 설정** (권장):
```bash
export NGROK_AUTH_TOKEN='your_token_here'
```

2. **.env 파일 생성** (python-dotenv 설치 시):
```bash
# .env 파일 생성
echo "NGROK_AUTH_TOKEN=your_token_here" > .env
```

Ngrok 토큰 발급: https://dashboard.ngrok.com/get-started/your-authtoken
