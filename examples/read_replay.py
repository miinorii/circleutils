from circleutils import Replay


# Read replay from file
replay = Replay.read("replay-osu_1278814_2481474922.osr")

print(replay.max_combo, replay.count_miss, replay.player_name, replay.seed)

# Access replay data
print(replay.data.w)
print(replay.data.x)
print(replay.data.y)
print(replay.data.z)

# Replay data to dataframe
data_df = replay.data.to_dataframe()
print(data_df)
