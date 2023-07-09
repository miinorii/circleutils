from circleutils import OSUFile
import tarfile


OSU_DUMP_PATH = r"2023_07_01_osu_files.tar.bz2"

with tarfile.open(OSU_DUMP_PATH, "r:bz2") as tar:
    for i, file in enumerate(tar):
        if file.isdir():
            continue
        print(i+1, file.name)
        content = tar.extractfile(file)
        beatmap = OSUFile.read(content)
        print(beatmap.metadata.title)
