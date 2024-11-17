import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random as rp
# Set the page configuration
st.set_page_config(page_title="Vehicle Dashboard", layout="wide")

# Load the predicted data
data = pd.read_csv('Data/predicted_data.csv')
latest_data = data.iloc[-1]

# Extract sensor readings
engine_temp = latest_data['EngineTemp']
# engine_temp = round(rp.uniform(80, 120), 2)
brake_pressure = latest_data['BrakePressure']
battery_life = latest_data['BatteryLife']

# Customizable Alert Thresholds
st.sidebar.markdown("### Customize Alert Thresholds")
engine_temp_threshold = st.sidebar.slider("Engine Temperature Alert Threshold (°C)", 60, 180, 110)
battery_life_threshold = st.sidebar.slider("Battery Life Alert Threshold (%)", 10, 100, 30)
brake_pressure_threshold = st.sidebar.slider("Brake Pressure Alert Threshold (PSI)", 30, 100, 85)

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("Enable Dark Mode", value=False)

# Apply Dark Mode CSS
if dark_mode:
    st.markdown("""
        <style>
        body {
            background-color: #2e2e2e;
            color: #f1f1f1;
        }
        </style>
    """, unsafe_allow_html=True)

# Health Status Calculation
battery_health = "Good" if battery_life > 50 else "Fair" if battery_life > 20 else "Poor"
engine_health = "Good" if engine_temp < 105 else "Overheating"
tire_health = "Good" if brake_pressure < 70 else "Check Tires"
overall_health = "Good" if battery_health == "Good" and engine_health == "Good" and tire_health == "Good" else "Needs Attention"

# Display Dashboard Title
st.title("🚗 Enhanced Vehicle Monitoring Dashboard")

# Toggle for Mobile View
mobile_view = st.sidebar.checkbox("Mobile View", value=False, key="mobile_toggle")

# Define columns based on view mode
if mobile_view:
    col1 = col2 = col3 = st.columns(1)[0]
else:
    col1, col2, col3 = st.columns(3)

# Battery Health Gauge
with col1:
    fig_battery = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=battery_life,
        title={'text': "Battery Life (%)"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "blue"}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    st.plotly_chart(fig_battery, use_container_width=True, tooltip="Current battery life percentage.")

# Engine Temperature Gauge
with col2:
    fig_engine = go.Figure(go.Indicator(
        mode="gauge+number",
        value=engine_temp,
        title={'text': "Engine Temperature (°C)"},
        gauge={'axis': {'range': [0, 150]}, 'bar': {'color': "red"}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    st.plotly_chart(fig_engine, use_container_width=True, tooltip="Engine temperature in degrees Celsius.")

# Brake Pressure Gauge
with col3:
    fig_brake = go.Figure(go.Indicator(
        mode="gauge+number",
        value=brake_pressure,
        title={'text': "Brake Pressure (PSI)"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    st.plotly_chart(fig_brake, use_container_width=True, tooltip="Brake pressure in PSI.")

# Health Check Summary
st.markdown("### Health Check Summary")
summary_cols = st.columns(1) if mobile_view else st.columns(4)
with summary_cols[0]:
    st.metric(label="Battery Health", value=battery_health, delta=f"{battery_life}%")
with summary_cols[1 if not mobile_view else 0]:
    st.metric(label="Engine Health", value=engine_health, delta=f"{engine_temp}°C")
with summary_cols[2 if not mobile_view else 0]:
    st.metric(label="Tire Health", value=tire_health, delta=f"{brake_pressure} PSI")
with summary_cols[3 if not mobile_view else 0]:
    st.metric(label="Overall Vehicle Health", value=overall_health)

# Predictive Notifications
st.markdown("### Predictive Maintenance Alerts")
alert_count = 0

if  engine_temp_threshold > 110 :
    st.warning(f"⚠️ High Engine Temperature! Consider reducing speed or checking the cooling system. Current:")
    alert_count += 1
if battery_life > battery_life_threshold:
    st.warning(f"⚠️ Low Battery Life! Consider checking the charging system. Current: {battery_life}%")
    alert_count += 1
if brake_pressure > brake_pressure_threshold:
    st.warning(f"⚠️ Low Brake Pressure! Possible tire or brake issue. Current: {brake_pressure} PSI")
    alert_count += 1

# Display Alert Summary
st.info(f"Total Alerts: {alert_count}")

# Animated Real-Time Sensor Trends
st.markdown("### Real-Time Sensor Data Trends")
fig_trends = px.line(data.tail(50), x=data.index[-50:], y=['EngineTemp', 'BrakePressure', 'BatteryLife'],
                     title="Real-Time Sensor Data Trends", labels={'index': 'Time', 'value': 'Sensor Value'})
fig_trends.update_layout(height=400)
st.plotly_chart(fig_trends, use_container_width=True)

# Footer
st.sidebar.success("Enhanced dashboard loaded successfully.")
