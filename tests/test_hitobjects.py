import unittest
from circleutils import Spinner, TimingPoint, Slider, calc_combo_data
import numpy as np


SAMPLE_START_TIME = np.array([22745,  46370, 124370])
SAMPLE_END_TIME = np.array([24245, 48245, 126245])
SAMPLE_OVERALL_DIFFICULTY = 4
SAMPLE_SLIDER_TIME = np.array([1014, 1842, 3168, 3665, 4328, 4991, 5986, 6980, 8141, 9632, 10793, 11953, 12450, 12947, 14273, 15102, 15599, 16096, 16925, 17422, 17754, 18251, 18914, 19577, 20406, 20903, 21732, 22229, 22726, 23555, 24881, 26207, 26870, 27533, 28859, 29522, 30185, 30848, 31511, 32837, 33500, 35489, 36152, 36815, 37312, 38141, 38804, 39632, 39964, 40958, 41290, 42284, 42616, 43610, 43942, 44273, 47257, 47754, 48085, 49246, 49577, 49909, 50737, 51400, 52063, 52560, 53389, 54052, 54715, 57367, 58362, 58859, 62008, 62339, 62671, 63168, 64163, 64826, 65157, 65820, 66483, 67312, 67809, 68141, 69135, 69964, 70461, 70958, 71953, 72284, 72947, 73279, 73776, 74439, 75268, 75931, 76594, 76925, 77920, 78583, 79246, 79743, 80572, 81234, 81732, 82395, 83058, 83555, 84052, 84549, 86041, 86373, 87036, 87367])
SAMPLE_TIMING_POINTS_TIME = np.array([1014, 6317, 11953, 14273, 24881, 35489, 46096, 47257, 48748, 49909, 51400, 54052, 62008, 83223, 83555, 85875, 88527])
SAMPLE_TIMING_POINTS_BEAT_LENGTH = np.array([331.491712707182, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -83.3333333333333, -100.0, -100.0, -100.0, -100.0])
SAMPLE_RELATIVE_BEATLENGTH = [331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182]
SAMPLE_VM = [-100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -83.3333333333333, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -100.0]
SAMPLE_SLIDER_SLIDES = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
SAMPLE_SLIDER_LENGTH = np.array([120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 60.0, 60.0, 60.0, 60.0, 60.0, 120.0, 120.0, 360.0, 120.0, 120.0, 60.0, 120.0, 120.0, 60.0, 60.0, 120.0, 120.0, 120.0, 120.0, 60.0, 120.0, 60.0, 120.0, 60.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 120.0, 60.0, 120.0, 120.0, 120.0, 60.0, 120.0, 60.0, 120.0, 60.0, 120.0, 60.0, 60.0, 60.0, 120.0, 60.0, 60.0, 30.0, 60.0, 180.0, 120.0, 180.0, 120.0, 120.0, 120.0, 120.0, 120.0, 60.0, 60.0, 60.0, 71.9999978027344, 71.9999978027344, 143.999995605469, 143.999995605469, 143.999995605469, 71.9999978027344, 71.9999978027344, 143.999995605469, 143.999995605469, 143.999995605469, 71.9999978027344, 71.9999978027344, 143.999995605469, 143.999995605469, 143.999995605469, 143.999995605469, 35.9999989013672, 35.9999989013672, 71.9999978027344, 143.999995605469, 143.999995605469, 71.9999978027344, 143.999995605469, 143.999995605469, 71.9999978027344, 71.9999978027344, 143.999995605469, 143.999995605469, 143.999995605469, 143.999995605469, 71.9999978027344, 71.9999978027344, 143.999995605469, 71.9999978027344, 71.9999978027344, 120.0, 120.0, 360.0, 60.0, 120.0, 60.0, 420.0])
SAMPLE_MULTIPLIER = 1.2
SAMPLE_TICK_RATE = 1
SAMPLE_VERSION = 14
SAMPLE_SLIDER_DURATION = np.array([331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 165.745856353591, 165.745856353591, 165.745856353591, 165.745856353591, 165.745856353591, 331.491712707182, 331.491712707182, 994.4751381215459, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 165.745856353591, 165.745856353591, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 165.745856353591, 331.491712707182, 165.745856353591, 662.983425414364, 331.491712707182, 331.491712707182, 662.983425414364, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 662.983425414364, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 165.745856353591, 331.491712707182, 165.745856353591, 331.491712707182, 165.745856353591, 331.491712707182, 165.745856353591, 165.745856353591, 165.745856353591, 331.491712707182, 165.745856353591, 165.745856353591, 165.745856353591, 165.745856353591, 497.23756906077296, 331.491712707182, 497.23756906077296, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 165.745856353591, 165.74585129542888, 165.74585129542888, 331.4917025908582, 331.4917025908582, 331.4917025908582, 165.74585129542888, 165.74585129542888, 331.4917025908582, 331.4917025908582, 331.4917025908582, 165.74585129542888, 165.74585129542888, 331.4917025908582, 331.4917025908582, 331.4917025908582, 331.4917025908582, 165.74585129542888, 165.74585129542888, 165.74585129542888, 331.4917025908582, 331.4917025908582, 331.49170259085776, 331.4917025908582, 331.4917025908582, 165.74585129542888, 165.74585129542888, 331.4917025908582, 331.4917025908582, 331.4917025908582, 331.4917025908582, 331.49170259085776, 165.74585129542888, 331.4917025908582, 165.74585129542888, 165.74585129542888, 331.491712707182, 331.491712707182, 994.4751381215459, 165.745856353591, 331.491712707182, 165.745856353591, 1160.2209944751369])
SAMPLE_TICK_DURATION = np.array([331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182, 331.491712707182])
SAMPLE_TICK_COUNT = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3])
SAMPLE_SLIDER_MASK = np.array([True, False, True, False, False, False, True, True, True, False, True, False, True, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, True, True, True, True, False, False, True, True, True, False, False, True, True, True, False, True, False, True, False, True, False, False, True, True, False, False, True, True, False, True, False, True, False, False, False, False, True, False, True, True, True, False, True, True, False, True, True, True, False, False, True, True, False, False, False, False, False, True, False, True, False, True, True, False, True, False, True, False, False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, True, False, False, True, True, True, False, False, False, True, True, True, False, True, True, True, True, False, True, True, True, False, False, False, False, False, False, False, True, False, False, True, True, False, False, True, True, True, True, False, False, True, False, True, True, False, True, False, True, False, False, True, True, True, False, False, True, False, False, True, True, True, False, False, True, True, False, False, True, True, True, False, True, False, True, False, True, False, True, True, False, False, False, False, True, True, False, True, True, False, True, False, True, False, True, False, True, False, False, True, True, True, True, False, True, True, True, True])
SAMPLE_COMBO_GIVEN = np.array([2, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 4, 2, 1, 1, 2, 3, 2, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 3, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 3, 1, 2, 2, 3, 1, 2, 2, 1, 2, 2, 3, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 3, 2, 3, 1, 2, 3, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 3, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 3, 3, 1, 1, 2, 2, 2, 1, 3, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 3, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 4, 1, 2, 2, 2, 5])
SAMPLE_AT_COMBO = np.array([0, 2, 3, 5, 6, 7, 8, 10, 12, 14, 15, 17, 18, 20, 21, 22, 24, 25, 26, 27, 29, 30, 31, 32, 34, 35, 36, 37, 39, 40, 41, 43, 45, 49, 51, 52, 53, 55, 58, 60, 61, 62, 64, 66, 68, 69, 71, 72, 74, 75, 77, 78, 79, 81, 84, 85, 86, 88, 90, 91, 93, 94, 96, 97, 98, 99, 100, 103, 104, 106, 108, 111, 112, 114, 116, 117, 119, 121, 124, 125, 126, 128, 130, 131, 132, 133, 134, 135, 137, 138, 140, 141, 144, 146, 147, 149, 150, 152, 153, 154, 156, 158, 159, 160, 162, 164, 165, 166, 168, 170, 171, 172, 174, 176, 178, 179, 180, 182, 184, 186, 187, 188, 189, 192, 194, 197, 198, 200, 203, 205, 207, 208, 210, 212, 214, 215, 216, 217, 218, 219, 220, 221, 224, 225, 226, 229, 231, 232, 233, 235, 237, 239, 241, 242, 243, 245, 246, 248, 250, 251, 253, 254, 256, 257, 258, 260, 262, 264, 265, 266, 268, 269, 270, 272, 274, 276, 277, 278, 281, 284, 285, 286, 288, 290, 292, 293, 296, 297, 299, 300, 302, 303, 305, 307, 308, 309, 310, 311, 313, 315, 316, 318, 320, 321, 324, 325, 327, 328, 330, 331, 333, 334, 335, 337, 339, 341, 345, 346, 348, 350, 352])


