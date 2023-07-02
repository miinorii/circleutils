from .types import GameplayMods
from .hitobject_models import SpinnerData
import numpy as np


class Spinner:
    @staticmethod
    def calc_length(start_time: np.ndarray, end_time: np.ndarray) -> np.ndarray:
        return end_time - start_time

    @staticmethod
    def calc_adjust_time(mods: list[GameplayMods]) -> float:
        adjust_time = 1
        if "DT" in mods or "NC" in mods:
            adjust_time = 1.5
        elif "HT" in mods:
            adjust_time = 0.75
        return adjust_time

    @staticmethod
    def calc_accel(length: np.ndarray, adjust_time: float) -> tuple[np.ndarray, np.ndarray]:
        accel_max = 8e-05 + np.maximum(0, (5000 - length) / 2000000)
        accel_adjusted = accel_max / adjust_time
        return accel_max, accel_adjusted

    @staticmethod
    def calc_rotation_ratio(od: float, mods: list[GameplayMods]) -> float:
        if "HR" in mods:
            od = min(10, od * 1.4)
        elif "EZ" in mods:
            od = od / 2
        return 2.5 + 0.5 * od if od > 5 else 3.0 + 0.4 * od

    @staticmethod
    def calc_rot_requirement(length: np.ndarray, rot_ratio: float) -> np.ndarray:
        return (length / 1000 * rot_ratio).astype(int)

    @staticmethod
    def calc_max_rotations(length: np.ndarray, accel_adjusted: np.ndarray, adjust_time: float) -> np.ndarray:
        x = 0.05  # from Magnus spinner document
        # x = 0.04999876 # corrected to be more in line with "leeway calculator" (test 1)
        # x = 0.0499986 # corrected to be more in line with "leeway calculator" (test 2)
        delta = np.floor(1000/60 * adjust_time)
        vmax_threshold = np.minimum(np.floor(x / accel_adjusted), length - delta)
        below_threshold_sum = (accel_adjusted * vmax_threshold + accel_adjusted) / 2 * vmax_threshold
        above_threshold_sum = np.maximum(0, length - delta - vmax_threshold) * x
        max_rot = (below_threshold_sum + above_threshold_sum) / np.pi
        return max_rot

    @staticmethod
    def calc_leeways(rot_req: np.ndarray, max_rot: np.ndarray) -> np.ndarray:
        leeways = max_rot - np.floor(max_rot)
        leeways[
            (rot_req % 2 != 0) &
            (np.floor(max_rot) % 2 != 0)
        ] += 1
        return leeways

    @staticmethod
    def calc_total(rot_req: np.ndarray, max_rot: np.ndarray) -> np.ndarray:
        total = np.where(rot_req % 2, np.floor(np.floor(max_rot) / 2) * 100, (rot_req + 3) / 2 * 100)
        total = (total + np.floor((np.floor(max_rot) - (rot_req + 3)) / 2) * 1100).astype(int)
        return total

    @staticmethod
    def calc_amount(rot_req: np.ndarray, max_rot: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        bonus = np.maximum(0, np.floor(max_rot) - (rot_req + 3))
        amount = (np.floor(bonus / 2) * 1000).astype(int)
        extra_100 = ~(rot_req % 2 != 0) & ~(bonus % 2 == 0)
        odd_rot_req = rot_req % 2 != 0
        return amount, extra_100, odd_rot_req

    @staticmethod
    def calc_spinner_data(start_time: np.ndarray,
                          end_time: np.ndarray,
                          base_od: float,
                          mods_combination: list[list[GameplayMods]]) -> list[SpinnerData]:
        data = []
        length = Spinner.calc_length(start_time, end_time)
        for mods in mods_combination:
            adjust_time = Spinner.calc_adjust_time(mods)
            accel_max, accel_adjusted = Spinner.calc_accel(length, adjust_time)
            rot_ratio = Spinner.calc_rotation_ratio(base_od, mods)
            rot_req = Spinner.calc_rot_requirement(length, rot_ratio)
            max_rot = Spinner.calc_max_rotations(length, accel_adjusted, adjust_time)
            leeways = Spinner.calc_leeways(rot_req, max_rot)
            total = Spinner.calc_total(rot_req, max_rot)
            amount, extra_100, odd_rot_req = Spinner.calc_amount(rot_req, max_rot)
            data.append(SpinnerData(**{
                "mods": mods,
                "length": length,
                "accel_max": accel_max,
                "accel_adjusted": accel_adjusted,
                "rot_req": rot_req,
                "max_rot": max_rot,
                "leeway": leeways,
                "total": total,
                "amount": amount,
                "extra_100": extra_100,
                "odd": odd_rot_req
            }))
        return data
