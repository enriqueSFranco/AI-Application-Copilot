import random


class UserAgentProvider:
    # Lista de user-agents comunes para rotar
    USER_AGENTS = [
        "Mozilla/5.0 (iPhone17,2; CPU iPhone OS 18_3_1 como Mac OS X) AppleWebKit/605.1.15 (KHTML, como Gecko) Mobile/15E148 Resorts/4.5.2",
        "Mozilla/5.0 (iPhone16,2; CPU iPhone OS 17_5_1 como Mac OS X) AppleWebKit/605.1.15 (KHTML, como Gecko) Mobile/15E148 Resorts/4.7.5",
        "Mozilla/5.0 (Linux; Android 15; SM-S931B Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, como Gecko) Versión/4.0 Chrome/127.0.6533.103 Safari móvil/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, como Gecko) Versión/18.3.1 Safari/605.1.15",
    ]
    def __init__(self, strategy="random"):
        self.strategy = strategy
        self.index = 0

    def get(self):
        if self.strategy == "random":
            return random.choice(self.USER_AGENTS)
        elif self.strategy == "round_robin":
            ua = self.USER_AGENTS[self.index]
            self.index = (self.index + 1) % len(self.USER_AGENTS)
            return ua
        else:
            raise ValueError(f"Estrategia desconocida: {self.strategy}")