class TestSpinner(unittest.TestCase):
    def test_mods_combination_arg(self):
        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY)
        self.assertEqual(1, len(data))
        self.assertEqual(0, len(data[0].mods))

        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY, [])
        self.assertEqual(1, len(data))
        self.assertEqual(0, len(data[0].mods))

        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY, [[]])
        self.assertEqual(1, len(data))
        self.assertEqual(0, len(data[0].mods))

        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY, ["DT", "HR"])
        self.assertEqual(1, len(data))
        self.assertEqual(2, len(data[0].mods))
        self.assertEqual(["DT", "HR"], data[0].mods)

        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY, [[], ["DT", "HR"]])
        self.assertEqual(2, len(data))
        self.assertEqual(0, len(data[0].mods))
        self.assertEqual(2, len(data[1].mods))
        self.assertEqual(["DT", "HR"], data[1].mods)

    def test_spinner_data_nomod(self):
        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY)
        self.assertEqual([], data[0].mods)
        self.assertTrue(np.array_equal(
            np.round(data[0].leeway, 8),
            np.array([0.40906289, 0.35255225, 0.35255225])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].accel_adjusted, 8),
            np.array([0.00183, 0.0016425, 0.0016425])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].max_rot, 8),
            np.array([23.40906289, 29.35255225, 29.35255225])
        ))
        self.assertTrue(np.array_equal(
            data[0].amount,
            np.array([7000, 9000, 9000])
        ))
        self.assertTrue(np.array_equal(
            data[0].length,
            np.array([1500, 1875, 1875])
        ))
        self.assertTrue(np.array_equal(
            data[0].total,
            np.array([8150, 10450, 10450])
        ))
        self.assertTrue(np.array_equal(
            data[0].rot_req,
            np.array([6, 8, 8])
        ))
        self.assertTrue(np.array_equal(data[0].accel_max, data[0].accel_adjusted))
        self.assertFalse(all(data[0].extra_100))
        self.assertFalse(all(data[0].odd))

    def test_spinner_data_dthr(self):
        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY, ["DT", "HR"])
        self.assertEqual(["DT", "HR"], data[0].mods)
        self.assertTrue(np.array_equal(
            np.round(data[0].leeway, 8),
            np.array([1.15717154, 1.08821578, 1.08821578])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].accel_adjusted, 8),
            np.array([0.00122, 0.001095, 0.001095])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].accel_max, 8),
            np.array([0.00183, 0.0016425, 0.0016425])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].max_rot, 8),
            np.array([23.15717154, 29.08821578, 29.08821578])
        ))
        self.assertTrue(np.array_equal(
            data[0].amount,
            np.array([6000, 8000, 8000])
        ))
        self.assertTrue(np.array_equal(
            data[0].length,
            np.array([1500, 1875, 1875])
        ))
        self.assertTrue(np.array_equal(
            data[0].total,
            np.array([7700, 10200, 10200])
        ))
        self.assertTrue(np.array_equal(
            data[0].rot_req,
            np.array([7, 9, 9])
        ))
        self.assertFalse(all(data[0].extra_100))
        self.assertTrue(all(data[0].odd))

    def test_spinner_data_htez(self):
        data = Spinner.calc_spinner_data(SAMPLE_START_TIME, SAMPLE_END_TIME, SAMPLE_OVERALL_DIFFICULTY, ["HT", "EZ"])
        self.assertEqual(["HT", "EZ"], data[0].mods)
        self.assertTrue(np.array_equal(
            np.round(data[0].leeway, 8),
            np.array([1.52704763, 1.47679098, 1.47679098])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].accel_adjusted, 8),
            np.array([0.00244, 0.00219, 0.00219])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].accel_max, 8),
            np.array([0.00183, 0.0016425, 0.0016425])
        ))
        self.assertTrue(np.array_equal(
            np.round(data[0].max_rot, 8),
            np.array([23.52704763, 29.47679098, 29.47679098])
        ))
        self.assertTrue(np.array_equal(
            data[0].amount,
            np.array([7000, 9000, 9000])
        ))
        self.assertTrue(np.array_equal(
            data[0].length,
            np.array([1500, 1875, 1875])
        ))
        self.assertTrue(np.array_equal(
            data[0].total,
            np.array([8800, 11300, 11300])
        ))
        self.assertTrue(np.array_equal(
            data[0].rot_req,
            np.array([5, 7, 7])
        ))
        self.assertFalse(all(data[0].extra_100))
        self.assertTrue(all(data[0].odd))


