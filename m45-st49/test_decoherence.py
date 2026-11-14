import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("decoherence",Path(__file__).with_name("decoherence.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestDecoherence(unittest.TestCase):
    def test_plus_initial(self):
        rho=m.state()
        self.assertAlmostEqual(m.measure(rho,"X")["plus"],1.0)
        self.assertAlmostEqual(m.measure(rho,"Z")["plus"],0.5)
    def test_dephasing_preserves_z_changes_x(self):
        rho=m.dephase(m.state(),0)
        self.assertEqual(m.measure(rho,"Z"),{"plus":0.5,"minus":0.5})
        self.assertEqual(m.measure(rho,"X"),{"plus":0.5,"minus":0.5})
    def test_intermediate(self):
        rho=m.dephase(m.state(),0.4)
        self.assertAlmostEqual(m.measure(rho,"X")["plus"],0.7)
        self.assertAlmostEqual(m.measure(rho,"Z")["plus"],0.5)
    def test_pure_z_state(self):
        rho=m.dephase(m.state(1.0),0)
        self.assertEqual(m.measure(rho,"Z")["plus"],1)
        self.assertEqual(m.measure(rho,"X")["plus"],0.5)
    def test_invalid(self):
        for x in (-1,2,float("nan"),float("inf")):
            with self.assertRaises(ValueError):m.state(0.5,x)
        with self.assertRaises(ValueError):m.validate([[1,2],[2,0]])
        with self.assertRaises(ValueError):m.measure(m.state(),"Y")
    def test_trace_and_positivity(self):
        for p in (0,0.1,0.5,0.9,1):
            for gamma in (0,0.25,0.5,1):
                self.assertTrue(m.validate(m.dephase(m.state(p),gamma)))
    def test_interpretation(self):
        result=m.experiment(0.5,0)
        self.assertEqual(result["interpretation"],"SIMULATION_NOT_PHYSICAL_COLLAPSE")
        self.assertAlmostEqual(result["coherence_l1"],0)
if __name__=="__main__":unittest.main()
