import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '21237&^^&^&(*!6515725&@!&*!87198229387hjesaj21122*&^%%^@%&#&*'
    # MSSQL connection configuration
    DB_DRIVER = os.environ.get('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    DB_SERVER = os.environ.get('DB_SERVER', 'localhost')
    DB_DATABASE = 'Q_Ops'
    DB_USERNAME = os.environ.get('DB_USERNAME', 'sa')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '_9q29838922cg')
    DB_TRUSTED_CONNECTION = os.environ.get('DB_TRUSTED_CONNECTION', 'yes')
    # Email / OTP
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'vishal@ri.in')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', ' ksln')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'vishal_jayaswal@emri.in')
