import copy
import unittest
from continuity_bridge import Denied, sample_record, seal, verify, three_node_simulation

class ST96Tests(unittest.TestCase):
    def test_valid_synthetic_record(self):
        record = sample_record()
        self.assertEqual(verify(seal(record)), record)

    def test_three_node_corruption_rejected(self):
        self.assertEqual(three_node_simulation(seal(sample_record())), {
            "accepted": 2, "rejected": 1, "no_network": True
        })

    def test_tampering_rejected(self):
        envelope = seal(sample_record())
        envelope["record"]["payload"]["text"] = "changed"
        with self.assertRaises(Denied):
            verify(envelope)

    def test_authorization_fail_closed(self):
        record = sample_record()
        record["approved_for_transfer"] = False
        with self.assertRaises(Denied):
            seal(record)

    def test_nested_secret_rejected(self):
        record = sample_record()
        record["payload"]["nested"] = [{"api_key": "synthetic-placeholder"}]
        with self.assertRaises(Denied):
            seal(record)

    def test_investment_action_rejected(self):
        record = sample_record()
        record["payload"]["action"] = "invest"
        with self.assertRaises(Denied):
            seal(record)

    def test_deployment_action_rejected(self):
        record = sample_record()
        record["payload"]["action"] = "deploy"
        with self.assertRaises(Denied):
            seal(record)

    def test_cannot_swap_signature(self):
        one = seal(sample_record())
        other = seal({**sample_record(), "id": "synthetic-002"})
        one["hmac_sha256"] = other["hmac_sha256"]
        with self.assertRaises(Denied):
            verify(one)

    def test_oversized_payload_rejected(self):
        record = sample_record()
        record["payload"]["text"] = "x" * 9000
        with self.assertRaises(Denied):
            seal(record)

if __name__ == "__main__":
    unittest.main()
