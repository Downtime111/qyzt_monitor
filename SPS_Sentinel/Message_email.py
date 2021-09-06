# -*- coding: UTF-8 -*-


"""
@描述：邮件发送模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-15
"""


import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import configparser

alarm_config = configparser.ConfigParser()


def send_email(msgRoot, sender, receivers, alarm_config):
    # alarm_config.read("./config/alarm_config.ini", encoding="utf-8")
    email_host = alarm_config["email"]['email_host']
    email_port = alarm_config["email"]['email_port']
    passwd = alarm_config["email"]["passwd"]
    try:
        smtpObj = smtplib.SMTP_SSL(email_host, email_port)
        smtpObj.login(sender, passwd)
        smtpObj.sendmail(sender, receivers, msgRoot.as_string())
        smtpObj.quit()  # 关闭连接
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def run_alarm_email(title, content_dic):
    alarm_config.read("./config/alarm_config.ini", encoding="utf-8")
    sender = alarm_config["email"]['sender']
    receivers = eval(alarm_config["email"]['receivers'])

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = formataddr(("旗云报警邮箱", sender))
    msgRoot['To'] = formataddr(("接收邮箱", ";".join(receivers)))
    # msgRoot['To'] = receivers
    msgRoot['Subject'] = title

    out = ''
    for key in content_dic:
        out = out + f"<span style=\"font-family: SimKai;\">设备【{key}】昨日记录【{str(content_dic[key])}】条</span><br />"
    mail_msg = get_page(title,out)

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    # with open('./img/test.jpg', 'rb') as fp:
    #     msgImage = MIMEImage(fp.read())
    # msgImage.add_header('Content-ID', '<image1>')
    # msgRoot.attach(msgImage)
    send_email(msgRoot, sender, receivers, alarm_config)


