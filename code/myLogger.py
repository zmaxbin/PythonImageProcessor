# -*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('../data/run.log',maxBytes=5*1024*1024)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger('antiFraud')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
handler.setLevel(logging.DEBUG)