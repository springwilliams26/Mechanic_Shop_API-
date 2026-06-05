class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic_shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True
    CACHE_TYPE = "SimpleCache"