from flask import request
import smtplib

@app.server.before_request
def notify_on_visit():
    user_ip = request.remote_addr
    # Send email via SMTP or log to file
    print(f"🔔 New visit from {user_ip}")