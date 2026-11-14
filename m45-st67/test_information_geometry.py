import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("information_geometry",Path(__file__).with_name("information_geometry.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestInformationGeometry(unittest.TestCase):
    def test_identical(self):
        r=m.analyze(("1","1j","2","-1"),("1","1j","2","-1"))
        self.assertAlmostEqual(r["a_frame_geometry"]["fidelity"],1)
        self.assertAlmostEqual(r["a_frame_geometry"]["trace_distance"],0)
        self.assertAlmostEqual(r["a_frame_geometry"]["bures_distance"],0)
    def test_orthogonal(self):
        r=m.analyze(("1","0","0","0"),("0","1","0","0"))
        self.assertAlmostEqual(r["a_frame_geometry"]["fidelity"],0)
        self.assertAlmostEqual(r["a_frame_geometry"]["trace_distance"],1)
        self.assertAlmostEqual(r["a_frame_geometry"]["fubini_study_angle_radians"],math.pi/2)
        self.assertAlmostEqual(r["a_frame_geometry"]["bures_distance"],math.sqrt(2))
    def test_global_phase_equivalence(self):
        r=m.analyze(("1","2j","0","-1"),("1j","-2","0","-1j"))
        self.assertAlmostEqual(r["a_frame_geometry"]["fidelity"],1)
    def test_frame_invariance_and_data_processing(self):
        cases=(("1","0","1","0"),("1","0","0","1"),
               ("1","1j","2","-1"),("0","1","0","0"))
        for i in range(len(cases)):
            for j in range(len(cases)):
                r=m.analyze(cases[i],cases[j])
                self.assertLess(r["max_frame_invariant_error"],1e-10)
                self.assertTrue(r["trace_distance_bounds_measurement_tv"])
                self.assertLessEqual(r["binary_measurement_total_variation"],
                                     r["a_frame_geometry"]["trace_distance"]+1e-10)
    def test_bad_inputs(self):
        for first in (("0","0","0","0"),("1","2","3"),("1","nan","0","0")):
            with self.assertRaises(ValueError):m.analyze(first=first)
if __name__=="__main__":unittest.main()
