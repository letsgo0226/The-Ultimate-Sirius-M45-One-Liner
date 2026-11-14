import copy
import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st85",Path(__file__).with_name("scientific_integrity.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def fixtures():
    audit={"protocol":m.PROTOCOLS["audit"],"stage_results":[]}
    ledger={"protocol":m.PROTOCOLS["ledger"],"claim_records":[],
            "claim_count":0,"audit_verified_count":0,"require_unit_tests":True}
    plan={"protocol":m.PROTOCOLS["plan"],"tasks":[],"returned_task_count":0,
          "policy":"ADVISORY_ONLY_NO_EXECUTION_NO_DEPLOYMENT",
          "scientific_truth_established":False}
    governance={"protocol":m.PROTOCOLS["governance"],"review_decisions":[],
                "source_plan_sha256":m.fingerprint(plan),
                "policy":"READ_ONLY_FAIL_CLOSED_REVIEW_GATE",
                "execution_enabled":False,"approved_count":0,"pending_count":0}
    return audit,ledger,plan,governance

class TestIntegrity(unittest.TestCase):
    def test_empty_valid_chain(self):
        self.assertTrue(m.check_chain(*fixtures())["passed"])
    def test_rejects_approval_and_execution(self):
        for field,value in (("approved_count",1),("execution_enabled",True)):
            docs=list(fixtures())
            docs[3][field]=value
            with self.subTest(field=field):
                self.assertFalse(m.check_chain(*docs)["passed"])
    def test_rejects_modified_plan_binding(self):
        docs=list(fixtures())
        docs[2]["returned_task_count"]=1
        codes={v["code"] for v in m.check_chain(*docs)["violations"]}
        self.assertIn("BROKEN_PLAN_BINDING",codes)
    def test_rejects_forged_verified_claim(self):
        docs=list(fixtures())
        docs[1]["claim_records"]=[{"stage":"ST64","execution_evidence_status":"AUDIT_VERIFIED",
                                   "scientific_truth_status":"NOT_ESTABLISHED_BY_EXECUTION_AUDIT",
                                   "checks":{}}]
        docs[1]["claim_count"]=1
        docs[1]["audit_verified_count"]=1
        self.assertFalse(m.check_chain(*docs)["passed"])
    def test_rejects_unbound_decision(self):
        docs=list(fixtures())
        docs[3]["review_decisions"]=[{"source_task_sha256":"0"*64,
                                      "approved":False,"execution_permitted":False,
                                      "decision":"PENDING_HUMAN_REVIEW"}]
        docs[3]["pending_count"]=1
        codes={v["code"] for v in m.check_chain(*docs)["violations"]}
        self.assertIn("BROKEN_TASK_BINDING",codes)
    def test_deterministic(self):
        docs=fixtures()
        self.assertEqual(m.check_chain(*docs),m.check_chain(*copy.deepcopy(docs)))
if __name__=="__main__":unittest.main()
