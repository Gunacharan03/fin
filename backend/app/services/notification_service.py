"""
Notification service.

This is a lightweight, provider-agnostic notification layer. Out of the box
it logs notifications server-side (visible in your terminal/logs) so the
rest of the app (reminders, alerts) has somewhere to call into without
requiring you to set up an email/SMS provider just to run the project.

To wire up real notifications later:
    - Email: plug in smtplib or a provider SDK (SendGrid, Postmark, SES) in `send_email`.
    - SMS/WhatsApp: plug in Twilio or similar in `send_sms`.
Both functions already have the right call signatures — route_handlers
and agents call `notify_user`, not the provider-specific functions directly,
so swapping providers later doesn't require touching calling code.
"""
import logging

logger = logging.getLogger("fin.notifications")


async def send_email(to_email: str, subject: str, body: str) -> bool:
    # TODO: integrate a real email provider (SendGrid/SES/SMTP) here.
    logger.info(f"[EMAIL STUB] To: {to_email} | Subject: {subject}\n{body}")
    return True


async def send_sms(phone_number: str, message: str) -> bool:
    # TODO: integrate Twilio or similar SMS/WhatsApp provider here.
    logger.info(f"[SMS STUB] To: {phone_number} | {message}")
    return True


async def notify_user(user: dict, title: str, message: str) -> bool:
    """
    Generic entry point used by routes/agents. Currently logs only;
    extend this to call send_email/send_sms once a provider is configured.
    """
    logger.info(f"[NOTIFICATION] User: {user.get('email')} | {title}: {message}")
    return True
