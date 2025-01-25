import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件配置
smtp_server = 'smtp.126.com'
smtp_port = 465
smtp_username = 'microkbcrt@126.com'  # 明文存储发件邮箱
smtp_password = 'FCyttuJCVDNydXL8'  # 明文存储授权码
recipient_emails = ['1811838153@qq.com', '605936513@qq.com', 'bawuban001@outlook.com', '3034246584@qq.com', '2139693400@qq.com', '1354433744@qq.com']  # 收件人邮箱列表

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        print(f"邮件 '{subject}' 发送成功！")
    except Exception as e:
        print(f"发送邮件时出错：{str(e)}")
    finally:
        server.quit()

def main():
    try:
        url = 'http://www.tqyb.com.cn/gz/weatherForecast/tenForecast/'
        response = requests.get(url)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        iframes = soup.find_all('iframe', src=re.compile(r'/data/ten/.*'))

        for iframe in iframes:
            iframe_url = 'http://www.tqyb.com.cn' + iframe['src']
            iframe_response = requests.get(iframe_url)
            iframe_response.encoding = 'utf-8'
            iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')

            for head in iframe_soup.find_all('head'):
                head.decompose()

            text_content = iframe_soup.get_text(separator='\n', strip=True)

            last_timestamp = ''
            try:
                with open('tenForecast.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if lines:
                        last_timestamp = lines[-1].strip()
            except FileNotFoundError:
                pass

            current_timestamp = re.search(r'\d{4}年\d{2}月\d{2}日\d{2}时', text_content)
            if current_timestamp and current_timestamp.group(0) != last_timestamp:
                with open('tenForecast.txt', 'w', encoding='utf-8') as file:
                    file.write(text_content)

                send_email('天气预报更新通知', text_content)
                last_timestamp = current_timestamp.group(0)

    except Exception as e:
        print(f"处理时出错：{str(e)}")

if __name__ == '__main__':
    main()
