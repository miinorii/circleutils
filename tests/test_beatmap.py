import unittest
from circleutils import OSUFile
import numpy as np


SAMPLE_V7_W1252 = "../ressources/49374.osu"
SAMPLE_V10_UTF16LE = "../ressources/191276.osu"
SAMPLE_V12_UTF8 = "../ressources/217519.osu"
SAMPLE_V14_UTF8 = "../ressources/1428960.osu"
SAMPLE_GENERAL = {
    'audio_filename': 'audio.mp3',
    'audio_lead_in': 0,
    'audio_hash': None,
    'preview_time': 62008,
    'countdown': 0,
    'sample_set': 'Soft',
    'stack_leniency': 0.7,
    'mode': 0,
    'letterbox_in_breaks': False,
    'story_fire_front': True,
    'use_skin_sprites': False,
    'always_show_playfield': False,
    'overlay_position': 'NoChange',
    'skin_preference': None,
    'epilepsy_warning': False,
    'countdown_offset': 0,
    'special_style': False,
    'widescreen_storyboard': False,
    'samples_match_playback_rate': False
}
SAMPLE_METADATA = {
    'title': 'Habataki no Birthday',
    'title_unicode': '羽ばたきのバースデイ',
    'artist': "Baby's breath",
    'artist_unicode': "Baby's breath",
    'creator': 'ShogunMoon',
    'version': "Nao's Advanced",
    'source': '天使の3P!',
    'tags': ['Tenshi', 'no', '3P!', "Angel's", '3Piece!', '五島', '潤', 'Jun', 'Gotou', '大野柚布子', 'Oono', 'Yuuko', '紅葉谷希美', 'Nozomi', 'Momijidani', '遠藤', 'ゆりか', 'Endo', 'Yurika', '金城そら', 'Sora', 'Kaneshiro', '古賀', '葵', 'Koga', 'Aoi', 'tv', 'size', 'opening', 'naotoshi', 'gaia', 'hazu-', 'irohas', 'dailycare', 'SnowNiNo_'],
    'beatmap_id': 1428960,
    'beatmap_set_id': 661398
}
SAMPLE_EDITOR = {'bookmarks': None, 'distance_spacing': 1.3, 'beat_divisor': 4, 'grid_size': 32, 'timeline_zoom': 1.7}
SAMPLE_DIFFICULTY = {'hp_drain_rate': 4.8, 'circle_size': 3.5, 'overall_difficulty': 5.6, 'approach_rate': 6.7, 'slider_multiplier': 1.2, 'slider_tick_rate': 1.0}
SAMPLE_COLOURS = {'combo1': [0, 128, 64], 'combo2': [0, 128, 255], 'combo3': [241, 223, 1]}


class TestEncoding(unittest.TestCase):
    def test_read_utf16le(self):
        beatmap = OSUFile.read(SAMPLE_V10_UTF16LE)
        self.assertEqual("月の律動 ~ Rhythm of the moon~", beatmap.metadata.title_unicode)

    def test_read_utf8(self):
        beatmap = OSUFile.read(SAMPLE_V12_UTF8)
        self.assertEqual("無力P", beatmap.metadata.artist_unicode)


