import smtplib
import pandas as pd

# Load the predicted data with anomalies
data = pd.read_csv('Data/predicted_data.csv')
anomalies = data[data['Anomaly'] == -1]


# Function to send email alerts
def send_email_alert(subject, body, to_email):
    from_email = "mabasham52@gmail.com"
    app_password = "gmvb fqmm zpxx uumy"  # Use the App Password here

    message = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, message)
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print("Error sending email:", e)


# Check if there are anomalies and send an alert
if len(anomalies) > 0:
    subject = "Vehicle Anomaly Alert"
    body = f"Anomalies detected in vehicle data.  Please check the dashboard for details."
    send_email_alert(subject, body, "hariharabudra@gmail.com")
else:
    print("No anomalies detected. No email alert sent.")
