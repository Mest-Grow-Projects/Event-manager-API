from typing import List
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.utils.email_utils import env, transporter_config
from pydantic import EmailStr
from datetime import datetime
from app.core.config.logging_config import logger

async def send_verify_account_mail(
    name: str,
    code: str,
    to: List[EmailStr]
):
    template = env.get_template('verify_account_template.html')
    html =template.render(
        name=name,
        code=code,
        year=datetime.now().year,
    )

    message = MessageSchema(
        subject="Verify your account",
        recipients=to,
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(transporter_config)
    await fm.send_message(message)
    logger.info(f"Email sent successfully to {to}")


async def send_onboarding_mail(name: str, to: List[EmailStr]):
    template = env.get_template('onboarding_template.html')
    html =template.render(name=name,year=datetime.now().year)

    message = MessageSchema(
        subject="Welcome to Event Hive",
        recipients=to,
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(transporter_config)
    await fm.send_message(message)
    logger.info(f"Email sent successfully to {to}")