class TestSection(unittest.TestCase):
    def test_general(self):
        beatmap = OSUFile.read(SAMPLE_V14_UTF8)
        self.assertEqual(SAMPLE_GENERAL, beatmap.general.model_dump())

    def test_difficulty(self):
        beatmap = OSUFile.read(SAMPLE_V14_UTF8)
        self.assertEqual(SAMPLE_DIFFICULTY, beatmap.difficulty.model_dump())

    def test_metadata(self):
        beatmap = OSUFile.read(SAMPLE_V14_UTF8)
        self.assertEqual(SAMPLE_METADATA, beatmap.metadata.model_dump())

    def test_colours(self):
        beatmap = OSUFile.read(SAMPLE_V14_UTF8)
        self.assertEqual(SAMPLE_COLOURS, beatmap.colours)

    def test_editor(self):
        beatmap = OSUFile.read(SAMPLE_V14_UTF8)
        self.assertEqual(SAMPLE_EDITOR, beatmap.editor.model_dump())

    def test_timing_points(self):
        beatmap = OSUFile.read(SAMPLE_V7_W1252)

        self.assertTrue(np.array_equal(
            np.array([375, -100, -100, -100, -100, -100, -100]),
            beatmap.timing_points.beat_length
        ))
        self.assertTrue(np.array_equal(
            np.array([0, 0, 0, 0, 0, 0, 0]),
            beatmap.timing_points.effects
        ))
        self.assertTrue(np.array_equal(
            np.array([4, 4, 4, 4, 4, 4, 4]),
            beatmap.timing_points.meter
        ))
        self.assertTrue(np.array_equal(
            np.array([0, 1, 0, 1, 0, 1, 0]),
            beatmap.timing_points.sample_index
        ))
        self.assertTrue(np.array_equal(
            np.array([2, 2, 2, 2, 2, 2, 2]),
            beatmap.timing_points.sample_set
        ))
        self.assertTrue(np.array_equal(
            np.array([24245, 24616, 48241, 59491, 102241, 102428, 126241]),
            beatmap.timing_points.time
        ))
        self.assertTrue(np.array_equal(
            np.array([1, 0, 0, 0, 0, 0, 0]),
            beatmap.timing_points.uninherited
        ))
        self.assertTrue(np.array_equal(
            np.array([40, 70, 70, 70, 70, 70, 70]),
            beatmap.timing_points.volume
        ))

    def test_read_v7_hit_objects(self):
        beatmap = OSUFile.read(SAMPLE_V7_W1252)
        self.assertEqual(7, beatmap.version)

        self.assertEqual(128, len(beatmap.hit_objects.x))
        self.assertEqual(128, len(beatmap.hit_objects.y))
        self.assertEqual(128, len(beatmap.hit_objects.type))
        self.assertEqual(128, len(beatmap.hit_objects.time))
        self.assertEqual(128, len(beatmap.hit_objects.object_params))

        self.assertEqual(112, beatmap.hit_objects.x[3])
        self.assertEqual(256, beatmap.hit_objects.y[3])
        self.assertEqual(1, beatmap.hit_objects.type[3])
        self.assertEqual(25745, beatmap.hit_objects.time[3])
        self.assertEqual("24245", beatmap.hit_objects.object_params[0])
        self.assertEqual("B|232:168,2,40,4|0|2", beatmap.hit_objects.object_params[7])

    def test_read_v10_hit_objects(self):
        beatmap = OSUFile.read(SAMPLE_V10_UTF16LE)
        self.assertEqual(10, beatmap.version)

        self.assertEqual(1020, len(beatmap.hit_objects.x))
        self.assertEqual(1020, len(beatmap.hit_objects.y))
        self.assertEqual(1020, len(beatmap.hit_objects.type))
        self.assertEqual(1020, len(beatmap.hit_objects.time))
        self.assertEqual(1020, len(beatmap.hit_objects.object_params))

        self.assertEqual(256, beatmap.hit_objects.x[0])
        self.assertEqual(192, beatmap.hit_objects.y[0])
        self.assertEqual(5, beatmap.hit_objects.type[0])
        self.assertEqual(1, beatmap.hit_objects.type[1])
        self.assertEqual(1056, beatmap.hit_objects.time[0])
        self.assertEqual(1261, beatmap.hit_objects.time[1])
        self.assertEqual("", beatmap.hit_objects.object_params[0])
        self.assertEqual("7220", beatmap.hit_objects.object_params[16])
        self.assertEqual("B|256:96|256:96|256:320|256:320|256:192,1,480", beatmap.hit_objects.object_params[64])

    def test_read_v12_hit_objects(self):
        beatmap = OSUFile.read(SAMPLE_V12_UTF8)
        self.assertEqual(12, beatmap.version)

        self.assertEqual(795, len(beatmap.hit_objects.x))
        self.assertEqual(795, len(beatmap.hit_objects.y))
        self.assertEqual(795, len(beatmap.hit_objects.type))
        self.assertEqual(795, len(beatmap.hit_objects.time))
        self.assertEqual(795, len(beatmap.hit_objects.object_params))

        self.assertEqual(256, beatmap.hit_objects.x[0])
        self.assertEqual(192, beatmap.hit_objects.y[0])
        self.assertEqual(21, beatmap.hit_objects.type[0])
        self.assertEqual(1, beatmap.hit_objects.type[1])
        self.assertEqual(9130, beatmap.hit_objects.time[0])
        self.assertEqual(9205, beatmap.hit_objects.time[1])
        self.assertEqual("", beatmap.hit_objects.object_params[0])

    def test_read_v14_hit_objects(self):
        beatmap = OSUFile.read(SAMPLE_V14_UTF8)
        self.assertEqual(14, beatmap.version)

        self.assertEqual(221, len(beatmap.hit_objects.x))
        self.assertEqual(221, len(beatmap.hit_objects.y))
        self.assertEqual(221, len(beatmap.hit_objects.type))
        self.assertEqual(221, len(beatmap.hit_objects.time))
        self.assertEqual(221, len(beatmap.hit_objects.object_params))

        self.assertEqual(164, beatmap.hit_objects.x[0])
        self.assertEqual(170, beatmap.hit_objects.y[0])
        self.assertEqual(6, beatmap.hit_objects.type[0])
        self.assertEqual(1, beatmap.hit_objects.type[1])
        self.assertEqual(1014, beatmap.hit_objects.time[0])
        self.assertEqual(1676, beatmap.hit_objects.time[1])
        self.assertEqual("P|225:150|296:186,1,120,2|2,0:0|0:0", beatmap.hit_objects.object_params[0])
        self.assertEqual("L|73:338,1,60,2|2,0:0|0:0", beatmap.hit_objects.object_params[12])


class TestHitObjectsFilter(unittest.TestCase):
    def test_filter_by_slider(self):
        beatmap = OSUFile.read(SAMPLE_V7_W1252)
        slider_only = beatmap.hit_objects.filter_by_slider()

        self.assertEqual(61, len(slider_only.x))
        self.assertEqual(61, len(slider_only.y))
        self.assertEqual(61, len(slider_only.type))
        self.assertEqual(61, len(slider_only.type))
        self.assertEqual(61, len(slider_only.object_params))
        self.assertTrue(all(slider_only.type & 2 == 2))

    def test_filter_by_spinner(self):
        beatmap = OSUFile.read(SAMPLE_V7_W1252)
        slider_only = beatmap.hit_objects.filter_by_spinner()

        self.assertEqual(3, len(slider_only.x))
        self.assertEqual(3, len(slider_only.y))
        self.assertEqual(3, len(slider_only.type))
        self.assertEqual(3, len(slider_only.type))
        self.assertEqual(3, len(slider_only.object_params))
        self.assertTrue(all(slider_only.type & 8 == 8))


if __name__ == '__main__':
    unittest.main()
