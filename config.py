class DevelopmentConfig():
    DEBUG = True
    SECRET_KEY = 'examePizzas'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/examePizzas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False