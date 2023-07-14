from .types import GameplayMods
from .hitobject_models import SpinnerData, SliderData, ComboData
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
                          mods_combination: list[list[GameplayMods]] | list[GameplayMods] | None = None) -> list[SpinnerData]:
        if not mods_combination:
            mods_iterable = [[]]
        elif isinstance(mods_combination[0], str):
            mods_iterable = [mods_combination]
        else:
            mods_iterable = mods_combination

        data = []
        length = Spinner.calc_length(start_time, end_time)
        for mods in mods_iterable:
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


class TimingPoint:
    @staticmethod
    def get_hitobject_beatlength_and_slider_vm(hitobjects_time: np.ndarray,
                                               tp_time: np.ndarray,
                                               tp_beatlength: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # Fix for maps with hitobjects defined before timing points
        target = hitobjects_time.copy()  # do not mutate at_time
        target[target < tp_time[0]] = tp_time[0]

        beatlength_list = []
        slider_vm_list = []

        for x in target:
            slider_vm = -100
            current_beatlength = 0
            last_beat_length_idx = -1

            range_mask = tp_time <= x
            type_mask = tp_beatlength[range_mask] > 0

            if any(type_mask):
                current_beatlength = tp_beatlength[range_mask][type_mask][-1]
                last_beat_length_idx = np.where(type_mask == 1)[0][-1]

            if any(~type_mask) and np.where(~type_mask == 1)[0][-1] > last_beat_length_idx:
                slider_vm = tp_beatlength[range_mask][~type_mask][-1]

            beatlength_list.append(current_beatlength)
            slider_vm_list.append(slider_vm)
        return np.array(beatlength_list), np.array(slider_vm_list)


class Slider:
    @staticmethod
    def calc_slider_duration(slider_vm: np.ndarray, length: np.ndarray,
                             beatlength: np.ndarray, slides: np.ndarray,
                             slider_multiplier: float) -> np.ndarray:
        # Notice: The slider's length can be used to determine the time it takes to complete the slider. length / (SliderMultiplier * 100 * SV) * beatLength tells how many milliseconds it takes to complete one slide of the slider (where SV is the slider velocity multiplier given by the effective inherited timing point, or 1 if there is none).
        return (np.clip(np.abs(slider_vm), 10, 1000) * length * beatlength / (slider_multiplier * 10000)) * slides

    @staticmethod
    def calc_tick_duration(beatlength: np.ndarray,
                           slider_vm: np.ndarray,
                           slider_tick_rate: float,
                           beatmap_version: int) -> np.ndarray:
        tick_duration = beatlength / slider_tick_rate
        if beatmap_version < 8:
            tick_duration = tick_duration * (np.clip(np.abs(slider_vm), 10, 1000) / 100)
        return tick_duration

    @staticmethod
    def calc_tick_count(slider_duration: np.ndarray, tick_duration: np.ndarray, slides: np.ndarray) -> np.ndarray:
        # For easier debugging
        # t = slider_duration / slides - tick_duration
        # total = []
        # for i, x in enumerate(t):
        #     current_tick_duration = tick_duration[i]
        #     tics = 0
        #     while x >= 10:
        #         tics += 1
        #         x -= current_tick_duration
        #     total.append(tics)
        # total = np.array(total)
        # return total + total * (slides - 1)
        t = slider_duration / slides - tick_duration
        ticks = np.maximum(0, np.ceil((10 - t) / -tick_duration))
        ticks += ticks * (slides - 1)
        return ticks.astype(int)

    @staticmethod
    def calc_slider_data(relative_beatlength: np.ndarray,
                         vm: np.ndarray,
                         slides: np.ndarray,
                         length: np.ndarray,
                         multiplier: float,
                         tick_rate: float,
                         version: int) -> SliderData:
        slider_duration = Slider.calc_slider_duration(
            vm, length,
            relative_beatlength, slides,
            multiplier
        )
        tick_duration = Slider.calc_tick_duration(
            relative_beatlength, vm,
            tick_rate,
            version
        )
        tick_count = Slider.calc_tick_count(slider_duration, tick_duration, slides)
        return SliderData(
            slides=slides,
            length=length,
            slider_duration=slider_duration,
            tick_duration=tick_duration,
            tick_count=tick_count
        )


def calc_combo_data(slider_mask: np.ndarray, tick_count: np.ndarray, slides: np.ndarray) -> ComboData:
    combo_given = np.ones(slider_mask.shape, dtype=int)
    if any(slider_mask):
        combo_given[slider_mask] = tick_count + slides + 1
    at_combo = np.concatenate(([0], combo_given.cumsum()[:-1]))
    max_combo = combo_given.sum()
    return ComboData(combo_given=combo_given, at_combo=at_combo, max_combo=max_combo)
