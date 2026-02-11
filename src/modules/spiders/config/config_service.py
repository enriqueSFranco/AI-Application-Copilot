from functools import lru_cache
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "selectors.yaml"


class ConfigService:
    @staticmethod
    @lru_cache
    def _load_config():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @classmethod
    def get_site_config(cls, site: str):
        config = cls._load_config()
        if site not in config:
            raise ValueError(f"No se encontró configuración para el sitio '{site}'")
        return config[site]
