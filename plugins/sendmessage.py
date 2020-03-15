import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def load_image(path, cid):
    """
    :param path:文件所在路径，当前路径为与app.py同级,因此image路径为./image/***.png
    :type path:str
    :param cid:需要绑定的cid
    :type cid:str
    """
    data = open(path, 'rb')
    message_img = MIMEImage(data.read())
    data.close()

    # 给图片绑定cid，将来根据这个cid的值，找到标签内部对应的img标签。
    message_img.add_header('Content-ID', cid)

    # 返回MIMEImage的对象，将该对象放入message中
    return message_img

class EmailSina(object):

    def __init__(self,sender_mail='',receivers=['466370683@qq.com'],username="张宏",price="50",goodsid="F63S5D69CXA2X22C1D",sender_pass = ''):

        self.sender_mail = sender_mail
        # 邮箱提供的授权码，可在第三方登录，我这个是随便打的。
        self.sender_pass = sender_pass
        self.receivers = receivers# 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        self.username = username
        self.price = price
        self.gameprice = str(int(price)*25)+"点"
        self.goodsid = goodsid

    def sendEmail(self):
        # 1> 创建用于发送带有附件文件的邮件对象
        # related: 邮件内容的格式，采用内嵌的形式进行展示。
        message = MIMEMultipart('related')
        msg = MIMEText('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <div id="mailContentContainer" class="qmbox qm_con_body_content qqmail_webmail_only" style=""><div style="min-height:22px;margin-bottom:8px;"><br></div><div id="original-content"><div id="original-content"><br><div><div id="original-content"><div style="COLOR: #000"><div><table width="608" align="center" style="WIDTH: 608px; COLOR: rgb(0,0,0)" border="0" cellspacing="0">
        <tbody>
        <tr>
        <td width="338" height="40" rowspan="2"><img src="cid:image1" naturalh="42" naturalw="247"></td>
        <td width="270" height="16"></td></tr>
        <tr>
        <td width="270" height="24" style="TEXT-ALIGN: center; BACKGROUND-COLOR: rgb(235,242,250)">
        <div align="center"><b style="FONT-SIZE: 12px; COLOR: rgb(153,204,255); LINE-HEIGHT: 18px"><font face="Arial">请 及 时 查 收。</font></b><b><font face="Arial">　</font></b></div></td></tr></tbody></table>
        <table width="608" height="41" align="center" style="BORDER-TOP: rgb(235,242,250) 4px solid; BORDER-RIGHT: rgb(235,242,250) 4px solid; WIDTH: 608px; COLOR: rgb(0,0,0); BORDER-LEFT: rgb(235,242,250) 4px solid; BACKGROUND-COLOR: rgb(245,245,245)" border="0" cellspacing="0" cellpadding="0">
        <tbody>
        <tr>
        <td width="66%" style="FONT-SIZE: 12px; TEXT-ALIGN: center">
        <div class="copyright">
        <div class="Apple-style-span" style2="style2"><strong style="FONT-WEIGHT: normal">
        <div align="left"><strong><font color="#757774">[ 小 提 醒 ]</font></strong><font color="#757774">请 保 管 好 邮 件 ， 避 免 被 他 人 使 用 ，请 立 即 完 成。</font></div></strong></div></div></td></tr></tbody></table>
        <table width="608" height="583" align="center" style="BORDER-RIGHT: rgb(235,242,250) 4px solid; WIDTH: 608px; BORDER-BOTTOM: rgb(235,242,250) 8px solid; COLOR: rgb(0,0,0); BORDER-LEFT: rgb(235,242,250) 4px solid" cellspacing="0" cellpadding="0">
        <tbody>
        <tr>
        <td>
        <p align="center" style="TEXT-ALIGN: left"><img width="540" height="185" style="HEIGHT: 223px; WIDTH: 590px" src="cid:image2" naturalh="185" naturalw="537"></p>
        <div align="center" style="TEXT-ALIGN: left">
        <div align="left">
        <table width="99%" style="TEXT-ALIGN: left" bgcolor="#c9c9c9" border="0" cellspacing="1" cellpadding="1">
        <tbody>
        <tr>
        <td align="right" style="FONT-SIZE: 9pt" bgcolor="#f6f6f6">&nbsp;凭 证：</td>
        <td width="33%" style="FONT-SIZE: 9pt" bgcolor="#ffffff">'''+self.goodsid+'''</td>
        <td height="20" align="right" style="FONT-SIZE: 9pt" bgcolor="#f6f6f6">商 家：</td>
        <td width="36%" style="FONT-SIZE: 9pt" bgcolor="#ffffff"><font color="#000000">15GD22-95425S-5523S-A453SA</font></td></tr>
        <tr>
        <td align="right" style="FONT-SIZE: 9pt" bgcolor="#f6f6f6">&nbsp; &nbsp;&nbsp; 名 称：</td>
        <td width="33%" style="FONT-SIZE: 9pt" bgcolor="#ffffff"><font class="Apple-style-span" color="#ff0000">点 卡</font></td>
        <td height="20" align="right" style="FONT-SIZE: 9pt" bgcolor="#f6f6f6">数 量：</td>
        <td width="36%" bgcolor="#ffffff"><font color="#ff0000" size="2"><b>'''+self.gameprice+'''</b></font></td></tr>
        <tr>
        <td align="right" style="FONT-SIZE: 9pt" bgcolor="#f6f6f6">金 额：</td>
        <td width="33%" style="FONT-SIZE: 9pt" bgcolor="#ffffff"><font color="#ff0000"><b>'''+self.price+'''</b></font></td>
        <td height="20" align="right" style="FONT-SIZE: 9pt" bgcolor="#f6f6f6">&nbsp; &nbsp; &nbsp; &nbsp; 买 家：</td>
        <td width="36%" style="FONT-SIZE: 9pt" bgcolor="#ffffff">'''+self.username+'''</td></tr></tbody></table></div></div>
        <p align="center" style="FONT-SIZE: 12px"><a href="http://m1j6661168.iask.in/" rel="noopener" target="_blank"><img src="http://ae01.alicdn.com/kf/HTB1mqYPh_qWBKNjSZFA5janSpXaj.gif" naturalh="34" naturalw="136"></a></p>
        <p style="FONT-SIZE: 12px"><b><font class="Apple-style-span" color="#333333">手 机 刷 卡 器 大 团 购 还 送 价 值 最 高 1 8 8 的 大 礼 包</font></b></p>
        <p align="center" style="FONT-SIZE: 12px"><span><img src="cid:image3" naturalh="151" naturalw="601"></span></p></td></tr></tbody></table><br></div>
        <div><br></div></div></div></div></div></div><style type="text/css">.qmbox style, .qmbox script, .qmbox head, .qmbox link, .qmbox meta {display: none !important;}</style></div>
        </body>
        </html>
        ''','html','utf-8')

        message.attach(msg)
        # 向img标签中指定图片
        message.attach(load_image('./image/logo.png', 'image1'))
        message.attach(load_image('./image/test1.jpg', 'image2'))
        message.attach(load_image('./image/test2.jpg', 'image3'))

        message['From'] = self.sender_mail
        message['to'] = self.receivers[0]
        message['Subject'] = Header("50元点卡！请查收！",'utf-8').encode()

        # 绑定新浪服务器，默认25号端口
        sftp_obj =smtplib.SMTP('smtp.sina.com', 25)
        # 新浪授权登录
        sftp_obj.login(self.sender_mail, self.sender_pass)
        #三个参数分别是：发件人邮箱账号，收件人邮箱账号，发送的邮件体
        sftp_obj.sendmail(self.sender_mail, self.receivers, message.as_string())
        sftp_obj.quit()