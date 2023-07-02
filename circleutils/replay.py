from __future__ import annotations
from .utils import from_string_data
from .types import GameModeInt
from pydantic import BaseModel
import lzma
import numpy as np
import pandas as pd


class ReplayData(BaseModel):
    w: np.ndarray
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray

    class Config:
        arbitrary_types_allowed = True

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            data={
                "w": self.w,
                "x": self.x,
                "y": self.y,
                "z": self.z,
            }
        )


class OSRFile(BaseModel):
    gamemode: GameModeInt
    version: int
    map_hash: str
    player_name: str
    replay_hash: str
    count_300: int
    count_100: int
    count_50: int
    count_geki: int
    count_katu: int
    count_miss: int
    score: int
    max_combo: int
    perfect_combo: int
    mods: int
    life_bar_graph: str
    timestamp: int
    seed: int | None
    data: ReplayData
    score_id: int
    extra: int | None

    @classmethod
    def read(cls, filepath) -> OSRFile:
        with open(filepath, "rb") as f:
            osr = f.read()
        gamemode = osr[0]
        version = int.from_bytes(osr[1:5], byteorder="little")
        map_hash, str_len = from_string_data(osr[5:])

        offset = 5 + str_len
        player_name, str_len = from_string_data(osr[offset:])

        offset = offset + str_len
        replay_hash, str_len = from_string_data(osr[offset:])

        offset = offset + str_len
        count_300 = int.from_bytes(osr[offset:offset + 2], byteorder="little")

        offset = offset + 2
        count_100 = int.from_bytes(osr[offset:offset + 2], byteorder="little")

        offset = offset + 2
        count_50 = int.from_bytes(osr[offset:offset + 2], byteorder="little")

        offset = offset + 2
        count_geki = int.from_bytes(osr[offset:offset + 2], byteorder="little")

        offset = offset + 2
        count_katu = int.from_bytes(osr[offset:offset + 2], byteorder="little")

        offset = offset + 2
        count_miss = int.from_bytes(osr[offset:offset + 2], byteorder="little")

        offset = offset + 2
        score = int.from_bytes(osr[offset:offset + 4], byteorder="little")

        offset = offset + 4
        max_combo = int.from_bytes(osr[offset:offset + 2], byteorder="little")

        offset = offset + 2
        perfect_combo = osr[offset]

        offset = offset + 1
        mods = int.from_bytes(osr[offset:offset + 4], byteorder="little")

        offset = offset + 4
        life_bar_graph, str_len = from_string_data(osr[offset:])

        offset = offset + str_len
        timestamp = int.from_bytes(osr[offset:offset + 8], byteorder="little")

        offset = offset + 8
        replay_data_len = int.from_bytes(osr[offset:offset + 4], byteorder="little")

        offset = offset + 4
        lzma_replay_data = osr[offset:offset + replay_data_len]

        decompressed_data = lzma.decompress(lzma_replay_data)
        replay_data = decompressed_data.split(b",")

        # Remove last row if empty
        if replay_data[-1] == b"":
            replay_data.pop()

        # Extract seed
        seed = None
        if b"-12345" in replay_data[-1]:
            seed = int(replay_data[-1].split(b"|")[3])
            replay_data.pop()

        # Extract replay data as numpy arrays
        data_array = np.array([x.split(b"|") for x in replay_data])
        data_w = data_array[:, 0].astype(np.int16)
        data_x = data_array[:, 1].astype(float)
        data_y = data_array[:, 2].astype(float)
        data_z = data_array[:, 3].astype(np.uint8)

        offset = offset + replay_data_len
        score_id = int.from_bytes(osr[offset:offset + 8], byteorder="little")

        offset = offset + 8
        extra = None
        if len(osr[offset:]) > 0:
            extra = int.from_bytes(osr[offset:], byteorder="little")

        return cls(
            gamemode=gamemode,
            version=version,
            map_hash=map_hash,
            player_name=player_name,
            replay_hash=replay_hash,
            count_300=count_300,
            count_100=count_100,
            count_50=count_50,
            count_geki=count_geki,
            count_katu=count_katu,
            count_miss=count_miss,
            score=score,
            max_combo=max_combo,
            perfect_combo=perfect_combo,
            mods=mods,
            life_bar_graph=life_bar_graph,
            timestamp=timestamp,
            seed=seed,
            data=ReplayData(w=data_w, x=data_x, y=data_y, z=data_z),
            score_id=score_id,
            extra=extra
        )
