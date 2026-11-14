// Exercise the actual inline github-script body with mocked event metadata and API.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const workflow = fs.readFileSync(path.join(__dirname, '..', '.github', 'workflows', 'm45-st86.yml'), 'utf8');
const match = workflow.match(/          script: \|\n([\s\S]*?)(?=  policy-tests:)/);
assert.ok(match, 'assignment script exists');
const script = match[1].split('\n').map(line => line.startsWith('            ') ? line.slice(12) : line).join('\n');
const run = new Function('context', 'github', 'core', 'return (async () => {\n' + script + '\n})()');

async function check(author, draft, merged, expected) {
  const calls = [];
  const context = {repo: {owner: 'letsgo0226', repo: 'The-Ultimate-Sirius-M45-One-Liner'},
    payload: {pull_request: {number: 61, user: {login: author}, draft, merged}}};
  const github = {rest: {issues: {addAssignees: async args => calls.push(args)}}};
  await run(context, github, {info: () => {}});
  assert.equal(calls.length, expected);
  if (expected) assert.deepEqual(calls[0].assignees, ['letsgo0226']);
}
(async () => {
  await check('letsgo0226', false, false, 1);
  await check('letsgo0226', true, false, 0);
  await check('external', false, false, 0);
  await check('letsgo0226', false, true, 0);
  console.log('ST86 actual workflow JavaScript guard tests passed');
})().catch(error => {console.error(error); process.exitCode = 1;});
