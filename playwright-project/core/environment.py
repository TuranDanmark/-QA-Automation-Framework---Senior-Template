import os
import platform
import subprocess
import json
from datetime import datetime
from core.logger import logger
from core.config_loader import config


ENV_DIR = "reports/allure-results"
ENV_FILE = f"{ENV_DIR}/environment.properties"
CATEGORIES_FILE = f"{ENV_DIR}/categories.json"


# -----------------------------------------------
# Получение версии Playwright
# -----------------------------------------------
def get_playwright_version():
    try:
        result = subprocess.check_output(["playwright", "--version"], text=True)
        return result.strip()
    except:
        return "unknown"


# -----------------------------------------------
# Получение версии браузера Chromium
# -----------------------------------------------
def get_browser_version():
    try:
        result = subprocess.check_output(
            ["playwright", "install", "chromium"], text=True
        )
        return "Chromium (installed)"
    except:
        return "unknown"


# -----------------------------------------------
# ENV Variables System (CI/CD, local, staging…)
# -----------------------------------------------
def load_dynamic_env():
    return {
        "ENV": os.getenv("TEST_ENV", "local"),
        "CI": os.getenv("CI", "false"),
        "GITHUB_RUN_ID": os.getenv("GITHUB_RUN_ID", ""),
        "GITHUB_SHA": os.getenv("GITHUB_SHA", ""),
        "JENKINS_BUILD": os.getenv("BUILD_NUMBER", ""),
        "JENKINS_JOB": os.getenv("JOB_NAME", ""),
        "ALLURE_TOKEN": os.getenv("ALLURE_TOKEN", ""),
        "ALLURE_PROJECT_ID": os.getenv("ALLURE_PROJECT_ID", ""),
    }


# -----------------------------------------------
# Generate Allure environment.properties
# -----------------------------------------------
def write_allure_environment():
    os.makedirs(ENV_DIR, exist_ok=True)

    dynamic_env = load_dynamic_env()

    lines = [
        "### SYSTEM ENVIRONMENT ###",
        f"OS = {platform.system()} {platform.release()}",
        f"Python = {platform.python_version()}",
        f"Machine = {platform.machine()}",
        f"Run Timestamp = {datetime.now()}",
        "",
        "### PLAYWRIGHT ###",
        f"Playwright = {get_playwright_version()}",
        f"Browser Version = {get_browser_version()}",
        "",
        "### UI SETTINGS ###",
        f"UI.Headless = {config['ui']['headless']}",
        f"UI.BaseURL.Alibaba = {config['ui']['base_url_alibaba']}",
        f"UI.BaseURL.Heroku = {config['ui']['base_url_heroku']}",
        "",
        "### API SETTINGS ###",
        f"API.BaseURL = {config['api']['base_url']}",
        "",
        "### DYNAMIC ENVIRONMENT ###",
    ]

    for key, value in dynamic_env.items():
        lines.append(f"{key} = {value}")

    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info("✔ Allure environment.properties created successfully")


# -----------------------------------------------
# Create Allure categories.json
# -----------------------------------------------
def create_allure_categories():
    categories = [
        {
            "name": "Authentication errors",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*(401|403).*"
        },
        {
            "name": "UI assertion failures",
            "matchedStatuses": ["failed"],
            "traceRegex": ".*AssertionError.*"
        },
        {
            "name": "Timeout / Wait errors",
            "matchedStatuses": ["failed"],
            "traceRegex": ".*Timeout.*"
        },
        {
            "name": "Network issues (API/UI)",
            "matchedStatuses": ["broken"],
            "traceRegex": ".*(ConnectionError|ECONNRESET).*"
        },
        {
            "name": "Unexpected errors",
            "matchedStatuses": ["broken", "failed"],
        }
    ]

    os.makedirs(ENV_DIR, exist_ok=True)
    with open(CATEGORIES_FILE, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=4)

    logger.info("✔ Allure categories.json created")


# -----------------------------------------------
# Init ENV (Run once)
# -----------------------------------------------
def init_environment():
    write_allure_environment()
    create_allure_categories()

    logger.info("✔ TEST ENVIRONMENT INITIALIZED")
