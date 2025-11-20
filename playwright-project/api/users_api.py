import requests
from core.config_loader import config

class UsersAPI:
    BASE = config["api"]["base_url"]

    def get_users(self, page=1):
        return requests.get(f"{self.BASE}/users", params={"page": page})
