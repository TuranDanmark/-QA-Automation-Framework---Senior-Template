from ui.pages.login_page import LoginPage
from playwright.sync_api import expect

def test_login_success(page):
    login = LoginPage(page)
    login.open()
    login.login("tomsmith", "SuperSecretPassword!")
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")
