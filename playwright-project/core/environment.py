import os
import platform
from datetime import datetime
from core.config_loader import config
from core.logger import logger


ENV_FILE = "reports/allure-results/environment.properties"
ALLURE_CATEGORIES = "reports/allure-results/categories.json"


def write_allure_environment():
    """Заполняем Allure environment.properties файлами."""
    os.makedirs("reports/allure-results", exist_ok=True)

    lines = [
        f"OS = {platform.system()} {platform.release()}",
        f"Python = {platform.python_version()}",
        f"Machine = {platform.machine()}",
        f"Run Timestamp = {datetime.now()}",
        "",
        "# UI settings",
        f"UI.BaseURL.Heroku = {config['ui']['base_url_heroku']}",
        f"UI.BaseURL.Alibaba = {config['ui']['base_url_alibaba']}",
        f"UI.Headless = {config['ui']['headless']}",
        "",
        "# API settings",
        f"API.BaseURL = {config['api']['base_url']}",
    ]

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info("✔ Allure environment.properties created")


def create_allure_categories():
    """Создаем categories.json для группировки падений."""
    categories = [
        {
            "name": "Authentication errors",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*(401|403).*"
        },
        {
            "name": "UI assertions",
            "matchedStatuses": ["failed"],
            "traceRegex": ".*AssertionError.*"
        },
        {
            "name": "Network/API issues",
            "matchedStatuses": ["broken"],
            "traceRegex": ".*ConnectionError.*"
        },
        {
            "name": "Unexpected errors",
            "matchedStatuses": ["failed", "broken"],
        }
    ]

    os.makedirs("reports/allure-results", exist_ok=True)
    import json
    with open(ALLURE_CATEGORIES, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=4)

    logger.info("✔ Allure categories.json created")


def init_environment():
    """
    Вызывается один раз при старте тестов.
    Создаёт environment.properties + categories.json.
    """
    write_allure_environment()
    create_allure_categories()
    logger.info("✔ Environment initialization completed")
