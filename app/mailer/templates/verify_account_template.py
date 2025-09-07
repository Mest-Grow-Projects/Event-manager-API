from .base_template import email_template

def verification_email_template(code: str, name: str) -> str:
    content = f"""
    <div class="content">
        <h2>Verify Your Account</h1>
        <p>Hello {name},</p>
        <p>Thank you for registering with Event Hive! To complete your 
            registration, please use the verification code below:
        </p>
        <div class="verification-code">{code}</div>
        <p>This verification code will expire in <strong>30 minutes</strong>.</p>
        <div class="warning">
        ⚠️ Never share this code with anyone. Our team will never ask for your verification code.
        </div>
        <p>If you did not sign up for this account, please ignore this email.</p>
        <p>Best regards,<br>The Event Hive Team</p>
    </div>
    """

    return email_template(content)