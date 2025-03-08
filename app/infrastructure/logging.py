import logging.config

from app.infrastructure import settings

# Настраиваем логирование с использованием словаря конфигурации: вывод в файл и консоль.

log_file='app/orders.log'

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
         'default': {
              'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
         },
    },
    'handlers': {
         'file': {
              'level': 'INFO',
              'class': 'logging.FileHandler',
              'filename': log_file,
              'formatter': 'default',
         },
         'console': {
              'class': 'logging.StreamHandler',
              'formatter': 'default',
         },
    },
    'loggers': {
         'orders': {
              'handlers': ['file', 'console'],
              'level': 'INFO',
              'propagate': True,
         },
    },
})
logger = logging.getLogger("orders")