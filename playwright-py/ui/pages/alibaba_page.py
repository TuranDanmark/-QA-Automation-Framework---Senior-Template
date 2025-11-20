from ui.pages.base_page import BasePage
from playwright.sync_api import expect

class AlibabaPage(BasePage):
    URL = "https://www.alibaba.com/"

    def open(self):
        self.goto(self.URL)

    def search(self, text):
        self.page.get_by_role("textbox", name="Search Alibaba").fill(text)
        self.page.get_by_role("button", name="Search", exact=True).click()

    def results_loaded(self):
        loc = self.page.locator("#sse-fluent-offerlist-ssr")
        expect(loc).to_be_visible()
        return loc.is_visible()
