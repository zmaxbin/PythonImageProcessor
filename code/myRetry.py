# -*- coding:utf-8 -*-

import functools
import time

def retry(logger=None,number_of_retry=3,delay=3):
    def decorator(func):
        @functools.wraps(func)
        def action(*args, **kwargs):
            mretry,mdealy = number_of_retry,delay
            while mretry > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    msg = "获取网页数据失败！"
                    logger.error(msg)
                    logger.error(ex, exc_info=1)
                    time.sleep(mdealy)
                    mretry -= 1
            logger.error("三次都失败!")
        return action
    return decorator