# Configuration file

DEBUG = True

LANG = "fr"

# DB_URL = "mysql://stacosys_user:stacosys_password@localhost:3306/stacosys"
DB_URL = "sqlite:///db.sqlite"

MAIL_URL = "http://localhost:8025/mbox"

HTTP_ADDRESS = "0.0.0.0"
HTTP_PORT = 8100
HTTP_WORKERS = 1
CORS_ORIGIN = "*"

SALT = "BRRJRqXgGpXWrgTidBPcixIThHpDuKc0"

SECRET = "Uqca5Kc8xuU6THz9"

ROOT_URL = 'http://localhost:8000'

RSS_URL_PROTO = 'http'
RSS_FILE = 'comments.xml'
