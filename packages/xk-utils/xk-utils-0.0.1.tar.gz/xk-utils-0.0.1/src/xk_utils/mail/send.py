import os
from logging import getLogger
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


def do_send_mail(key, contents, _subtype='plain', mysql_config=None):
    logger = getLogger()
    if mysql_config is None:
        mysql_config = {}

    """
    :param title: 邮件标题
    :param contents: 邮件内容
    :param from_addr: 来源地址， 如果不提供， 用config mail_user 参数
    :param to_addrs: 发送地址，list, 如果不提供， 用name参数
    :param _subtype: 数据类型 plain, html
    :param name: 对应邮件地址，在数据库中查询
    :return:
    """
    mail_host = os.environ['MAIL_HOST']
    mail_port = os.environ['MAIL_PORT']
    mail_user = os.environ['MAIL_USER']
    from_addr = os.environ['MAIL_USER']
    mail_password = os.environ['MAIL_PASSWORD']
    import pymysql
    sql = f'select mail_addr, title from mail_send where name=%s'
    conn = pymysql.Connection(**mysql_config)
    with conn.cursor() as cursor:
        cursor.execute(sql, args=(key,))
        result = cursor.fetch_one()
        to_addrs = result[0]
        title = result[1]

    message = MIMEText(contents, _subtype, 'utf-8')
    message['Subject'] = title
    message['From'] = from_addr
    message['To'] = ','.join(to_addrs)

    smtp = SMTP_SSL(
        host=mail_host,
        port=mail_port,
    )
    smtp.login(
        user=mail_user,
        password=mail_password,
    )
    smtp.sendmail(from_addr, to_addrs, message.as_string())
    logger.info('发送邮件成功')