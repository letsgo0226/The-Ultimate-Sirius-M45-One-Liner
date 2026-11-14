import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("quantum_frames",Path(__file__).with_name("quantum_frames.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestQuantumFrames(unittest.TestCase):
    def test_covariance_across_axes(self):
        for bloch in ((0,0,0),(1,0,0),(0,1,0),(0,0,-1),(0.3,0.4,0.5)):
            for axis in ((1,0,0),(0,1,0),(0,0,1),(1,1,1)):
                for angle in (0,0.5,math.pi,2*math.pi):
                    with self.subTest(bloch=bloch,axis=axis,angle=angle):
                        r=m.analyze(bloch,(1,2,3),axis,angle)
                        self.assertLess(r["max_invariant_error"],1e-10)
                        self.assertAlmostEqual(r["born_plus_original"],r["born_plus_transported"])
    def test_pure_and_mixed(self):
        pure=m.analyze((0,1,0))
        mixed=m.analyze((0,0,0))
        self.assertAlmostEqual(pure["purity_original"],1)
        self.assertAlmostEqual(mixed["purity_original"],0.5)
        self.assertAlmostEqual(mixed["determinant_original"],0.25)
    def test_complex_y_off_diagonal(self):
        r=m.analyze((0,1,0))
        self.assertNotEqual(r["density_matrix_complex_pairs"][0][1][1],0)
    def test_unchanged_state_changed_detector_not_covariant(self):
        rho=m.density((0,0,1))
        pz=m.prob(rho,m.projector((0,0,1)))
        px=m.prob(rho,m.projector((1,0,0)))
        self.assertNotAlmostEqual(pz,px)
    def test_bad_inputs(self):
        for kw in ({"bloch":(1,1,1)},{"measurement_axis":(0,0,0)},
                   {"rotation_axis":(0,0,0)},{"angle":float("nan")},
                   {"bloch":(0,float("inf"),0)}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
