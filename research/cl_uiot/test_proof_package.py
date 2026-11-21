import unittest
from pathlib import Path
from proof_package import check
class PackageTests(unittest.TestCase):
    def test_static(self):
        digest=check(Path(__file__).with_name("cone_proof.json"))
        self.assertEqual(len(digest),64)
        print("GCFPPO verified SHA-256:",digest)
