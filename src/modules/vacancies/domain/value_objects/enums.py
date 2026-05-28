from enum import Enum


class JobBoard(Enum):
    OCC = "occ"
    LINKEDIN = "linkedin"
    ARCDEV = "arcdev"


class StrategyCloseModal(Enum):
    # Tipo de estrategia para cerrar la modal de la pagina de linkedin
    BUTTON = "button"
    OVERLAY = "overlay"
