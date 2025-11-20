import requests
from core.config_loader import config

class AuthAPI:
    BASE = config["api"]["base_url"]

    def login(self, email, password):
        return requests.post(f"{self.BASE}/login", json={"email": email, "password": password})
