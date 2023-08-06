import tf_lessons as tfl
import numpy as np


def test_lesson_dataset():
    expected_xs_sample = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
    obtained_xs_sample = tfl.xs
    np.testing.assert_equal(expected_xs_sample, obtained_xs_sample)
    expected_ys_sample = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)
    obtained_ys_sample = tfl.ys
    np.testing.assert_equal(expected_ys_sample, obtained_ys_sample)
