import unittest
from fractions import Fraction as Q
from metric_variation_audit_3p1 import (
    check_metric_variation,metric_stress_component,demo
)
from stress_energy_coupled_3p1 import total_stress
from maxwell_3p1 import ETA,scale

class MetricVariationAuditTests(unittest.TestCase):
    def setUp(self):
        self.phi=({(1,0,0,0):Q(2),(0,1,0,0):Q(1)},
                  {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
        self.A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)}, {},
                {(0,0,1,0):Q(3)})

    def test_all_components_coupled(self):
        self.assertTrue(check_metric_variation(self.phi,self.A,Q(3),Q(2)))

    def test_free_scalar_limit(self):
        A=({},{},{},{})
        self.assertTrue(check_metric_variation(self.phi,A,Q(5),Q(2)))

    def test_electromagnetic_limit(self):
        phi=({}, {})
        self.assertTrue(check_metric_variation(phi,self.A,Q(1),Q(2)))

    def test_zero_field(self):
        self.assertTrue(check_metric_variation(({},{}),({},{},{},{}),Q(1),Q(2)))

    def test_individual_offdiagonal_component(self):
        mu,nu=0,1
        lhs=metric_stress_component(self.phi,self.A,mu,nu,Q(3),Q(2))
        rhs=scale(total_stress(self.phi,self.A,mu,nu,Q(3),Q(2)),ETA[mu])
        self.assertEqual(lhs,rhs)

    def test_demo(self):
        self.assertTrue(demo()["all_16_components_match"])

if __name__=="__main__":
    unittest.main()
