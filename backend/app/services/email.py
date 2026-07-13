from flask import current_app
from flask_mail import Message
from app import mail
import logging

logger = logging.getLogger(__name__)


def send_contact_confirmation_email(contact_name: str, contact_email: str, subject: str):
    """Send confirmation email to user after contact form submission."""
    try:
        sender = current_app.config.get("MAIL_DEFAULT_SENDER")
        msg = Message(
            subject="Pypycode message",
            recipients=[contact_email],
            sender=sender,
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">Thank you for contacting us!</h2>
                        <p>Hi {contact_name},</p>
                        <p>We've received your message with the subject: <strong>{subject}</strong></p>
                        <p>Our team will review your inquiry and get back to you as soon as possible.</p>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="font-size: 12px; color: #666;">
                            If you have any additional information to add, please reply to this email.
                        </p>
                        <p style="font-size: 12px; color: #666;">
                            Best regards,<br>
                            The PyPyCode Team
                        </p>
                    </div>
                </body>
            </html>
            """
        )
        mail.send(msg)
        logger.info(f"Confirmation email sent to {contact_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {contact_email}: {str(e)}")
        return False


def send_contact_notification_email(contact_name: str, contact_email: str, subject: str, message: str, admin_email: str):
    """Send notification email to admin about new contact submission."""
    try:
        sender = current_app.config.get("MAIL_DEFAULT_SENDER")
        msg = Message(
            subject="Pypycode message",
            recipients=[admin_email],
            sender=sender,
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2c3e50;">New Contact Form Submission</h2>
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Name:</strong> {contact_name}</p>
                            <p><strong>Email:</strong> {contact_email}</p>
                            <p><strong>Subject:</strong> {subject}</p>
                            <p><strong>Message:</strong></p>
                            <p style="white-space: pre-wrap; background-color: white; padding: 10px; border-left: 3px solid #2c3e50;">
{message}
                            </p>
                        </div>
                        <p>
                            <a href="https://pypycode.com/admin/contact" style="display: inline-block; padding: 10px 20px; background-color: #2c3e50; color: white; text-decoration: none; border-radius: 5px;">
                                View in Admin Panel
                            </a>
                        </p>
                    </div>
                </body>
            </html>
            """
        )
        mail.send(msg)
        logger.info(f"Admin notification email sent for contact from {contact_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send admin notification email: {str(e)}")
        return False
