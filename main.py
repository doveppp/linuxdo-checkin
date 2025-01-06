import os
import random
import time
from functools import wraps

from loguru import logger
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from tabulate import tabulate

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PlaywrightTimeout:
            logger.error(f"操作超时: {func.__name__}")
        except Exception as e:
            logger.error(f"执行 {func.__name__} 时发生错误: {str(e)}")
        return None
    return wrapper

os.environ.pop("DISPLAY", None)
os.environ.pop("DYLD_LIBRARY_PATH", None)

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

HOME_URL = "https://linux.do/"


class LinuxDoBrowser:
    def __init__(self) -> None:
        try:
            self.pw = sync_playwright().start()
            self.browser = self.pw.firefox.launch(headless=True, timeout=30000)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(HOME_URL)
        except Exception as e:
            logger.error(f"初始化浏览器失败: {str(e)}")
            self.cleanup()
            raise

    def cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'context'):
                self.context.close()
            if hasattr(self, 'browser'):
                self.browser.close()
            if hasattr(self, 'pw'):
                self.pw.stop()
        except Exception as e:
            logger.error(f"清理资源时发生错误: {str(e)}")

    @handle_exceptions
    def login(self):
        logger.info("开始登录")
        try:
            self.page.click(".login-button .d-button-label")
            time.sleep(2)
            self.page.fill("#login-account-name", USERNAME)
            time.sleep(2)
            self.page.fill("#login-account-password", PASSWORD)
            time.sleep(2)
            self.page.click("#login-button")
            time.sleep(10)
            user_ele = self.page.query_selector("#current-user")
            if not user_ele:
                logger.error("登录失败")
                return False
            logger.info("登录成功")
            return True
        except Exception as e:
            logger.error(f"登录过程发生错误: {str(e)}")
            return False

    @handle_exceptions
    def click_topic(self):
        try:
            topic_list = self.page.query_selector_all("#list-area .title")
            logger.info(f"发现 {len(topic_list)} 个主题")
            for topic in topic_list:
                try:
                    href = topic.get_attribute("href")
                    if not href:
                        continue
                    logger.info(f"点击主题: {href}")
                    page = self.context.new_page()
                    page.goto(HOME_URL + href)
                    if random.random() < 0.3:
                        self.click_like(page)
                    self.browse_post(page)
                    page.close()
                except Exception as e:
                    logger.error(f"处理主题时发生错误: {str(e)}")
                    continue
        except Exception as e:
            logger.error(f"获取主题列表失败: {str(e)}")

    def browse_post(self, page):
        prev_url = None
        # 开始自动滚动，最多滚动10次
        for _ in range(10):
            # 随机滚动一段距离
            scroll_distance = random.randint(550, 650)  # 随机滚动 550-650 像素
            logger.info(f"Scrolling down by {scroll_distance} pixels...")
            page.evaluate(f"window.scrollBy(0, {scroll_distance})")
            logger.info(f"Loaded: {page.url}")

            if random.random() < 0.03:  # 33 * 4 = 132
                logger.success("Randomly exit")
                break

            # 检查是否到达页面底部
            at_bottom = page.evaluate("window.scrollY + window.innerHeight >= document.body.scrollHeight")
            current_url = page.url
            if current_url != prev_url:
                prev_url = current_url
            elif at_bottom and prev_url == current_url:
                logger.success("Reached the bottom of the page. Exiting.")
                break

            # 动态随机等待
            wait_time = random.uniform(2, 4)  # 随机等待 2-4 秒
            logger.info(f"Waiting for {wait_time:.2f} seconds...")
            time.sleep(wait_time)

    def run(self):
        try:
            if not self.login():
                return
            self.click_topic()
            self.print_connect_info()
        except Exception as e:
            logger.error(f"运行过程发生错误: {str(e)}")
        finally:
            self.cleanup()

    def click_like(self, page):
        try:
            # 专门查找未点赞的按钮
            like_button = page.locator('.discourse-reactions-reaction-button[title="点赞此帖子"]').first
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
        logger.info("Print connect info")
        page = self.context.new_page()
        page.goto("https://connect.linux.do/")
        rows = page.query_selector_all("table tr")

        info = []

        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) >= 3:
                project = cells[0].text_content().strip()
                current = cells[1].text_content().strip()
                requirement = cells[2].text_content().strip()
                info.append([project, current, requirement])

        print("--------------Connect Info-----------------")
        print(tabulate(info, headers=["项目", "当前", "要求"], tablefmt="pretty"))

        page.close()


if __name__ == "__main__":
    try:
        if not USERNAME or not PASSWORD:
            logger.error("请设置 USERNAME 和 PASSWORD 环境变量")
            exit(1)
        l = LinuxDoBrowser()
        l.run()
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        exit(1)
