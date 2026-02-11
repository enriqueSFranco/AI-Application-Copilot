import random


class UserAgentProvider:
    """Proveedor de User-Agents para rotar peticiones HTTP

    Esta clase permite simular diferentes navegadores y dispositivos al
    realizar scraping o peticiones a APIs que aplican detección de bots.
    Los users-agents puedes rotarse de manera aleatoria o secuencial.

    Attrubutes:
        USER_AGENTS (List[str]): Lista de user-agents
        strategy (str): Estrategia de rotación de manera aleatoria o secuencial
        index (int): Puntero usado en round-robin.
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/140.0.0.0 Safari/537.36",
    ]

    def __init__(self, strategy="random"):
        """
        Inicializa el proveedor de user-agents.

        Args:
            strategy (str): Estrategia de rotación.
                - "random": selecciona un user-agent aleatorio.
                - "round_robin": recorre la lista en orden secuencial.
        """
        self.strategy = strategy
        self.index = 0

    def get(self):
        """
        Obtiene un user-agent según la estrategia configurada.

        Returns:
            str: Un user-agent válido de la lista.

        Raises:
            ValueError: Si la estrategia definida no es válida.
        """
        if self.strategy == "random":
            return random.choice(self.USER_AGENTS)
        elif self.strategy == "round_robin":
            ua = self.USER_AGENTS[self.index]
            self.index = (self.index + 1) % len(self.USER_AGENTS)
            return ua
        else:
            raise ValueError(f"Estrategia desconocida: {self.strategy}")
