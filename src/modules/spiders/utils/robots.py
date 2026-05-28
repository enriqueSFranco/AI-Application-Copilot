import urllib.robotparser
from functools import lru_cache
from urllib.parse import urlparse

# https://www.occ.com.mx/robots.txt
# https://mx.indeed.com/robots.txt
# https://www.linkedin.com/robots.txt


class RobotsCheck:
    @staticmethod
    @lru_cache(maxsize=32)
    def get_parser_from_domain(domain):
        """
        Descarga y cachea el robots.txt de un dominio.
        """
        rp = urllib.robotparser.RobotFileParser()
        robot_url = f"https://www.{domain}/robots.txt"
        rp.set_url(robot_url)

        try:
            rp.read()
        except Exception:
            return None

        return rp

    @staticmethod
    def is_allowed(url: str, user_agent: str = "*"):
        """
        Retorna True si el scraping es permitido.
        """
        domain = urlparse(url).hostname or ""
        rp = RobotsCheck.get_parser_from_domain(domain)
        if not rp:
            return True
        return rp.can_fetch(user_agent, url)
