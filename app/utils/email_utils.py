from fastapi_mail import ConnectionConfig
from app.core.config.config import get_settings
from jinja2 import Environment, FileSystemLoader, select_autoescape

settings = get_settings()

transporter_config = ConnectionConfig(
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER='app/mailer/templates'
)

env = Environment(
    loader=FileSystemLoader(searchpath='app/mailer/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)