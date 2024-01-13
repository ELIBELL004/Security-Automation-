import logging
import os
import re
import smtplib
import time
from datetime import datetime

# Configuration section
config = {
    "log_file": "/var/log/auth.log",
    "sender_email": "security_alerts@example.com",
    "recipient_email": "admin@example.com",
    "smtp_server": "your_smtp_server",
    "smtp_port": 587,
    "sender_username": "sender_username",
    "sender_password": "sender_password",
    "rules": {
        "failed_login": r"Failed password for .* from",
        "unauthorized_access": r"User .* tried to access",
        # Add more rules as needed
    },
    "check_interval": 5  # Check every 5 seconds
}

# Logging configuration
logging.basicConfig(filename="security_alerts.log", level=logging.INFO)

def send_alert(message):
    """Sends an email alert."""
    with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
        server.starttls()
        server.login(config["sender_username"], config["sender_password"])
        server.sendmail(
            config["sender_email"],
            config["recipient_email"],
            f"Subject: Security Alert\n\n{message}"
        )

def monitor_log():
    """Monitors the log file for suspicious events."""
    try:
        with open(config["log_file"], "r") as file:
            for line in file:
                for rule_name, rule_pattern in config["rules"].items():
                    if re.search(rule_pattern, line):
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        alert_message = f"{timestamp} - {rule_name}: {line.strip()}"
                        logging.info(alert_message)
                        send_alert(alert_message)
    except FileNotFoundError:
        logging.error(f"Log file not found: {config['log_file']}")

if __name__ == "__main__":
    while True:
        monitor_log()
        time.sleep(config["check_interval"])