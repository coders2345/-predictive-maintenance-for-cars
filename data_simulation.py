import random
import pandas as pd


# Function to generate mock sensor data
def generate_sensor_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        engine_temp = round(random.uniform(70, 120), 2)  # Engine temperature in Celsius
        brake_pressure = round(random.uniform(30, 80), 2)  # Brake pressure in PSI
        battery_life = random.randint(0, 100)  # Battery life percentage
        data.append([engine_temp, brake_pressure, battery_life])

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(data, columns=['EngineTemp', 'BrakePressure', 'BatteryLife'])
    df.to_csv('vehicle_data.csv', index=False)
    print("Data simulation complete. Data saved to 'vehicle_data.csv'.")


# Run the data simulation
if __name__ == "__main__":
    generate_sensor_data()
