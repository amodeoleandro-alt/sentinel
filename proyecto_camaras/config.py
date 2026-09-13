import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base compartida por todos los entornos."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambiar-esta-clave-en-produccion")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Duración de la sesión por inactividad (requisito: cierre automático)
    PERMANENT_SESSION_LIFETIME_MINUTES = 30


class DevelopmentConfig(Config):
    """Entorno de desarrollo: SQLite local, sin necesidad de configurar un motor externo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "app.db")


class ProductionConfig(Config):
    """
    Entorno de producción: MySQL (por ejemplo, en AlwaysData).
    Configurar mediante variables de entorno:
      DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
    """
    DEBUG = False
    DB_USER = os.environ.get("DB_USER", "usuario")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "camaras_db")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
