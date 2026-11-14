import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("correspondence",Path(__file__).with_name("correspondence.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestCorrespondence(unittest.TestCase):
    def test_covariance_for_group_and_scales(self):
        for word in ("","H","Z","HZ","ZH","HZH","ZHZ","HZHZ"):
            for n in (1,2,16,100,256):
                with self.subTest(word=word,n=n):
                    result=m.run(n,"3/5","4/5",word)
                    self.assertTrue(all(v["macro_covariant"] for v in result["contexts"].values()))
    def test_h_transports_z_to_x(self):
        r=m.run(8,"3/5","4/5","H")
        self.assertEqual(r["contexts"]["Z"]["input_frame_measurement_axis"],"+X")
        self.assertEqual(r["contexts"]["Z"]["exact_plus_probability"],"4/5")
    def test_z_flips_x(self):
        r=m.run(8,"3/5","4/5","Z")
        self.assertEqual(r["contexts"]["X"]["input_frame_measurement_axis"],"-X")
        self.assertEqual(r["contexts"]["X"]["exact_plus_probability"],"1/5")
    def test_invalid_inputs(self):
        for kwargs in ({"n":0},{"n":257},{"x":"1","z":"1"},{"word":"Y"}):
            with self.assertRaises(ValueError):m.run(**kwargs)
    def test_distribution(self):
        r=m.run(32,"3/5","4/5","HZ")
        for case in r["contexts"].values():
            self.assertAlmostEqual(sum(case["macro_count_distribution"]),1,places=12)
            self.assertLessEqual(case["maximum_absolute_distribution_error"],1e-12)
if __name__=="__main__":unittest.main()
