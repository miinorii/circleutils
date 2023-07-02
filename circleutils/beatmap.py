from __future__ import annotations
from .utils import convert_to_snake_case
from .beatmap_models import (
    GeneralSection, DifficultySection, MetadataSection,
    EditorSection, HitObjectsSection, TimingPointsSection
)
from .hitobject import Spinner
from .hitobject_models import SpinnerData
from .types import GameplayMods
from pydantic import BaseModel
from tarfile import TarInfo
import numpy as np
import io
import json


class OSUFile(BaseModel):
    version: int
    general: GeneralSection
    events: None  # TODO
    editor: EditorSection | None
    metadata: MetadataSection
    difficulty: DifficultySection
    colours:  dict[str, list[int]] | None
    timing_points: TimingPointsSection | None
    hit_objects: HitObjectsSection

    @classmethod
    def read(cls, filepath: str | io.BufferedReader | TarInfo) -> OSUFile:
        if isinstance(filepath, (io.BufferedReader, TarInfo)):
            content = filepath.read()
        else:
            with open(filepath, "rb") as f:
                content = f.read()

        encoding = json.detect_encoding(content)

        # decode with proper encoding and replace newline
        content = content.decode(encoding, "replace").replace("\r\n", "\n")

        # split on newlines and strip whitespaces, ignore empty lines
        content = [x.strip() for x in content.split("\n") if len(x) > 4]

        # Check section linespan
        linespan = {}
        current_section = None
        for index, line in enumerate(content):
            if not line.startswith("[") or not line.endswith("]"):
                continue
            if current_section:
                linespan[current_section].append(index)
            current_section = line
            linespan[current_section] = [index + 1]
        linespan[current_section].append(len(content))

        # Extract version
        version = int(content[0].split("v")[-1])

        start, end = linespan["[General]"]
        general_section = read_kv_section(content[start:end])

        if "[Editor]" in linespan:
            start, end = linespan["[Editor]"]
            editor_section = read_editor_section(content[start:end])
        else:
            editor_section = None

        start, end = linespan["[Metadata]"]
        metadata_section = read_metadata_section(content[start:end])

        start, end = linespan["[Difficulty]"]
        difficulty_section = read_difficulty_section(content[start:end])

        if "[TimingPoints]" in linespan:
            start, end = linespan["[TimingPoints]"]
            timing_points = read_timing_points(content[start:end])
        else:
            timing_points = None

        if "[Colours]" in linespan:
            start, end = linespan["[Colours]"]
            colours_section = read_colours_section(content[start:end])
        else:
            colours_section = None

        start, end = linespan["[HitObjects]"]
        hit_objects = read_hit_objects(content[start:end])

        return cls(
            version=version,
            general=general_section,
            editor=editor_section,
            metadata=metadata_section,
            difficulty=difficulty_section,
            events=None,
            colours=colours_section,
            timing_points=timing_points,
            hit_objects=hit_objects
        )

    def get_spinner_data(self, mods_combination: list[list[GameplayMods]]) -> list[SpinnerData]:
        spinners = self.hit_objects.filter_by_spinner()
        if spinners.empty:
            return []
        return Spinner.calc_spinner_data(
            spinners.time,
            spinners.object_params,
            self.difficulty.overall_difficulty,
            mods_combination
        )


def read_kv_section(section: list[str]) -> dict[str, str]:
    kv = {}
    for line in section:
        # Handle invalid file format
        split = line.strip().split(":", 1)

        # Skip if no value are provided
        if len(split) != 2 or len(split[1]) == 0:
            continue

        # Remove whitespace
        key = split[0].strip()
        value = split[1].strip()

        kv[convert_to_snake_case(key)] = value
    return kv


def read_metadata_section(section: list[str]) -> MetadataSection:
    kv = read_kv_section(section)

    if "tags" in kv:
        kv["tags"] = kv["tags"].split(" ")
    return MetadataSection(**kv)


def read_colours_section(section: list[str]) -> dict[str, list[int]]:
    kv = read_kv_section(section)
    return {k: v.split(",") for k, v in kv.items()}


def read_editor_section(section: list[str]) -> EditorSection:
    kv = read_kv_section(section)

    if "bookmarks" in kv:
        kv["bookmarks"] = kv["bookmarks"].split(",")
    return EditorSection(**kv)


def read_difficulty_section(section: list[str]) -> DifficultySection:
    kv = read_kv_section(section)

    # Fix missing AR
    if "approach_rate" not in kv and "overall_difficulty" in kv:
        kv["approach_rate"] = kv["overall_difficulty"]
    return DifficultySection(**kv)


def read_timing_points(content: list[str]) -> TimingPointsSection:
    kv = {}

    data_array = np.array([x.split(",") for x in content])
    _, data_available = data_array.shape

    if data_available >= 2:
        kv["time"] = data_array[:, 0].astype(float).astype(int)
        kv["beat_length"] = data_array[:, 1].astype(float)
    if data_available >= 5:
        kv["meter"] = data_array[:, 2].astype(int)
        kv["sample_set"] = data_array[:, 3].astype(int)
        kv["sample_index"] = data_array[:, 4].astype(int)
    if data_available >= 6:
        kv["volume"] = data_array[:, 5].astype(int)
    if data_available >= 7:
        kv["uninherited"] = data_array[:, 6].astype(np.uint8)
    if data_available >= 8:
        kv["effects"] = data_array[:, 7].astype(int)

    return TimingPointsSection(**kv)


def read_hit_objects(content: list[str]) -> HitObjectsSection:
    # May god forgive me for what im about to code ... (should handle all edgecases)
    data = []
    for line in content:
        split = line.replace(":0:0:0:0:", ",0:0:0:0:").split(",", 5)
        if len(split) == 5:
            split.append("")
            split.append("0:0:0:0:")
        else:
            if int(split[3]) & 1:
                split.insert(-1, "")
            else:
                second_part = split.pop().rsplit(",", 1)
                if second_part[-1].count(":") >= 1 and "|" not in second_part[-1]:
                    split.append(second_part[0])
                    split.append(second_part[-1])
                else:
                    split.append(",".join(second_part))
                    split.append("0:0:0:0:")
        data.append(split)
    # dtype=object to prevent numpy from exploding when parsing .osu with really long strings ex: 2571051.osu
    data_array = np.array(data, dtype=object, copy=False)
    return HitObjectsSection(**{
        "x": data_array[:, 0].astype(float).astype(int),
        "y": data_array[:, 1].astype(float).astype(int),
        "time": data_array[:, 2].astype(int),
        "type": data_array[:, 3].astype(int),
        "hit_sound": data_array[:, 4].astype(int),
        "object_params": data_array[:, 5].astype(str),
        "hit_sample": data_array[:, 6].astype(str)
    })

