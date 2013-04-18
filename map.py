from runes import architecture
from copy import deepcopy

class Map():
    def __init__(self, default, cells=()):
        self.map = [[deepcopy(defaut) for _ in range(80)] for _ in range(21)]
        return