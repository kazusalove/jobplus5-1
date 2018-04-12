class BaseConfig(object):
    pass

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus'

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass


configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
        }
