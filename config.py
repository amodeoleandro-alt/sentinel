import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base compartida."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-sentinel")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME_MINUTES = 30


class DevelopmentConfig(Config):
    """Desarrollo local."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")


class ProductionConfig(Config):
    """Producción en Render: Fuerza el uso de SQLite."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
