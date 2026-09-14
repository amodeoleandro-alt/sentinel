import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base compartida por todos los entornos."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambiar-esta-clave-en-produccion")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME_MINUTES = 30


class DevelopmentConfig(Config):
    """Entorno de desarrollo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")


class ProductionConfig(Config):
    """Entorno de producción: Usa MySQL si existen credenciales, de lo contrario SQLite."""
    DEBUG = False
    
    # Si existen variables de MySQL o DATABASE_URL las usa; si no, recurre a SQLite en la raíz
    if os.environ.get("DB_HOST"):
        DB_USER = os.environ.get("DB_USER", "usuario")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
        DB_HOST = os.environ.get("DB_HOST")
        DB_NAME = os.environ.get("DB_NAME", "camaras_db")
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    elif os.environ.get("DATABASE_URL"):
        db_url = os.environ.get("DATABASE_URL")
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
