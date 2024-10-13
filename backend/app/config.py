class Config:
    """Basis configuratie."""

    DEBUG = False
    TESTING = False
    # Database instellingen, secret keys, etc.


class DevelopmentConfig(Config):
    """Ontwikkelingsconfiguratie."""

    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testconfiguratie."""

    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """Productieconfiguratie."""

    DEBUG = False
