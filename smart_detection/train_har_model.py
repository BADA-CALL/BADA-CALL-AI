import kagglehub
import pandas as pd
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import layers

path = kagglehub.dataset_download("enricogrimaldi/falls-vs-normal-activities")
all_files = [f for f in os.listdir(path) if f.endswith('.csv')]
full_df = pd.DataFrame()

for file in all_files:
    temp_df = pd.read_csv(os.path.join(path, file))
    temp_df['label'] = 1 if 'fall' in file.lower() else 0
    full_df = pd.concat([full_df, temp_df], ignore_index=True)

X = full_df[['xAcc', 'yAcc', 'zAcc', 'xGyro', 'yGyro', 'zGyro']]
y = full_df['label']

model = tf.keras.Sequential([
    layers.InputLayer(input_shape=(6,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=10, batch_size=32, verbose=1)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('har_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("✅ har_model.tflite 생성 완료.")
