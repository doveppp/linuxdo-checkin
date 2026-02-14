"""
cron: 0 */6 * * *
new Env("Linux.Do Cookie 签到")
"""

import os
import random
import time
from loguru import logger
from DrissionPage import ChromiumOptions, Chromium
from notify import NotificationManager

# 从 Secrets 获取 Cookie 值
COOKIE_T = os.environ.get("LINUXDO_COOKIE_T")
BROWSE_ENABLED = os.environ.get("BROWSE_ENABLED", "true").strip().lower() != "false"

class LinuxDoCookieBot:
    def __init__(self) -> None:
        co = ChromiumOptions()
        co.headless(True)
        co.set_argument("--no-sandbox")
        co.set_argument("--disable-gpu")
        # 模拟真实浏览器 User-Agent
        co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
        self.browser = Chromium(co)
        self.page = self.browser.new_tab()
        self.notifier = NotificationManager()

    def login_with_cookie(self):
        logger.info("正在尝试使用 Cookie 登录...")
        # 必须先访问一次域名才能注入该域名的 Cookie
        self.page.get("https://linux.do/")
        time.sleep(3)
        
        # 注入验证身份的关键 Cookie '_t'
        self.page.set.cookies({
            'name': '_t',
            'value': COOKIE_T,
            'domain': '.linux.do',
            'path': '/'
        })
        
        # 刷新页面以应用 Cookie
        self.page.refresh()
        time.sleep(5)
        
        # 检查是否成功看到用户头像
        if self.page.ele("@id=current-user", timeout=10):
            logger.success("✅ Cookie 登录验证成功！")
            return True
        else:
            logger.error("❌ 登录验证失败，Cookie 可能已失效或 LINUXDO_COOKIE_T 设置错误")
            # 打印当前页面标题辅助排查
            logger.info(f"当前页面标题: {self.page.title}")
            return False

    def browse_task(self):
        logger.info("开始模拟人工浏览...")
        # 确保回到首页
        self.page.get("https://linux.do/")
        time.sleep(3)
        
        # 提取帖子链接
        links = self.page.eles("tag:a")
        topic_urls = list(set([l.attr("href") for l in links if "/t/topic/" in (l.attr("href") or "")]))
        
        if not topic_urls:
            logger.warning("未能获取到帖子列表")
            return

        # 随机看 5 个贴
        selected = random.sample(topic_urls, min(len(topic_urls), 5))
        for url in selected:
            new_tab = self.browser.new_tab()
            try:
                new_tab.get(url)
                logger.info(f"正在看: {new_tab.title}")
                time.sleep(random.uniform(5, 10))
                # 随机向下滚动一下
                new_tab.run_js(f"window.scrollBy(0, {random.randint(400, 800)})")
            finally:
                new_tab.close()

    def run(self):
        try:
            if not COOKIE_T:
                logger.error("错误: 未在 Secrets 中发现 LINUXDO_COOKIE_T")
                return
            
            if self.login_with_cookie():
                if BROWSE_ENABLED:
                    self.browse_task()
                self.notifier.send_all("LINUX DO 助手", "✅ 签到及浏览任务已完成")
            else:
                self.notifier.send_all("LINUX DO 助手", "❌ 签到失败：身份令牌无效")
        finally:
            self.browser.quit()

if __name__ == "__main__":
    LinuxDoCookieBot().run()
