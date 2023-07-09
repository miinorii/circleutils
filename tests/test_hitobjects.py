import unittest
from circleutils import Spinner
import numpy as np


SAMPLE_START_TIME = np.array([22745,  46370, 124370])
SAMPLE_END_TIME = np.array([24245, 48245, 126245])
SAMPLE_OVERALL_DIFFICULTY = 4


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


if __name__ == "__main__":
    unittest.main()
