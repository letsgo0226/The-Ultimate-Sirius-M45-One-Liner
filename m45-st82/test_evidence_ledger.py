import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location("st82",Path(__file__).with_name("evidence_ledger.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestEvidenceLedger(unittest.TestCase):
    def test_fail_closed_without_audit(self):
        report=m.ledger()
        self.assertEqual(report["audit_verified_count"],0)
        self.assertEqual(report["claim_count"],11)
        self.assertTrue(all(x["execution_evidence_status"]=="UNVERIFIED"
                            for x in report["claim_records"]))
    def test_verified_only_with_matching_evidence(self):
        audit={"protocol":"M45-ST81-REPRODUCIBILITY-AUDIT-v1","stage_results":[]}
        for stage,(path,_,_) in m.STAGES.items():
            source=m.sha256_file(m.ROOT/path)
            audit["stage_results"].append({
                "stage":stage,"status":"pass","source_sha256":source,
                "output_sha256":"a"*64,"repeat_output_sha256":"a"*64,
                "reproducible":True})
            audit["stage_results"].append({"stage":stage+"-TESTS","status":"pass"})
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"audit.json"
            path.write_text(json.dumps(audit),encoding="utf-8")
            report=m.ledger(path)
            self.assertEqual(report["audit_verified_count"],11)
            audit["stage_results"][0]["source_sha256"]="0"*64
            path.write_text(json.dumps(audit),encoding="utf-8")
            report=m.ledger(path)
            self.assertEqual(report["audit_verified_count"],10)
            self.assertFalse(report["claim_records"][0]["checks"]["source_hash_matches_audit"])
    def test_missing_tests_remains_unverified_by_default(self):
        stage="ST64"
        path=m.STAGES[stage][0]
        audit={"protocol":"M45-ST81-REPRODUCIBILITY-AUDIT-v1",
               "stage_results":[{"stage":stage,"status":"pass",
                                 "source_sha256":m.sha256_file(m.ROOT/path),
                                 "output_sha256":"b"*64,"repeat_output_sha256":"b"*64,
                                 "reproducible":True}]}
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/"audit.json"
            file.write_text(json.dumps(audit),encoding="utf-8")
            self.assertEqual(m.ledger(file)["audit_verified_count"],0)
            self.assertEqual(m.ledger(file,require_tests=False)["audit_verified_count"],1)
    def test_duplicate_audit_entry_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/"audit.json"
            file.write_text(json.dumps({
                "protocol":"M45-ST81-REPRODUCIBILITY-AUDIT-v1",
                "stage_results":[{"stage":"ST64"},{"stage":"ST64"}]}))
            with self.assertRaises(ValueError):
                m.ledger(file)
if __name__=="__main__":unittest.main()
