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


class SliderData(BaseModel):
    slides: np.ndarray
    length: np.ndarray
    slider_duration: np.ndarray
    tick_duration: np.ndarray
    tick_count: np.ndarray

    class Config:
        arbitrary_types_allowed = True


class ComboData(BaseModel):
    combo_given: np.ndarray
    at_combo: np.ndarray
    max_combo: int

    class Config:
        arbitrary_types_allowed = True
