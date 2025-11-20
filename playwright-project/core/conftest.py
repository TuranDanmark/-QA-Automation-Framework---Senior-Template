from core.environment import init_environment
import os
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from core.logger import logger
from core.config_loader import config
import allure

def pytest_configure(config):
    init_environment()

    if hasattr(config, "_metadata"):
        config._metadata["CI"] = os.getenv("CI", "false")
        config._metadata["ENV"] = os.getenv("TEST_ENV", "local")


# -----------------------
# CONFIG fixture (session)
# -----------------------
@pytest.fixture(scope="session")
def cfg():
    return config

# -----------------------
# Playwright instance
# -----------------------
@pytest.fixture(scope="session")
def playwright_instance():
    logger.info("▶ Start Playwright")
    with sync_playwright() as pw:
        yield pw
    logger.info("⏹ Playwright stopped")

# -----------------------
# Browser context (session)
# -----------------------
@pytest.fixture(scope="session")
def browser_context(playwright_instance, cfg):
    ui = cfg["ui"]
    browser = playwright_instance.chromium.launch(headless=ui.get("headless", True),
                                                  args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context(
        viewport={"width": 1600, "height": 900},
        record_video_dir="videos" if ui.get("record_video", False) else None,
        record_har_path="network.har" if ui.get("record_har", False) else None
    )
    yield context
    logger.info("Closing browser context")
    context.close()
    browser.close()

# -----------------------
# page fixture (function)
# -----------------------
@pytest.fixture()
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

# -----------------------
# Attach hooks: screenshots, video, HAR -> pytest-html & Allure
# -----------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # let pytest execute the actual test and get the report object
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    # initialize extras for pytest-html
    extra = getattr(rep, "extra", [])

    # If test failed: take screenshot + attach video/har if present
    if rep.failed:
        page = item.funcargs.get("page", None)

        if page:
            # create screens dir
            os.makedirs("screens", exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screens/{item.name}_{ts}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                logger.error(f"Saved screenshot: {screenshot_path}")

                # attach to pytest-html
                if item.config.pluginmanager.hasplugin("html"):
                    html = item.config.pluginmanager.getplugin("html")
                    extra.append(html.extras.png(screenshot_path))

                # attach to Allure
                try:
                    allure.attach.file(screenshot_path, name=item.name + "_screenshot", attachment_type=allure.attachment_type.PNG)
                except Exception:
                    pass

            except Exception as e:
                logger.exception("Failed to capture screenshot: %s", e)

            # video (Playwright)
            try:
                if page.video:
                    video_path = page.video.path()
                    if os.path.exists(video_path):
                        if item.config.pluginmanager.hasplugin("html"):
                            html = item.config.pluginmanager.getplugin("html")
                            extra.append(html.extras.url(video_path))
                        try:
                            allure.attach.file(video_path, name=item.name + "_video", attachment_type=allure.attachment_type.MP4)
                        except Exception:
                            pass
            except Exception:
                pass

        # attach HAR if exists
        try:
            if os.path.exists("network.har"):
                if item.config.pluginmanager.hasplugin("html"):
                    html = item.config.pluginmanager.getplugin("html")
                    extra.append(html.extras.text(open("network.har", "r", encoding="utf-8").read()))
                try:
                    allure.attach.file("network.har", name=item.name + "_network", attachment_type=allure.attachment_type.JSON)
                except Exception:
                    pass
        except Exception:
            pass

    rep.extra = extra

# -----------------------
# Add metadata to HTML report
# -----------------------
def pytest_configure(config):
    if not hasattr(config, "_metadata"):
        return
    config._metadata["Project"] = "QA Framework"
    config._metadata["Base URL ALIBABA"] = config._metadata.get("Base URL ALIBABA", config._metadata.get("Base URL ALIBABA", str(config)))
