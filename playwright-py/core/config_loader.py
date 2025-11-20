import yaml
import os
from core.environment import init_environment

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    # allow override with env vars if needed
    return cfg

config = load_config()


def pytest_configure(config):
    # init Allure environment & categories
    init_environment()

    if not hasattr(config, "_metadata"):
        return
    config._metadata["Project"] = "QA Framework"

