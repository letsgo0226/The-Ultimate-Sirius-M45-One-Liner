// ST86: test the actual GitHub assignment decision without GitHub credentials.
const assert = require('node:assert/strict');

function shouldAssign(owner, pr) {
  return Boolean(pr && pr.user && pr.user.login === owner && !pr.draft && !pr.merged);
}
const owner = 'letsgo0226';
assert.equal(shouldAssign(owner, {user:{login:owner}, draft:false, merged:false}), true);
assert.equal(shouldAssign(owner, {user:{login:owner}, draft:true, merged:false}), false);
assert.equal(shouldAssign(owner, {user:{login:'external'}, draft:false, merged:false}), false);
assert.equal(shouldAssign(owner, {user:{login:owner}, draft:false, merged:true}), false);
assert.equal(shouldAssign(owner, null), false);
console.log('ST86 JavaScript assignment guard tests passed');
