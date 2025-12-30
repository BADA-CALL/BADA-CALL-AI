import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def build_bada_model(acc_path, buoy_path):
    # 데이터 로드 (인코딩 대응)
    def load(p):
        for e in ['cp949', 'utf-8-sig']:
            try: return pd.read_csv(p, encoding=e)
            except: continue

    df_acc, df_buoy = load(acc_path), load(buoy_path)

    y, m, d = df_acc.columns[3:6]
    df_acc['date'] = pd.to_datetime(df_acc[[y, m, d]].astype(str).agg('-'.join, axis=1)).dt.date
    df_buoy['date'] = pd.to_datetime(df_buoy.iloc[:, 1]).dt.date

    cols = df_buoy.columns[2:5]
    df_buoy[cols] = df_buoy[cols].apply(pd.to_numeric, errors='coerce')
    df_buoy = df_buoy.dropna(subset=cols)

    df_acc['label'] = 1
    merged = pd.merge(df_buoy, df_acc[['date', 'label']].drop_duplicates(), on='date', how='left').fillna(0)

    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(merged[cols], merged['label'])
    return model, cols

def predict_bada_risk(model, feature_names, ws, mw, wh):
    base_prob = model.predict_proba(pd.DataFrame([[ws, mw, wh]], columns=feature_names))[0][1]

    # 체감형 확률 보정 (Sigmoid)
    score = (ws / 15.0) * 0.5 + (wh / 3.0) * 0.5
    refined_prob = 1 / (1 + np.exp(-7 * (score - 0.75)))

    final_pct = (base_prob * 60) + (refined_prob * 40)
    final_pct = max(min(final_pct, 85.0), 5.0)

    # 초저위험 구간 보정
    if ws < 5.0 and wh < 0.5: final_pct = 5.0 + (ws * 0.4)

    level = "🔴 위험" if final_pct > 60 else ("🟡 주의" if final_pct > 20 else "🟢 안전")
    return round(final_pct, 1), level
