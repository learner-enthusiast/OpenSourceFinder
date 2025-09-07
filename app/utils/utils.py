from enum import Enum
import hmac
import hashlib
import os
import sendgrid
import logging

logger = logging.getLogger("uvicorn.error")


class ProjectFilters:
    """Container for all project filtering enums"""

    class Language(str, Enum):
        PYTHON = "python"
        JAVASCRIPT = "javascript"
        JAVA = "java"
        TYPESCRIPT = "typescript"
        GO = "go"
        RUBY = "ruby"
        CSHARP = "c#"
        CPP = "c++"
        PHP = "php"
        RUST = "rust"
        SWIFT = "swift"
        KOTLIN = "kotlin"
        SCALA = "scala"
        DART = "dart"
        C = "c"

    class SortField(str, Enum):
        STARS = "stars"
        FORKS = "forks"

    class Order(str, Enum):
        ASC = "asc"
        DESC = "desc"


class utils:
    SECRET_KEY = os.getenv("OTP_SECRET_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    SEND_GRID_API_KEY = os.getenv("SEND_GRID_API_KEY")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    @staticmethod
    def hash_otp_hmac(otp: str) -> str:
        return hmac.new(
            utils.SECRET_KEY.encode("utf-8"), otp.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    @staticmethod
    def verify_otp_hmac(input_otp: str, stored_hash: str) -> bool:
        return hmac.compare_digest(stored_hash, utils.hash_otp_hmac(input_otp))

    @staticmethod
    async def _send_email_otp(
        email: str,
        otp: str,
    ):
        """Send OTP via email using SendGrid"""

        try:
            message = sendgrid.Mail(
                from_email=utils.FROM_EMAIL,
                to_emails=email,
                subject="Your Login OTP",
                html_content=f"""
                    <h1>Your OTP Code</h1>
                    <p>Here is your OTP code: <strong>{otp}</strong></p>
                    <p>This code will expire in 2 minutes.</p>
                    <p>If you didn't request this code, please ignore this email.</p>
                """,
            )

            sg = sendgrid.SendGridAPIClient(utils.SEND_GRID_API_KEY)
            response = sg.send(message)

            if response.status_code not in [200, 202]:
                raise Exception(
                    f"SendGrid API returned status code {response.status_code}"
                )
            return True
        except Exception as e:
            logger.info(f"Email Otp send failed {e}")
            return False

    @staticmethod
    async def _send_sms_otp(phone: str, otp: str):
        try:
            from twilio.rest import Client

            client = Client(utils.TWILIO_ACCOUNT_SID, utils.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your login otp is: {otp}. Valid for 2 minutes.",
                from_=utils.TWILIO_PHONE_NUMBER,
                to=phone,
            )

            if not message.sid:
                raise Exception("Failed to get Message SID from TWILIO")
            logger.info(f"OTP SMS SENT SUCCESFULLY TO {phone}")
            return True
        except Exception as e:
            logger.error(f"OTP _Phone Failed {e}")
            return False
