from typing import List
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks
from app.utils.email_utils import env, transporter_config
from pydantic import EmailStr
from datetime import datetime

async def send_verify_account_mail(
    background_tasks: BackgroundTasks,
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
    background_tasks.add_task(fm.send_message, message)
    return {"message": "Verification email sent"}