def get_page(title, content):
    mail_msg = """
    <meta charset="utf-8">
    <table width="100%">
        <tr>
            <td style="width: 100%;">
                <center>
                    <table class="content-wrap" style="margin: 0px auto; width: 600px;">
                        <tr>
                            <td style="margin: 0px auto; overflow: hidden; padding: 0px; border: 0px dotted rgb(238, 238, 238);">
                                <!---->
                                <div class="full" tindex="1" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="fullTable"
                                           style="width: 600px;">
                                        <tbody>
                                        <tr>
                                            <td class="fullTd"
                                                style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top;">
                                                <div style="display: inline-block; vertical-align: top; width: 100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                           style="vertical-align: top;">
                                                        <tr>
                                                            <td style="font-size: 0px; word-break: break-word; width: 600px; text-align: center; padding: 10px 0px;">
                                                                <div><img height="auto" alt="5" width="600"
                                                                          src="https://www.drageasy.com/1ade793a56dabae7b8a97fded12d2806.png?imageslim"
                                                                          style="box-sizing: border-box; border: 0px; display: inline-block; outline: none; text-decoration: none; height: auto; max-width: 100%; padding: 0px;">
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div tindex="2" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0"
                                           style="background-color: rgb(255, 255, 255); background-image: url(&quot;&quot;); background-repeat: no-repeat; background-size: 100px; background-position: 1% 50%;">
                                        <tbody>
                                        <tr>
                                            <td style="direction: ltr; font-size: 0px; text-align: center; vertical-align: top; width: 600px;">
                                                <table width="100%" border="0" cellpadding="0" cellspacing="0"
                                                       style="vertical-align: top;">
                                                    <tbody>
                                                    <tr>
                                                        <td class="oneColumn column1"
                                                            style="width: 100%; max-width: 100%; min-height: 1px; font-size: 13px; text-align: left; direction: ltr; vertical-align: top; padding: 0px;">
                                                            <div columnnumber="1">
                                                                <table align="center" border="0" cellpadding="0"
                                                                       cellspacing="0" style="width: 100%;">
                                                                    <tbody>
                                                                    <tr>
                                                                        <td style="direction: ltr; font-size: 0px; text-align: center; vertical-align: top; border: 0px;">
                                                                            <div class="mj-column-per-50"
                                                                                 style="width: 100%; max-width: 100%; font-size: 13px; text-align: left; direction: ltr; display: inline-block; vertical-align: top;">
                                                                                <table border="0" cellpadding="0"
                                                                                       cellspacing="0" width="100%"
                                                                                       style="border-collapse: collapse; border-spacing: 0px; width: 100%; vertical-align: top;">
                                                                                    <tr>
                                                                                        <td align="center" border="0"
                                                                                            style="font-size: 0px; word-break: break-word;">
                                                                                            <div class="full"
                                                                                                 style="margin: 0px auto; max-width: 600px;">
                                                                                                <table align="center"
                                                                                                       border="0"
                                                                                                       cellpadding="0"
                                                                                                       cellspacing="0"
                                                                                                       class="fullTable"
                                                                                                       style="width: 600px;">
                                                                                                    <tbody>
                                                                                                    <tr>
                                                                                                        <td class="fullTd"
                                                                                                            style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top; background-image: url(&quot;&quot;); background-repeat: no-repeat; background-size: 100px; background-position: 10% 50%;">
                                                                                                            <table border="0"
                                                                                                                   cellpadding="0"
                                                                                                                   cellspacing="0"
                                                                                                                   width="100%"
                                                                                                                   style="vertical-align: top;">
                                                                                                                <tr>
                                                                                                                    <td align="left"
                                                                                                                        style="font-size: 0px; padding: 8px 20px;">
                                                                                                                        <div class="text"
                                                                                                                             style="font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; overflow-wrap: break-word; margin: 0px; text-align: center; line-height: 20px; color: rgb(51, 51, 51); font-size: 14px; font-weight: bolder;">
                                                                                                                            <div>
                                                                                                                                <h2 style="line-height: 36px; font-size: 1.5em; font-weight: bold; margin: 0px;">
                                                                                                                                {title}
                                                                                                                                </h2>
                                                                                                                            </div>
                                                                                                                        </div>
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </div>
                                                                                        </td>
                                                                                    </tr>
                                                                                </table>
                                                                            </div>
                                                                            <div class="mj-column-per-50"
                                                                                 style="width: 100%; max-width: 100%; font-size: 13px; text-align: left; direction: ltr; display: inline-block; vertical-align: top;">
                                                                                <table border="0" cellpadding="0"
                                                                                       cellspacing="0" width="100%"
                                                                                       style="border-collapse: collapse; border-spacing: 0px; width: 100%; vertical-align: top;">
                                                                                    <tr>
                                                                                        <td align="center" border="0"
                                                                                            style="font-size: 0px; word-break: break-word;">
                                                                                            <div class="full"
                                                                                                 style="margin: 0px auto; max-width: 600px;">
                                                                                                <table align="center"
                                                                                                       border="0"
                                                                                                       cellpadding="0"
                                                                                                       cellspacing="0"
                                                                                                       class="fullTable"
                                                                                                       style="width: 600px;">
                                                                                                    <tbody>
                                                                                                    <tr>
                                                                                                        <td class="fullTd"
                                                                                                            style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top; background-image: url(&quot;&quot;); background-repeat: no-repeat; background-size: 100px; background-position: 10% 50%;">
                                                                                                            <table border="0"
                                                                                                                   cellpadding="0"
                                                                                                                   cellspacing="0"
                                                                                                                   width="100%"
                                                                                                                   style="vertical-align: top;">
                                                                                                                <tr>
                                                                                                                    <td align="left"
                                                                                                                        style="font-size: 0px; padding: 0px 15px 15px;">
                                                                                                                        <div class="text"
                                                                                                                             style="font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; overflow-wrap: break-word; margin: 0px; text-align: center; line-height: 24px; color: rgb(99, 99, 99); font-size: 14px; font-weight: normal;">
                                                                                                                            <div>
                                                                                                                                <p style="text-size-adjust: none; word-break: break-word; line-height: 24px; font-size: 14px; margin: 0px;">
                                                                                                                                    <span style="font-family: SimKai;">下发时间：{time}</span>
                                                                                                                                </p>
                                                                                                                            </div>
                                                                                                                        </div>
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </table>
                                                                                                        </td>
                                                                                                    </tr>
                                                                                                    </tbody>
                                                                                                </table>
                                                                                            </div>
                                                                                        </td>
                                                                                    </tr>
                                                                                </table>
                                                                            </div>
                                                                        </td>
                                                                    </tr>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="full" tindex="3" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="fullTable"
                                           style="width: 600px;">
                                        <tbody>
                                        <tr>
                                            <td class="fullTd"
                                                style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top; background-image: url(&quot;&quot;); background-repeat: no-repeat; background-size: 100px; background-position: 10% 50%;">
                                                <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                       style="vertical-align: top;">
                                                    <tr>
                                                        <td align="left" style="font-size: 0px; padding: 20px;">
                                                            <div class="text"
                                                                 style="font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; overflow-wrap: break-word; margin: 0px; text-align: left; line-height: 1.6; color: rgb(0, 0, 0); font-size: 14px; font-weight: normal;">
                                                                <div>
                                                                    <p style="text-size-adjust: none; word-break: break-word; line-height: 1.6; font-size: 14px; margin: 0px;">
                                                                        <span style="font-family: SimKai;">
                                                                            {content}
                                                                        </span>
                                                                    </p></div>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="full" tindex="4" style="margin: 0px auto; max-width: 600px;">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" class="fullTable"
                                           style="width: 600px;">
                                        <tbody>
                                        <tr>
                                            <td class="fullTd"
                                                style="direction: ltr; width: 600px; font-size: 0px; padding-bottom: 0px; text-align: center; vertical-align: top;">
                                                <div style="display: inline-block; vertical-align: top; width: 100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%"
                                                           style="vertical-align: top;">
                                                        <tr>
                                                            <td style="font-size: 0px; word-break: break-word; width: 600px; text-align: center; padding: 10px 0px;">
                                                                <div><img height="auto" alt="7" width="600"
                                                                          src="https://www.drageasy.com/6e95e11f76ce8d76f0fcbfedac9dffe2.png?imageslim"
                                                                          style="box-sizing: border-box; border: 0px; display: inline-block; outline: none; text-decoration: none; height: auto; max-width: 100%; padding: 0px;">
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </table>
                </center>
            </td>
        </tr>
    </table><!---->
    <center style="text-align:center;font-size: 12px;margin:5px;color:rgb(102, 102, 102);transform: scale(.9);-webkit-transform: scale(.9);">
        旗云中天科技有限公司
    </center>""".format(
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        content=content,
        title=title
    )
    return mail_msg


if __name__ == '__main__':
    title = '报警测试邮件'
    device = 'test'
    run_alarm_email(title, device)
