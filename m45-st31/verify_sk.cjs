"use strict";
const fs=require("node:fs");
require("../m45-st29/site/sk.js");
const {evaluate}=globalThis.SKLab;
function verify(cert){
 if(!cert||cert.protocol!=="M45-ST29"||!Array.isArray(cert.trace)||cert.trace.length<1)throw Error("invalid certificate");
 const expected=evaluate(cert.trace[0],cert.steps);
 if(expected.trace.length!==cert.trace.length)throw Error("trace length mismatch");
 if(JSON.stringify(expected.trace)!==JSON.stringify(cert.trace))throw Error("invalid SK trace");
 if(expected.steps!==cert.steps||expected.result!==cert.result)throw Error("result mismatch");
 // A bounded certificate can be NORMAL only when a further step is impossible.
 if(cert.status!==expected.status)throw Error("status mismatch");
 return {status:"PASS",steps:cert.steps,result:cert.result};
}
if(require.main===module){
 if(process.argv.length!==3)throw Error("usage: node verify_sk.cjs certificate.json");
 console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2],"utf8")))));
}
module.exports={verify};
