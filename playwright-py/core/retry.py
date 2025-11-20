import time
from core.logger import logger

RETRIES = 2

def retry_test(item):
    for attempt in range(RETRIES):
        outcome = yield
        report = outcome.get_result()
        if report.failed and attempt < RETRIES - 1:
            logger.warning(f"🔁 RETRY #{attempt+1} for test: {item.name}")
            time.sleep(1)
            item.rerun = True
        else:
            break
