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

---

## 📡 BADA-CALL AI API 명세서

### Endpoint: `POST /predict`

스마트폰 센서 데이터를 실시간으로 전송하여 사고 여부를 판단합니다.

#### Request

**URL**: `{server_url}/predict`
**Method**: `POST`
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "payload": [
    {
      "name": "accelerometer",
      "values": {
        "x": 0.0,
        "y": 9.8,
        "z": 0.0
      }
    }
  ]
}
```

**Parameters**:
- `payload` (array, required): 센서 데이터 배열
  - `name` (string, required): 센서 타입 (`accelerometer`, `gravity`, `linear_acceleration` 중 하나)
  - `values` (object, required): 센서 값
    - `x` (float): X축 가속도 (m/s²)
    - `y` (float): Y축 가속도 (m/s²)
    - `z` (float): Z축 가속도 (m/s²)

**Example (cURL)**:
```bash
curl -X POST https://your-ngrok-url.ngrok.io/predict \
  -H "Content-Type: application/json" \
  -d '{
    "payload": [
      {
        "name": "accelerometer",
        "values": {"x": 0.0, "y": 9.8, "z": 0.0}
      }
    ]
  }'
```

#### Response

**Success Response (200 OK)**:
```json
{
  "is_accident": 1,
  "confidence": 0.85,
  "message": "🚨 사고 감지!"
}
```

**Response Fields**:
- `is_accident` (integer): 사고 발생 여부 (`0`: 정상, `1`: 사고 감지)
- `confidence` (float): AI 신뢰도 (0.0 ~ 1.0, 현재는 0.0으로 고정)
- `message` (string): 상태 메시지 (`"✅ 정상"` 또는 `"🚨 사고 감지!"`)

**판정 기준**:
- 충격량(최대 가속도)이 15.0 m/s² (약 1.5G)를 초과하면 사고로 판정

**Example Responses**:

정상 상태:
```json
{
  "is_accident": 0,
  "confidence": 0.0,
  "message": "✅ 정상"
}
```

사고 감지:
```json
{
  "is_accident": 1,
  "confidence": 0.0,
  "message": "🚨 사고 감지!"
}
```

---

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/BADA-CALL/BADA-CALL-AI.git
cd BADA-CALL-AI
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 필요한 환경 변수를 설정하세요:
```bash
cp .env.example .env
# .env 파일을 열어서 NGROK_AUTH_TOKEN을 입력하세요
```

### 4. 서버 실행
```bash
cd smart_detection
python app_server.py
```

서버 실행 후 출력된 Ngrok URL을 확인하고, 스마트폰 앱(Sensor Logger 등)에서 해당 URL의 `/predict` 엔드포인트로 데이터를 전송하세요.