class TestTimingPoint(unittest.TestCase):
    def test_get_hitobject_beatlength_and_slider_vm(self):
        relative_beatlength, vm = TimingPoint.get_hitobject_beatlength_and_slider_vm(
            SAMPLE_SLIDER_TIME,
            SAMPLE_TIMING_POINTS_TIME,
            SAMPLE_TIMING_POINTS_BEAT_LENGTH
        )
        self.assertEqual(SAMPLE_VM, list(vm))
        self.assertEqual(SAMPLE_RELATIVE_BEATLENGTH, list(relative_beatlength))


class TestSlider(unittest.TestCase):
    def test_calc_slider_duration(self):
        slider_duration = Slider.calc_slider_duration(
            np.array(SAMPLE_VM), SAMPLE_SLIDER_LENGTH,
            np.array(SAMPLE_RELATIVE_BEATLENGTH), SAMPLE_SLIDER_SLIDES,
            SAMPLE_MULTIPLIER
        )
        self.assertTrue(np.array_equal(
            slider_duration,
            SAMPLE_SLIDER_DURATION
        ))

    def test_calc_tick_duration(self):
        tick_duration = Slider.calc_tick_duration(
            np.array(SAMPLE_RELATIVE_BEATLENGTH),
            np.array(SAMPLE_VM),
            SAMPLE_TICK_RATE,
            SAMPLE_VERSION
        )
        self.assertTrue(np.array_equal(
            tick_duration,
            SAMPLE_TICK_DURATION
        ))

    def test_tick_count(self):
        tick_count = Slider.calc_tick_count(
            SAMPLE_SLIDER_DURATION,
            SAMPLE_TICK_DURATION,
            SAMPLE_SLIDER_SLIDES
        )
        self.assertTrue(np.array_equal(
            tick_count,
            SAMPLE_TICK_COUNT
        ))

    def test_calc_slider_data(self):
        data = Slider.calc_slider_data(
            np.array(SAMPLE_RELATIVE_BEATLENGTH),
            np.array(SAMPLE_VM),
            SAMPLE_SLIDER_SLIDES,
            SAMPLE_SLIDER_LENGTH,
            SAMPLE_MULTIPLIER,
            SAMPLE_TICK_RATE,
            SAMPLE_VERSION
        )
        self.assertTrue(np.array_equal(
            data.slider_duration,
            SAMPLE_SLIDER_DURATION
        ))
        self.assertTrue(np.array_equal(
            data.tick_duration,
            SAMPLE_TICK_DURATION
        ))
        self.assertTrue(np.array_equal(
            data.tick_count,
            SAMPLE_TICK_COUNT
        ))


class TestCombo(unittest.TestCase):
    def test_calc_combo_data(self):
        data = calc_combo_data(
            SAMPLE_SLIDER_MASK,
            SAMPLE_TICK_COUNT,
            SAMPLE_SLIDER_SLIDES
        )
        self.assertTrue(np.array_equal(
            data.combo_given,
            SAMPLE_COMBO_GIVEN
        ))
        self.assertTrue(np.array_equal(
            data.at_combo,
            SAMPLE_AT_COMBO
        ))
        self.assertEqual(357, data.max_combo)


if __name__ == "__main__":
    unittest.main()
