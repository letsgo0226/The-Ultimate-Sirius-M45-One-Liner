import unittest
from recursive_tt_vacuum_3p1 import solve,zero
from formal_einstein_3p1 import coefficients
from tt_backreaction_3p1 import correction

class RecursiveVacuumTests(unittest.TestCase):
    def test_second(self):
        self.assertEqual(solve([0,2],[0,0,1],2)[1],correction([0,2],[0,0,1]))
    def test_third(self):
        self.assertEqual(coefficients(solve([0,1],[0,0,1],3)),[zero()]*4)
    def test_fourth(self):
        self.assertEqual(coefficients(solve([0,1],[],4)),[zero()]*5)
    def test_flat(self):
        self.assertEqual(solve([],[],3),[zero()]*3)
    def test_invalid(self):
        for n in (0,-1,2.5,True):
            with self.assertRaises(ValueError):solve([],[],n)
