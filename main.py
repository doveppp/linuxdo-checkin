import os
import time
import random
from playwright.sync_api import sync_playwright


USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


HOME_URL = "https://linux.do/"


class LinuxDoBrowser:
    def __init__(self) -> None:
        self.pw = sync_playwright().start()
        self.browser = self.pw.firefox.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto(HOME_URL)

    def login(self):
        self.page.click(".header-buttons .d-button-label")
        time.sleep(2)
        self.page.fill("#login-account-name", USERNAME)
        time.sleep(2)
        self.page.fill("#login-account-password", PASSWORD)
        time.sleep(2)
        self.page.click("#login-button")
        time.sleep(30)
        user_ele = self.page.query_selector("#current-user")
        if not user_ele:
            print("Login failed")
            return False
        else:
            print("Check in success")
            return True

    def click_topic(self):
        for topic in self.page.query_selector_all("#list-area .title"):
            page = self.context.new_page()
            page.goto(HOME_URL + topic.get_attribute("href"))
            if random.random() < 0.02:  # 100 * 0.02 * 30 = 60
                self.click_like(page)
            time.sleep(10)
            page.close()

    def run(self):
        if not self.login():
            return
        self.click_topic()

    def click_like(self, page):
        page.locator(".discourse-reactions-reaction-button").first.click()
        print("Like success")


if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("Please set USERNAME and PASSWORD")
        exit(1)
    l = LinuxDoBrowser()
    l.run()
