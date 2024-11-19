from huey import RedisHuey
from redis import ConnectionPool

from project.settings.general import DEBUG

SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'TITLE': 'Тестовое задание',
    'DESCRIPTION': 'Swagger',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Настройки huey
REDIS_HOST = '127.0.0.1' if DEBUG else 'redis'
POOL = ConnectionPool(host=REDIS_HOST, port=6379, max_connections=20)
HUEY = RedisHuey('xml_parser', connection_pool=POOL)
