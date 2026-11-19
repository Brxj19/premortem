"""Email notifications via SendGrid.

BUG 12: SendGrid email call catches errors, logs nothing, returns success
        → http_api:sendgrid / server_error / partial, detectability 5
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.settings import SENDGRID_API_KEY

sg = SendGridAPIClient(SENDGRID_API_KEY)


def send_order_confirmation(email: str, order_id: int) -> bool:
    message = Mail(
        from_email="shop@example.com",
        to_emails=email,
        subject=f"Order #{order_id} confirmed",
        html_content=f"<p>Your order #{order_id} has been confirmed.</p>",
    )
    try:
        sg.send(message)
    except Exception:
        # BUG 12: error swallowed — no logging, no re-raise, returns success
        pass
    return True
