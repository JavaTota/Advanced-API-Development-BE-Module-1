class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Jahvante.97.mysql@localhost/mechanic_shop'
    DEBUG = True # Enable debug mode for development

class TestingConfig:
    pass

class ProductionConfig:
    pass