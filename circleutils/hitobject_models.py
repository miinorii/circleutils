from pydantic import BaseModel
import numpy as np
from .types import GameplayMods


class SpinnerData(BaseModel):
    mods: list[GameplayMods]
    length: np.ndarray
    accel_max: np.ndarray
    accel_adjusted: np.ndarray
    rot_req: np.ndarray
    max_rot: np.ndarray
    leeway: np.ndarray
    total: np.ndarray
    amount: np.ndarray
    extra_100: np.ndarray
    odd: np.ndarray

    class Config:
        arbitrary_types_allowed = True
