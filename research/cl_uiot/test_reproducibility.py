import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from reproducibility import FILES,manifest,verify_manifest

class ReproducibilityTest(unittest.TestCase):
    def test_manifest(self):
        with TemporaryDirectory() as d:
            p=Path(d)
            for name in FILES:
                (p/name).write_bytes(name.encode())
            m=manifest(p)
            self.assertTrue(verify_manifest(p,m))
            self.assertEqual(m,manifest(p))
            self.assertFalse(verify_manifest(p,{"schema":"UECV-07/v1","sha256":{}}))
            for name in FILES:
                f=p/name
                f.write_bytes(b"changed")
                self.assertFalse(verify_manifest(p,m))
                f.write_bytes(name.encode())
            (p/FILES[0]).unlink()
            self.assertFalse(verify_manifest(p,m))
    def test_repository(self):
        p=Path(__file__).resolve().parent
        self.assertTrue(verify_manifest(p,manifest(p)))
