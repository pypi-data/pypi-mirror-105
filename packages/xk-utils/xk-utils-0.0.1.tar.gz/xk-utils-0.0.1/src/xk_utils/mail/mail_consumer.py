import json
import os
import time
import redis

from xk_utils.logger import get_logger
from xk_utils.mail.config import *

from xk_utils.mail.send import do_send_mail

logger = get_logger("mail_log", write_file=False, send_mail=False)


def mail_consumer(mail_prefix, **redis_config):
    """
    :param mail_prefix: redis mail key 前缀
    :param redis_config:
    :return:
    """
    logger.info(f'start send logger, mail_prefix:{mail_prefix}')
    redis_conn = redis.Redis(**redis_config)
    keys = redis_conn.keys(mail_prefix + '*')
    for key in keys:
        contents = []
        while True:
            # 从redis获取数据， 500 或者为空时结束
            value = redis_conn.rpop(keys)
            if value:
                data = json.loads(value.decode('utf8'))
                content = data.get('content') or json.dumps(data)
                contents.append(content)
            else:
                break

            if len(contents) >= 500:
                break

        do_send_mail(key, '\n'.join(contents))


def main():
    redis_config = {
        'host': os.environ['REDIS_HOST'],
        'port': os.environ['REDIS_PORT'],
        'password': os.environ['REDIS_PASSWORD'],
        'db': os.environ['REDIS_MAIL_DB'],

    }
    from apscheduler.schedulers.background import BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(mail_consumer, trigger='interval', args=(MAIL_PREFIX,), kwargs=redis_config, seconds=5 * 60)
    scheduler.add_job(mail_consumer, trigger='interval', args=(MAIL_PREFIX_NOW,), kwargs=redis_config, seconds=5)
    scheduler.start()


if __name__ == '__main__':
    main()
