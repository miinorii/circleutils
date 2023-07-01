from __future__ import annotations
from .utils import to_uleb128, from_string_data
from .logger import logger


class Collection:
    def __init__(self, date: int, content: dict[str, list[str]]):
        self.date = date
        self.content = content

    @staticmethod
    def read(filepath) -> Collection:
        with open(filepath, "rb") as col_file:
            file_bytes = col_file.read()

        file_date = int.from_bytes(file_bytes[:4], byteorder="little")
        logger.debug(f"collection date: {file_date}")

        col_count = int.from_bytes(file_bytes[4:8], byteorder="little")
        logger.debug(f"number of collections: {col_count}")

        col_content = {}
        offset = 8
        for col_id in range(col_count):
            col_name, length = from_string_data(file_bytes[offset:])
            offset += length
            logger.debug(f"collection name: {col_name}")

            col_content[col_name] = []
            col_size = int.from_bytes(file_bytes[offset:offset + 4], byteorder="little")
            logger.debug(f"number of map in '{col_name}': {col_size}")

            offset += 4
            for _ in range(col_size):
                map_hash, length = from_string_data(file_bytes[offset:])
                offset += length
                logger.debug(f"map hash: {map_hash}")
                col_content[col_name].append(map_hash)
        return Collection(date=file_date, content=col_content)

    def to_bytes(self) -> bytes:
        """
        convert dict into a compliant collection.db format
        see https://github.com/ppy/osu/wiki/Legacy-database-file-structure
        sample:  {'date': 20210809,'content': {'collection 1': ['d104277ef8efda81d390945328a9fca2'],'collection 2': ['54b0095dcda063b1bedc95b2d84d00f1', '5f0ff1c7011fce07f28a74d481c267ea']}}
        """

        col_content = self.content
        date = self.date
        col_count = len(col_content)

        data = bytes()
        data += date.to_bytes(4, byteorder="little")
        data += col_count.to_bytes(4, byteorder="little")

        for col_name in col_content:
            col_name_lenght_uleb128 = to_uleb128(len(col_name))

            data += bytes.fromhex("0b") + col_name_lenght_uleb128
            data += col_name.encode("utf-8")

            col_size = len(col_content[col_name])

            data += col_size.to_bytes(4, byteorder="little")

            for map_hash in col_content[col_name]:
                map_hash_length_uleb128 = to_uleb128(len(map_hash))

                data += bytes.fromhex("0b") + map_hash_length_uleb128
                data += map_hash.encode("utf-8")

        logger.debug(f"data hex: {data.hex()}")
        return data

    def save(self, filepath):
        """
        write converted data to specified file
        """
        with open(filepath, "wb") as f:
            f.write(self.to_bytes())
