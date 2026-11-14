import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st83",Path(__file__).with_name("epistemic_correction.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def record(stage,fail=None,status="UNVERIFIED"):
    return {"stage":stage,"source_path":"sample.py",
            "execution_evidence_status":status,
            "checks":{key:key!=fail for key in m.ORDER}}

def ledger(*records,require_tests=True):
    return {"protocol":m.EXPECTED_PROTOCOL,
            "require_unit_tests":require_tests,
            "claim_records":list(records)}

class TestCorrection(unittest.TestCase):
    def test_prioritizes_first_missing_prerequisite(self):
        a=record("ST64","source_present")
        b=record("ST68","repeatability_confirmed")
        result=m.plan(ledger(a,b))
        self.assertEqual(result["proposed_task_count"],2)
        self.assertEqual(result["tasks"][0]["action"],"INVESTIGATE_NONDETERMINISM")
        self.assertEqual(result["tasks"][1]["action"],"RESTORE_OR_LOCATE_SOURCE")
        self.assertTrue(all(not t["auto_execute"] for t in result["tasks"]))
    def test_verified_generates_no_tasks(self):
        r=m.plan(ledger(record("ST64",status="AUDIT_VERIFIED")))
        self.assertEqual(r["tasks"],[])
        self.assertFalse(r["scientific_truth_established"])
    def test_missing_tests_can_be_optional(self):
        r=m.plan(ledger(record("ST64","unit_tests_passed"),require_tests=False))
        self.assertEqual(r["tasks"],[])
    def test_determinism_and_limit(self):
        data=ledger(record("ST64","audit_present"),record("ST68","audit_present"))
        self.assertEqual(m.plan(data,1),m.plan(data,1))
        self.assertTrue(m.plan(data,1)["truncated"])
    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):m.plan({"protocol":"wrong","claim_records":[]})
        with self.assertRaises(ValueError):m.plan(ledger(record("ST64"),record("ST64")))
        with self.assertRaises(ValueError):m.plan(ledger(record("ST64")),0)
        with self.assertRaises(ValueError):m.plan(ledger(record("ST64","audit_present",status="AUDIT_VERIFIED")))
        bad=record("ST64")
        bad["checks"]["source_present"]="yes"
        with self.assertRaises(ValueError):m.plan(ledger(bad))
if __name__=="__main__":unittest.main()
