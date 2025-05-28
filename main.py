"""
cron: 0 */6 * * *
new Env("Linux.Do 签到")
"""

import os
import random
import time
import functools
import sys
import requests
import re
from loguru import logger
from DrissionPage import ChromiumOptions, Chromium
from tabulate import tabulate


def retry_decorator(retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:  # 最后一次尝试
                        logger.error(f"函数 {func.__name__} 最终执行失败: {str(e)}")
                    logger.warning(
                        f"函数 {func.__name__} 第 {attempt + 1}/{retries} 次尝试失败: {str(e)}"
                    )
                    time.sleep(1)
            return None

        return wrapper

    return decorator


os.environ.pop("DISPLAY", None)
os.environ.pop("DYLD_LIBRARY_PATH", None)

USERNAME = os.environ.get("LINUXDO_USERNAME")
PASSWORD = os.environ.get("LINUXDO_PASSWORD")
BROWSE_ENABLED = os.environ.get("BROWSE_ENABLED", "true").strip().lower() not in [
    "false",
    "0",
    "off",
]
if not USERNAME:
    USERNAME = os.environ.get("USERNAME")
if not PASSWORD:
    PASSWORD = os.environ.get("PASSWORD")
GOTIFY_URL = os.environ.get("GOTIFY_URL")  # Gotify 服务器地址
GOTIFY_TOKEN = os.environ.get("GOTIFY_TOKEN")  # Gotify 应用的 API Token
SC3_PUSH_KEY = os.environ.get("SC3_PUSH_KEY")  # Server酱³ SendKey

HOME_URL = "https://linux.do/"
LOGIN_URL = "https://linux.do/login"


class LinuxDoBrowser:
    def __init__(self) -> None:
        EXTENSION_PATH = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "turnstilePatch")
        )
        from sys import platform

        if platform == "linux" or platform == "linux2":
            platformIdentifier = "X11; Linux x86_64"
        elif platform == "darwin":
            platformIdentifier = "Macintosh; Intel Mac OS X 10_15_7"
        elif platform == "win32":
            platformIdentifier = "Windows NT 10.0; Win64; x64"

        co = (
            ChromiumOptions()
            .headless(True)
            .add_extension(EXTENSION_PATH)
            .incognito(True)
            .set_argument("--no-sandbox")
        )
        co.set_user_agent(
            f"Mozilla/5.0 ({platformIdentifier}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )
        self.browser = Chromium(co)
        self.page = self.browser.new_tab()

    def getTurnstileToken(self):
        self.page.run_js("try { turnstile.reset() } catch(e) { }")

        turnstileResponse = None

        for i in range(0, 5):
            try:
                turnstileResponse = self.page.run_js(
                    "try { return turnstile.getResponse() } catch(e) { return null }"
                )
                if turnstileResponse:
                    return turnstileResponse

                challengeSolution = self.page.ele("@name=cf-turnstile-response")
                challengeWrapper = challengeSolution.parent()
                challengeIframe = challengeWrapper.shadow_root.ele("tag:iframe")
                challengeIframeBody = challengeIframe.ele("tag:body").shadow_root
                challengeButton = challengeIframeBody.ele("tag:input")
                challengeButton.click()
            except Exception as e:
                logger.warning(f"处理 Turnstile 时出错: {str(e)}")
            time.sleep(1)
        # self.page.refresh()
        # raise Exception("failed to solve turnstile")

    def login(self):
        logger.info("开始登录")
        self.page.get(LOGIN_URL)
        time.sleep(2)
        turnstile_token = self.getTurnstileToken()
        logger.info(f"turnstile_token: {turnstile_token}")
        self.page.get_screenshot("screenshot.png")
        self.page.ele("@id=login-account-name").input(USERNAME)
        self.page.ele("@id=login-account-password").input(PASSWORD)
        self.page.ele("@id=login-button").click()
        time.sleep(10)
        user_ele = self.page.ele("@id=current-user")
        if not user_ele:
            logger.error("登录失败")
            return False
        else:
            logger.info("登录成功")
            return True

    def click_topic(self):
        topic_list = self.page.ele("@id=list-area").eles(".:title")
        logger.info(f"发现 {len(topic_list)} 个主题帖，随机选择10个")
        for topic in random.sample(topic_list, 10):
            self.click_one_topic(topic.attr("href"))

    @retry_decorator()
    def click_one_topic(self, topic_url):
        new_page = self.browser.new_tab()
        new_page.get(topic_url)
        if random.random() < 0.3:  # 0.3 * 30 = 9
            self.click_like(new_page)
        self.browse_post(new_page)
        new_page.close()

    def browse_post(self, page):
        prev_url = None
        # 开始自动滚动，最多滚动10次
        for _ in range(10):
            # 随机滚动一段距离
            scroll_distance = random.randint(550, 650)  # 随机滚动 550-650 像素
            logger.info(f"向下滚动 {scroll_distance} 像素...")
            page.run_js(f"window.scrollBy(0, {scroll_distance})")
            logger.info(f"已加载页面: {page.url}")

            if random.random() < 0.03:  # 33 * 4 = 132
                logger.success("随机退出浏览")
                break

            # 检查是否到达页面底部
            at_bottom = page.run_js(
                "window.scrollY + window.innerHeight >= document.body.scrollHeight"
            )
            current_url = page.url
            if current_url != prev_url:
                prev_url = current_url
            elif at_bottom and prev_url == current_url:
                logger.success("已到达页面底部，退出浏览")
                break

            # 动态随机等待
            wait_time = random.uniform(2, 4)  # 随机等待 2-4 秒
            logger.info(f"等待 {wait_time:.2f} 秒...")
            time.sleep(wait_time)

    def run(self):
        if not self.login():  # 登录
            logger.error("登录失败，程序终止")
            sys.exit(1)  # 使用非零退出码终止整个程序

        if BROWSE_ENABLED:
            self.click_topic()  # 点击主题
            logger.info("完成浏览任务")

        self.print_connect_info()  # 打印连接信息
        self.send_notifications(BROWSE_ENABLED)  # 发送通知
        self.page.close()
        self.browser.quit()

    def click_like(self, page):
        try:
            # 专门查找未点赞的按钮
            like_button = page.ele(".discourse-reactions-reaction-button")
            if like_button:
                logger.info("找到未点赞的帖子，准备点赞")
                like_button.click()
                logger.info("点赞成功")
                time.sleep(random.uniform(1, 2))
            else:
                logger.info("帖子可能已经点过赞了")
        except Exception as e:
            logger.error(f"点赞失败: {str(e)}")

    def print_connect_info(self):
        logger.info("获取连接信息")
        page = self.browser.new_tab()
        page.get("https://connect.linux.do/")
        rows = page.ele("tag:table").eles("tag:tr")

        info = []

        for row in rows:
            cells = row.eles("tag:td")
            if len(cells) >= 3:
                project = cells[0].text.strip()
                current = cells[1].text.strip()
                requirement = cells[2].text.strip()
                info.append([project, current, requirement])

        print("--------------Connect Info-----------------")
        print(tabulate(info, headers=["项目", "当前", "要求"], tablefmt="pretty"))

        page.close()

    def send_notifications(self, browse_enabled):
        status_msg = "✅每日登录成功"
        if browse_enabled:
            status_msg += " + 浏览任务完成"

        if GOTIFY_URL and GOTIFY_TOKEN:
            try:
                response = requests.post(
                    f"{GOTIFY_URL}/message",
                    params={"token": GOTIFY_TOKEN},
                    json={"title": "LINUX DO", "message": status_msg, "priority": 1},
                    timeout=10,
                )
                response.raise_for_status()
                logger.success("消息已推送至Gotify")
            except Exception as e:
                logger.error(f"Gotify推送失败: {str(e)}")
        else:
            logger.info("未配置Gotify环境变量，跳过通知发送")

        if SC3_PUSH_KEY:
            match = re.match(r"sct(\d+)t", SC3_PUSH_KEY, re.I)
            if not match:
                logger.error(
                    "❌ SC3_PUSH_KEY格式错误，未获取到UID，无法使用Server酱³推送"
                )
                return

            uid = match.group(1)
            url = f"https://{uid}.push.ft07.com/send/{SC3_PUSH_KEY}"
            params = {"title": "LINUX DO", "desp": status_msg}

            attempts = 5
            for attempt in range(attempts):
                try:
                    response = requests.get(url, params=params, timeout=10)
                    response.raise_for_status()
                    logger.success(f"Server酱³推送成功: {response.text}")
                    break
                except Exception as e:
                    logger.error(f"Server酱³推送失败: {str(e)}")
                    if attempt < attempts - 1:
                        sleep_time = random.randint(180, 360)
                        logger.info(f"将在 {sleep_time} 秒后重试...")
                        time.sleep(sleep_time)


if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("Please set USERNAME and PASSWORD")
        exit(1)
    l = LinuxDoBrowser()
    l.run()
