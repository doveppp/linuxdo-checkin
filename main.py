import os
import json
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from DrissionPage import ChromiumPage, ChromiumOptions

def options_default():
    """设置无头浏览器的选项。"""
    co = ChromiumOptions()
    co.headless(True)  # 无头模式
    co.incognito(True)  # 无痕模式
    return co

def login(email, password):
    """使用 Gmail 登录 ChatGPT，并返回 accessToken。"""
    options = options_default()
    page = ChromiumPage(options)

    try:
        page.get('https://chat.openai.com')
        time.sleep(2)

        # 输入 Gmail 和密码
        email_input = page.ele('#email-input')
        email_input.input(email)
        page.ele('.continue-btn').click()

        time.sleep(2)

        password_input = page.ele('#password')
        password_input.input(password)
        page.ele('@name=action').click()

        time.sleep(2)

        # 获取 accessToken
        page.get('https://chat.openai.com/api/auth/session')
        data = json.loads(page.ele('tag:pre').text)
        return data.get("accessToken")

    except Exception as e:
        print(f"登录失败: {e}")
    finally:
        page.close()
    return None

def send_email(tokens):
    """使用腾讯邮箱发送 accessToken。"""
    sender = os.getenv('EMAIL_USERNAME')
    password = os.getenv('EMAIL_PASSWORD')
    recipient = os.getenv('RECIPIENT_EMAIL')

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Weekly Access Tokens'

    body = '\n'.join(tokens)
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.qq.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == '__main__':
    accounts = os.getenv('ACCOUNTS').splitlines()
    tokens = []

    # 遍历所有账号并获取 accessToken
    for account in accounts:
        email, password = account.split(':')
        token = login(email, password)
        if token:
            tokens.append(f"{email}: {token}")

    # 如果成功获取 token，发送邮件
    if tokens:
        send_email(tokens)
