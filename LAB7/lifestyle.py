from enum import Enum


class LifeStyle(Enum):
    PerRequest = 1
    Scoped = 2
    Singleton = 3
    