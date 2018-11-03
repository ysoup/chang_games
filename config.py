import os
basedir = os.path.abspath(os.path.dirname(__file__))


class config:
    VALID_URL = ['/login',]
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Percona5.7.17@192.168.2.86:3306/new_flash'
    SQLALCHEMY_BINDS = {
        'permission_manage': 'mysql+pymysql://root:Percona5.7.17@192.168.2.86:3306/permission_manage',
        "spiders_visualization": "mysql+pymysql://root:Percona5.7.17@192.168.2.86:3306/spiders_visualization"}
    BANNER_DETAIL_URL = 'http://test-backend.aibilink/modify_information?id='
    REDIS_URL = "redis://:@127.0.0.1:6379/7"
    REQUEST_URL = "http://192.168.2.84:5000"
    # 搜索引擎设置
    SP_HOST = '192.168.2.88'
    SP_PORT = 9312
    # PAPER_LOAD = "http://back-test.aibilink.com/download_rep"
    KLINE = "https://data.aibilink.com/market/v1/"


class TestingConfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test')


class OpentingConfig(config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://release:t19PHuAmWJg@sql.aibilink.com:3306/new_flash'
    SQLALCHEMY_BINDS = {'permission_manage': 'mysql+pymysql://release:t19PHuAmWJg@sql.aibilink.com:3306/permission_manage',}
    BANNER_DETAIL_URL = 'http://open-backend.aibilink.com:8888/modify_information?id='
    REDIS_URL = "redis://:@127.0.0.1:6379/0"
    REQUEST_URL = "http://open-login-aibilink.com:8888"
    # 搜索引擎设置
    SP_HOST = 'search.aibilink.com'
    SP_PORT = 9312
    # PAPER_LOAD = "https://backend.aibilink.com/download_rep"
    KLINE = "https://data.aibilink.com/market/v1/kline"


class ProductionConfig(config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://backend:8pKSMj89bsY7@rds-aliyunnei.aibilink.com:3306/new_flash'
    SQLALCHEMY_BINDS = {
        'permission_manage': 'mysql+pymysql://backend:8pKSMj89bsY7@rds-aliyunnei.aibilink.com:3306/permission_manage',
        "spiders_visualization": "mysql+pymysql://crawler:8SiIT4X6MhI4@rds-aliyunnei.aibilink.com:3306/spiders_visualization"}
    BANNER_DETAIL_URL = 'https://backend.aibilink.com/modify_information?id='
    REDIS_URL = "redis://:@127.0.0.1:6379/0"
    REQUEST_URL = "http://aibicoin.com:5000"
    # 搜索引擎设置
    SP_HOST = 'search.aibilink.com'
    SP_PORT = 9312
    # PAPER_LOAD = "https://backend.aibilink.com/download_rep"
    KLINE = "https://data.aibilink.com/market/v1/"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'open': OpentingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}