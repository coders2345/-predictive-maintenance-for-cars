import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load the simulated sensor data
data = pd.read_csv('Data/vehicle_data.csv')

# Feature scaling
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data[['EngineTemp', 'BrakePressure', 'BatteryLife']])

# Initialize the Isolation Forest model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(scaled_data)

# Predict anomalies (-1 indicates anomaly, 1 indicates normal)
data['Anomaly'] = model.predict(scaled_data)

# Count the number of anomalies
num_anomalies = len(data[data['Anomaly'] == -1])
print(f"Anomalies detected: {num_anomalies}")

# Save the results to a new CSV file
data.to_csv('predicted_data.csv', index=False)
print("Anomaly detection complete. Results saved to 'predicted_data.csv'.")
