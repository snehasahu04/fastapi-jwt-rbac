import os
import smtplib
from email.mime.text import MIMEText


# EMAIL CONFIG

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "snehademo4@gmail.com")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "tfsadpaknlicozmu")   # Gmail App Password
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", SENDER_EMAIL)



def send_email(receiver: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


def send_admin_notification(subject: str, body: str):
    return send_email(ADMIN_EMAIL, subject, body)


def send_signup_email(email: str):
    user_ok = send_email(email, "Signup Alert", "Signup successful. Welcome!")
    admin_ok = send_admin_notification(
        "New user signup",
        f"A new user signed up with email: {email}"
    )
    return user_ok or admin_ok


def send_login_email(email: str):
    user_ok = send_email(email, "Login Alert", "You logged in successfully")
    admin_ok = send_admin_notification(
        "User login",
        f"User logged in with email: {email}"
    )
    return user_ok or admin_ok


def send_promotion_email(email: str):
    user_ok = send_email(email, "Promotion Alert", "You are promoted to INTERN")
    admin_ok = send_admin_notification(
        "User promoted",
        f"User promoted to intern: {email}"
    )
    return user_ok or admin_ok