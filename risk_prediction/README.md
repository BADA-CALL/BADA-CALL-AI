# 📊 Maritime Risk Prediction AI

기상 데이터와 과거 사고 사례를 분석하여 현재 항해 환경의 위험도를 5%~85%의 확률로 계산합니다.

## 🧪 AI Model & Logic

- **Algorithm**: Random Forest Classifier
- **Probability Scaling**: 사용자의 체감을 고려하여 Sigmoid 보정 로직을 적용했습니다.
- **Key Features**: 풍속(Wind Speed), 최대파고(Max Wave Height), 유의파고(Significant Wave Height).

## 🌡️ Risk Levels

- **🟢 안전 (5~20%)**: 기상으로 인한 사고 위험이 낮음.
- **🟡 주의 (20~60%)**: 기상 악화 시작, 소형 선박 주의 요망.
- **🔴 위험 (60~85%)**: 사고 발생 확률 매우 높음, 출항 자제 권고.

## 📂 Data Sources

- **Accident Data**: 해양수산부 중앙해양안전심판원 통계현황.
- **Weather Data**: 기상청 기상부이(Buoy) 관측 데이터.
