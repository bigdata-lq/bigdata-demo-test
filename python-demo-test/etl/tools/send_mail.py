# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:lq
# Message: 邮件相关
# 功能点：生成html, 生成xlsx,
#-------------------------------------------------------------------------------
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
from etl.settings import mail_settings as mail
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication


class AldMail(object):

    @staticmethod
    def __instant_email(subject, text, receivers=list(), *args, **kwargs):
        msgRoot = MIMEMultipart('related')
        # 指定图片为当前目录
        msgRoot['From'] = mail["sender"]
        msgRoot['To'] = ",".join(receivers)
        msgRoot['Subject'] = Header(subject, 'utf-8')
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgAlternative.attach(MIMEText(text, 'html', 'utf-8'))
        if "img" in kwargs:
            for img in kwargs["img"]:
                f = open("../temp/"+img, 'rb')
                data = f.read()
                f.close()
                os.remove("../temp/"+img)
                msgImage = MIMEImage(data)
                # 定义图片 ID，在 HTML 文本中引用
                msgImage.add_header('Content-ID', '<{}>'.format(img))
                msgRoot.attach(msgImage)
        if "xlsx" in kwargs:
            xlsx = kwargs["xlsx"]
            for x, df in xlsx.items():
                if not x.endswith(".xlsx"):
                    x += ".xlsx"
                df.to_excel(x, index=False)
                f = open(x, "rb")
                data = f.read()
                f.close()
                temp = MIMEApplication(data)
                temp.add_header("content-disposition", "attachment", filename=("gbk", "", x))
                msgRoot.attach(temp)
                os.remove(x)
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail["mail_host"], 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail["mail_user"], mail["mail_pass"])
        smtpObj.sendmail(mail["sender"], receivers, msgRoot.as_string())

    @staticmethod
    def send_mail(subject, text, receivers=None, *args, **kwargs):
        receivers += mail["receivers"]
        receivers = list(set(receivers))
        print(receivers)
        if receivers:
            AldMail.__instant_email(subject, text, receivers=receivers, *args, **kwargs)
            print("邮件发送成功")
        else:
            print("还未添加发送人")

    @staticmethod
    def generate_html(subject, df, ordinal=True):
        """根据df生成html"""
        columns = df.columns.values.tolist()
        if ordinal:
            titles = """<td width="50" align="center">序号</td>"""
        else:
            titles = ""
        for i in columns:
            titles += """<td width="50" align="center">{}</td>""".format(i)

        contents = ""
        for i in range(len(df)):
            if ordinal:
                temp = """<tr><td width="75"align="center">{}</td>""".format(i+1)
            else:
                temp = ""
            for j in df.iloc[i]:
                temp += '<td width="75"align="center">{}</td>'.format(j)
            temp += "</tr>"
            contents += temp
        html = """
                       <div id="container">
                       <p><h2>{subject}</h2></p>
                       <div id="content">
                        <table width="80%" border="2" bordercolor="black" cellspacing="0" cellpadding="0">
                       <tr>
                         {title}
                       </tr>
                       {content}
                       </table>
                       </div>
                       """.format(subject=subject, title=titles, content=contents)
        return html

    @staticmethod
    def final_html(*args, **kwargs):
        html = ""
        for i in args:
            if i.endswith(("jpg", "png")):
                i = "<img src=cid:{}>".format(i)
            html += "<div>{}</div>".format(i)
        html = "<html></body>{}<body></html>".format(html)
        return html

    def __str__(self):
        return "数据报表基础类"
