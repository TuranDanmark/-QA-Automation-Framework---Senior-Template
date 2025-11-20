from playwright.sync_api import expect

class BasePage:
    def __init__(self, page):
        self.page = page

    def goto(self, url):
        self.page.goto(url)

    def click(self, locator):
        self.page.locator(locator).click()

    def fill(self, locator, text):
        self.page.locator(locator).fill(text)

    def should_contain(self, locator, text):
        expect(self.page.locator(locator)).to_contain_text(text)
