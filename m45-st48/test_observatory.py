import importlib.util
import io
import json
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("observatory",Path(__file__).with_name("observatory.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class FakeResponse:
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,n):return json.dumps({"signature":{"version":"1.3","source":"test"},
                                      "result":"HEADER\n$$SOE\n2026-Nov-14\n$$EOE"}).encode()

class ObservatoryTests(unittest.TestCase):
    def test_url(self):
        url=m.request_url("mars","2026-11-14")
        self.assertIn("horizons.api",url)
        self.assertIn("COMMAND",url)
    def test_fetch_and_verify(self):
        record=m.fetch("mars","2026-11-14",opener=lambda req,timeout:FakeResponse())
        self.assertTrue(m.verify(record))
        self.assertEqual(record["kind"],"MODEL_EPHEMERIS_NOT_DIRECT_SENSOR_OBSERVATION")
    def test_tamper(self):
        record=m.fetch("mars","2026-11-14",opener=lambda req,timeout:FakeResponse())
        record["result"]+="tamper"
        self.assertFalse(m.verify(record))
    def test_bad_input(self):
        for target,day in (("unknown","2026-11-14"),("mars","bad"),("mars","2200-01-01")):
            with self.subTest(target=target,day=day):
                with self.assertRaises(ValueError):m.request_url(target,day)
    def test_missing_table(self):
        class Invalid:
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def read(self,n):return b'{"signature":{},"result":"ERROR"}'
        with self.assertRaises(ValueError):
            m.fetch("mars","2026-11-14",opener=lambda req,timeout:Invalid())

if __name__=="__main__":unittest.main()
