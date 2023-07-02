from enum import IntEnum
from typing import Literal


GameplayMods = Literal["HD", "DT", "HR", "FL", "NF", "NC", "SD", "SO", "PF", "EZ", "HT", "TD"]


class GameModeInt(IntEnum):
    OSU = 0
    TAIKO = 1
    FRUITS = 2
    MANIA = 3
