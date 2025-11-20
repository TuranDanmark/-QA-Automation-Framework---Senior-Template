import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("qa_framework")
logger.setLevel(logging.INFO)
logger.propagate = False  # важный фикс — не ломать requests

file_handler = logging.FileHandler("logs/test.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(fmt)

console = logging.StreamHandler()
console.setFormatter(fmt)

logger.addHandler(file_handler)
logger.addHandler(console)
