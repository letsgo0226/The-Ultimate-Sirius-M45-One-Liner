import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path
spec=importlib.util.spec_from_file_location("equivalence",Path(__file__).with_name("equivalence.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class TestEquivalence(unittest.TestCase):
    def test_grid_is_physical(self):
        for p,c in m.grid(16):
            self.assertGreaterEqual(p,0)
            self.assertLessEqual(p,1)
            self.assertGreaterEqual(c,0)
            self.assertLessEqual(c*c,p*(1-p))
    def test_partition(self):
        states=m.grid(8)
        for context in ("Z","X","XZ"):
            groups=m.classes(8,context)
            flattened=[s for members in groups.values() for s in members]
            self.assertEqual(len(flattened),len(states))
            self.assertEqual(set(flattened),set(states))
    def test_context_distinguishes(self):
        a=(Fraction(1,2),Fraction(0))
        b=(Fraction(1,2),Fraction(1,4))
        self.assertEqual(m.probability(a,"Z"),m.probability(b,"Z"))
        self.assertNotEqual(m.probability(a,"X"),m.probability(b,"X"))
    def test_refinement(self):
        # Joint XZ equivalence refines each individual context.
        for members in m.classes(8,"XZ").values():
            for context in ("X","Z"):
                self.assertEqual(len({m.probability(s,context) for s in members}),1)
    def test_full_xz_injective_on_grid(self):
        self.assertEqual(len(m.classes(8,"XZ")),len(m.grid(8)))
    def test_invalid(self):
        for d in (0,33,1.5,True):
            with self.assertRaises(ValueError):m.grid(d)
        with self.assertRaises(ValueError):m.classes(4,"Y")
if __name__=="__main__":unittest.main()
