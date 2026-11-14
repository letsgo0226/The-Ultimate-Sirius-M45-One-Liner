import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("relational_frames",Path(__file__).with_name("relational_frames.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestRelationalFrames(unittest.TestCase):
    def test_common_phase_invariance(self):
        for alpha,beta in ((0,0),(0.2,1.1),(-1.4,2.2)):
            for shift in (0,0.5,math.pi,2*math.pi,-3.1):
                with self.subTest(alpha=alpha,beta=beta,shift=shift):
                    r=m.analyze(alpha,beta,shift)
                    self.assertLess(r["collective_phase_invariance_max_error"],1e-10)
                    self.assertAlmostEqual(r["relative_phase_cosine"],math.cos(beta-alpha))
    def test_relative_phase_is_physical(self):
        a=m.analyze(0,0,0)
        b=m.analyze(0,math.pi,0)
        self.assertAlmostEqual(a["relative_phase_cosine"],1)
        self.assertAlmostEqual(b["relative_phase_cosine"],-1)
    def test_twirled_density(self):
        r=m.analyze()
        self.assertAlmostEqual(r["trace"],1)
        self.assertAlmostEqual(r["global_purity_before_twirl"],1)
        self.assertAlmostEqual(r["global_purity_after_twirl"],3/8)
        matrix=r["twirled_joint_density_complex_pairs"]
        for i in range(4):
            self.assertAlmostEqual(matrix[i][i][0],0.25)
            for j in range(4):
                if (i,j) not in ((1,2),(2,1)) and i!=j:
                    self.assertEqual(matrix[i][j],[0,0])
    def test_conditioned_sector_pure(self):
        r=m.analyze()
        pairs=r["one_excitation_conditional_density_complex_pairs"]
        a=[[complex(*v) for v in row] for row in pairs]
        self.assertAlmostEqual(m.trace(a).real,1)
        self.assertAlmostEqual(m.purity(a),1)
    def test_invalid(self):
        for kw in ({"alpha":float("nan")},{"beta":float("inf")},{"shared_shift":1e7}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
