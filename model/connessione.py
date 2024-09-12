from dataclasses import dataclass
from model.airport import Airport

@dataclass
class Connessione:
    a1: Airport
    a2: Airport
    n: int

