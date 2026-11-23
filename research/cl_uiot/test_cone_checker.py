import unittest,json
from cone_certificate import certificate
from cone_checker import verify
class CheckerTests(unittest.TestCase):
    def test_full(self):
        t=certificate()
        self.assertTrue(verify(json.loads(json.dumps(t))))
    def test_false_leaves(self):
        for t in ("empty","central","cone"):self.assertFalse(verify(t))
    def test_missing(self):self.assertFalse(verify((0,"empty")))
    def test_budget(self):self.assertFalse(verify(certificate(),node_limit=1))
    def test_tamper(self):
        t=certificate()
        self.assertFalse(verify((t[0],"empty",t[2])))
