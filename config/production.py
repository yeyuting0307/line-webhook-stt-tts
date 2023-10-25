import os
class ProductionConfig:
    DEBUG = False # Debug Mode Off
    SECRET_KEY = os.environ.get('PROD_FLASK_SECRET_KEY', 'should-be-complex-secret-key')
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
