import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st84",Path(__file__).with_name("epistemic_governance.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def sample(action="INVESTIGATE_NONDETERMINISM",failed="repeatability_confirmed"):
    task={"stage":"ST80","action":action,"failed_check":failed,"priority":95,
          "requires_human_approval":True,"auto_execute":False}
    return {"protocol":m.PROTOCOL,"tasks":[task],"returned_task_count":1,
            "policy":"ADVISORY_ONLY_NO_EXECUTION_NO_DEPLOYMENT",
            "scientific_truth_established":False}
class TestGovernance(unittest.TestCase):
    def test_high_risk_requires_review(self):
        r=m.govern(sample())
        d=r["review_decisions"][0]
        self.assertEqual(d["risk"],"high")
        self.assertEqual(d["required_reviewer_role"],"independent_reviewer")
        self.assertEqual(d["decision"],"PENDING_HUMAN_REVIEW")
        self.assertFalse(d["execution_permitted"])
        self.assertEqual(r["approved_count"],0)
    def test_deterministic_and_low_risk(self):
        p=sample("RUN_ST81_AUDIT","audit_present")
        a=m.govern(p)
        self.assertEqual(a,m.govern(p))
        self.assertEqual(a["review_decisions"][0]["risk"],"low")
    def test_empty_plan(self):
        p=sample()
        p["tasks"]=[]
        p["returned_task_count"]=0
        self.assertEqual(m.govern(p)["pending_count"],0)
    def test_rejects_escalation(self):
        for field,value in (("auto_execute",True),("requires_human_approval",False),
                            ("action","DELETE_REPOSITORY"),("priority",True)):
            p=sample()
            p["tasks"][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):m.govern(p)
    def test_rejects_mismatched_action_and_bad_claim(self):
        p=sample()
        p["tasks"][0]["failed_check"]="audit_present"
        with self.assertRaises(ValueError):m.govern(p)
        p=sample()
        p["scientific_truth_established"]=True
        with self.assertRaises(ValueError):m.govern(p)
if __name__=="__main__":unittest.main()
