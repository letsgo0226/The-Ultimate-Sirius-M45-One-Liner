import unittest,itertools
from fractions import Fraction as Q
from inflation_coefficients import project,extend,mul,identity

class TestInflationCoefficients(unittest.TestCase):
    def test_projection(self):
        matrices=(((1,0),(0,-1)),((0,1),(1,0)),((1,2),(0,-1)),((1,0),(0,1)))
        for t,s in itertools.product(matrices,repeat=2):
            for x in itertools.product((-1,0,1),repeat=4):
                a=project(t,s,(x[:2],x[2:]))
                self.assertEqual(project(t,s,a),a)
                u=extend(t,s,a)
                self.assertEqual(mul(u,u),identity(4))
                self.assertEqual(tuple(r[:2] for r in u),t+((0,0),(0,0)))
    def test_active(self):
        a=project(((-1,),),((1,),),((Q(3,7),),))
        self.assertEqual(a,((Q(3,7),),))
        self.assertEqual(extend(((-1,),),((1,),),a),((-1,Q(3,7)),(0,1)))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            project(((2,),),((1,),),((1,),))
        with self.assertRaises(ValueError):
            extend(((1,),),((1,),),((1,),))
        with self.assertRaises(ValueError):
            project(((1,),),((1,),),((1.0,),))
