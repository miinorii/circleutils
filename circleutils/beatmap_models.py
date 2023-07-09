from __future__ import annotations
from .types import GameModeInt
from typing import Literal
from pydantic import BaseModel, computed_field
from functools import cached_property
import numpy as np


class GeneralSection(BaseModel):
    audio_filename: str
    audio_lead_in: int = 0
    audio_hash: str | None = None
    preview_time: int = -1
    countdown: int = 1
    sample_set: Literal["Normal", "Soft", "Drum"] | None = "Normal"
    stack_leniency: float = 0.7
    mode: GameModeInt = 0
    letterbox_in_breaks: bool = False
    story_fire_front: bool = True
    use_skin_sprites: bool = False
    always_show_playfield: bool = False
    overlay_position: Literal["NoChange", "Below", "Above"] | None = "NoChange"
    skin_preference: str | None = None
    epilepsy_warning: bool = False
    countdown_offset: int = 0
    special_style: bool = False
    widescreen_storyboard: bool = False
    samples_match_playback_rate: bool = False


class EditorSection(BaseModel):
    bookmarks: list[int] | None = None
    distance_spacing: float | None = None
    beat_divisor: int
    grid_size: int
    timeline_zoom: float | None = None


class MetadataSection(BaseModel):
    title: str
    title_unicode: str | None = None
    artist: str | None = None
    artist_unicode: str | None = None
    creator: str
    version: str | None = None
    source: str | None = None
    tags: list[str] | None = None
    beatmap_id: int | None = None
    beatmap_set_id: int | None = None


class DifficultySection(BaseModel):
    hp_drain_rate: float
    circle_size: float
    overall_difficulty: float
    approach_rate: float
    slider_multiplier: float
    slider_tick_rate: float


class TimingPointsSection(BaseModel):
    time: np.ndarray
    beat_length: np.ndarray
    meter: np.ndarray | None = None
    sample_set: np.ndarray | None = None
    sample_index: np.ndarray | None = None
    volume: np.ndarray | None = None
    uninherited: np.ndarray | None = None
    effects: np.ndarray | None = None

    class Config:
        arbitrary_types_allowed = True


class HitObjectsSection(BaseModel):
    x: np.ndarray
    y: np.ndarray
    time: np.ndarray
    type: np.ndarray
    hit_sound: np.ndarray
    object_params: np.ndarray
    hit_sample: np.ndarray

    class Config:
        arbitrary_types_allowed = True

    @computed_field
    @cached_property
    def empty(self) -> bool:
        return len(self.time) == 0

    @computed_field
    @cached_property
    def slider_mask(self) -> np.ndarray:
        return self.type & 2 == 2

    @computed_field
    @cached_property
    def spinner_mask(self) -> np.ndarray:
        return self.type & 8 == 8

    def filter_by_slider(self) -> HitObjectsSection:
        return HitObjectsSection(
            x=self.x[self.slider_mask],
            y=self.y[self.slider_mask],
            time=self.time[self.slider_mask],
            type=self.type[self.slider_mask],
            hit_sound=self.hit_sound[self.slider_mask],
            object_params=self.object_params[self.slider_mask],
            hit_sample=self.hit_sample[self.slider_mask]
        )

    def filter_by_spinner(self) -> HitObjectsSection:
        return HitObjectsSection(
            x=self.x[self.spinner_mask],
            y=self.y[self.spinner_mask],
            time=self.time[self.spinner_mask],
            type=self.type[self.spinner_mask],
            hit_sound=self.hit_sound[self.spinner_mask],
            object_params=self.object_params[self.spinner_mask].astype(int),
            hit_sample=self.hit_sample[self.spinner_mask]
        )
