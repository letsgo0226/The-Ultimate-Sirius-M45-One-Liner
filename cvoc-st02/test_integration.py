import unittest
from integration import COMPONENTS, Rejected, digest, verify_manifest

DATA = b'{"state":"sample"}'

def manifest(component='st38-sk-ledger'):
    out = COMPONENTS[component][1]
    return dict(protocol='cvoc-integration-v0', component=component,
        source_commit='a'*40, schema_version='unverified-raw-v0',
        input_digest_sha256=digest(DATA),
        operator_type=f'RawBytes -> Unverified{out}', execution_budget=1,
        authorization='read-only', native_verification=False)

class Tests(unittest.TestCase):
    def test_all_components(self):
        for component in COMPONENTS:
            self.assertFalse(verify_manifest(manifest(component), DATA)['native_verified'])
    def reject(self, update, data=DATA):
        m = manifest(); m.update(update)
        with self.assertRaises(Rejected): verify_manifest(m, data)
    def test_tamper(self): self.reject({}, b'changed')
    def test_unknown_component(self): self.reject({'component':'st99'})
    def test_type(self): self.reject({'operator_type':'SKLedger -> VerifiedTMState'})
    def test_budget(self): self.reject({'execution_budget':-1})
    def test_boolean_budget(self): self.reject({'execution_budget':True})
    def test_write(self): self.reject({'authorization':'write'})
    def test_claim(self): self.reject({'native_verification':True})
    def test_unpinned(self): self.reject({'source_commit':'main'})
    def test_schema(self): self.reject({'schema_version':'unknown'})
    def test_extra_field(self): self.reject({'execute':'yes'})
    def test_oversize(self):
        with self.assertRaises(Rejected): verify_manifest(manifest(), b'x'*1048577)

if __name__ == '__main__': unittest.main()
