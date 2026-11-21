import unittest
from fractions import Fraction as Q
from gw_period_average_3p1 import average,shift_derivative,inner_average,energy_kernel

class PeriodAverageTests(unittest.TestCase):
    def test_idempotent(self):
        f={0:(3,0),1:(2,4)}
        self.assertEqual(average(average(f)),average(f))
    def test_derivative(self):
        self.assertEqual(average(shift_derivative({0:(2,0),3:(4,5)})),{})
    def test_orthogonal(self):
        self.assertEqual(inner_average({1:(2,0)},{2:(2,0)}),0)
        self.assertEqual(inner_average({1:(2,0)},{1:(0,2)}),0)
    def test_cosine_energy(self):
        self.assertEqual(energy_kernel({1:(3,0)},{},2)[0][0],36)
    def test_two_polarizations(self):
        self.assertEqual(energy_kernel({1:(3,0)},{2:(0,2)})[0][0],25)
    def test_constant(self):
        self.assertEqual(energy_kernel({0:(3,0)},{})[0][0],0)
    def test_null_flux(self):
        k=energy_kernel({1:(2,3)},{})
        self.assertEqual(k[0][0]-k[1][1]-k[2][2]-k[3][3],0)
        self.assertEqual(k[0][3],-k[0][0])
