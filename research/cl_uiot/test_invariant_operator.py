"""Offline finite tests: symmetry-preserving solution sets and counterexamples."""
import unittest
from invariant_operator import (
    FiniteInvariantModel, commutes, demo, fixed_operator, is_fixed,
    is_solution, matvec
)

class InvariantOperatorTests(unittest.TestCase):
    def setUp(self):
        self.D = ((1, 0), (0, 0))
        self.U = ((-1, 0), (0, 1))

    def test_commuting_symmetry(self):
        self.assertTrue(commutes(self.D, self.U))

    def test_kernel_fixedpoint_equivalence(self):
        T = fixed_operator(self.D, 3)
        for x in range(-3, 4):
            for y in range(-3, 4):
                psi = (x, y)
                self.assertEqual(is_fixed(T, psi), is_solution(self.D, psi))

    def test_symmetry_transports_every_supplied_solution(self):
        model = FiniteInvariantModel(self.D, self.U)
        self.assertTrue(model.check_axioms())
        for y in range(-5, 6):
            self.assertTrue(model.solution_transports((0, y)))

    def test_noncommuting_action_rejected(self):
        # Swap mixes D's zero and nonzero eigenspaces.
        swap = ((0, 1), (1, 0))
        self.assertFalse(commutes(self.D, swap))
        self.assertFalse(FiniteInvariantModel(self.D, swap).check_axioms())

    def test_symmetry_without_commutation_can_destroy_solution(self):
        swap = ((0, 1), (1, 0))
        psi = (0, 1)
        self.assertTrue(is_solution(self.D, psi))
        self.assertFalse(is_solution(self.D, matvec(swap, psi)))

    def test_zero_lambda_forbidden(self):
        with self.assertRaises(ValueError):
            fixed_operator(self.D, 0)

    def test_example_has_nonidentity_operator(self):
        self.assertNotEqual(fixed_operator(self.D, 2), ((1, 0), (0, 1)))
        self.assertEqual(demo()["solutions"], demo()["fixed_points"])
        self.assertTrue(demo()["symmetry_preserves_solutions"])

if __name__ == "__main__":
    unittest.main()
