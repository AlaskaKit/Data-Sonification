class Config(object):
	DEBUG = False
	TESTING = False
	SESSION_COOKIE_SECURE = True
	ALLOWED_EXTENSIONS = ["XLS", "XLSX", "CSV"]
	SECRET_KEY = "autogenerated secret key"


class ProductionConfig(Config):
	SRC_UPLOADS = r'set prod path'
	WAV_FILES = r'set prod path'


class DevelopmentConfig(Config):
	DEBUG = True
	SRC_UPLOADS = r'set dev path'
	WAV_FILES = r'set dev path'
	SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
	DEBUG = True
	SRC_UPLOADS = r'set test path'
	WAV_FILES = r'set test path'
	SESSION_COOKIE_SECURE = False
