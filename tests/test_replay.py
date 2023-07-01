import unittest
from circleutils import Replay


SAMPLE_REPLAY = "replay-osu_1278814_2481474922.osr"


class TestReplay(unittest.TestCase):
    def test_read(self):
        replay = Replay.read(SAMPLE_REPLAY)
        self.assertEqual(0, replay.count_50)
        self.assertEqual(0, replay.count_100)
        self.assertEqual(129, replay.count_300)
        self.assertEqual(18, replay.count_geki)
        self.assertEqual(0, replay.count_katu)
        self.assertEqual(0, replay.count_miss)
        self.assertEqual("54e082c3fc2a2b7bd4bb862ffaaef037", replay.map_hash)
        self.assertEqual(147, replay.max_combo)
        self.assertEqual(1608, replay.mods)
        self.assertEqual(1, replay.perfect_combo)
        self.assertEqual("MBmasher", replay.player_name)
        self.assertEqual("7260f34b7339f0c410dcfd35d4e481ff", replay.replay_hash)
        self.assertEqual(798755, replay.score)
        self.assertEqual(2481474922, replay.score_id)
        self.assertEqual(7605553, replay.seed)
        self.assertEqual(636557171420000000, replay.timestamp)
        self.assertEqual(20151228, replay.version)
