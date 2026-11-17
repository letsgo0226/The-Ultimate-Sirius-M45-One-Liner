"""Bounded unit tests for the finite CL-UFRT demonstrator."""
import unittest
from fixedpoint import Left, Right, SolutionFixedPoint, identity, encode, decode, finite_solution_fixed_points, demo

class TestCLUFRT(unittest.TestCase):
    def test_witness_round_trip(self):
        for witness in (-2, 0, 2, "proof-token"):
            self.assertEqual(decode(encode(witness)), witness)

    def test_all_identity_fixed_points_are_not_solutions(self):
        placeholder = Left()
        self.assertEqual(identity(placeholder), placeholder)
        with self.assertRaises(TypeError):
            decode(SolutionFixedPoint(placeholder))

    def test_solution_detection(self):
        found = [decode(t) for t in finite_solution_fixed_points(list(range(-4, 5)), lambda x: x*x == 4)]
        self.assertEqual(found, [-2, 2])

    def test_no_valid_witness_in_finite_domain(self):
        self.assertEqual(finite_solution_fixed_points(list(range(-4, 5)), lambda x: x*x == -1), [])

    def test_not_complete_outside_domain(self):
        self.assertEqual(finite_solution_fixed_points([0, 1], lambda x: x*x == 4), [])

    def test_type_branch_constraint(self):
        self.assertIsInstance(encode("proof").point, Right)
        self.assertEqual(demo()["witnesses"], [-2, 2])

if __name__ == "__main__":
    unittest.main()
