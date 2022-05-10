from decouple import config


class Config:
    SECRET_KEY = config("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = f'mysql://{config("DB_USER")}:{config("DB_PASSWORD")}@{config("DB_HOST")}/tareas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config("DEV_MAIL_USERNAME")
    MAIL_PASSWORD = config("DEV_MAIL_PASSWORD")


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}
