import tf_lessons as tfl
import numpy as np


def test_nothing():
    expected_sample = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
    obtained_sample = tfl.xs
    np.testing.assert_equal(expected_sample, obtained_sample)
