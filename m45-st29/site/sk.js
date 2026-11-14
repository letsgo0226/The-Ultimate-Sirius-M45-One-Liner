"use strict";
(function(root){
function parse(src){
 let i=0;
 function term(depth){
  if(depth>400)throw Error("輸入巢狀層級過深");
  if(i>=src.length)throw Error("表達式不完整");
  const c=src[i++];
  if(c==="S"||c==="K")return c;
  if(c!=="@")throw Error("僅允許 @、S、K");
  return [term(depth+1),term(depth+1)];
 }
 const result=term(0);
 if(i!==src.length)throw Error("表達式含多餘符號");
 return result;
}
function encode(t){return typeof t==="string"?t:"@"+encode(t[0])+encode(t[1]);}
function step(t){
 if(typeof t==="string")return null;
 let args=[],head=t;
 while(Array.isArray(head)){args.unshift(head[1]);head=head[0];}
 let r,rest;
 if(head==="K"&&args.length>=2){r=args[0];rest=args.slice(2);}
 else if(head==="S"&&args.length>=3){r=[[args[0],args[2]],[args[1],args[2]]];rest=args.slice(3);}
 else {
  const l=step(t[0]);if(l!==null)return [l,t[1]];
  const rr=step(t[1]);return rr!==null?[t[0],rr]:null;
 }
 for(const x of rest)r=[r,x];
 return r;
}
function evaluate(src,limit=30){
 if(typeof src!=="string"||src.length<1||src.length>300)throw Error("長度必須介於 1 至 300");
 if(!Number.isInteger(limit)||limit<0||limit>100)throw Error("步數範圍 0–100");
 let t=parse(src),trace=[src];
 for(let i=0;i<limit;i++){
  const next=step(t);
  if(next===null)break;
  const output=encode(next);
  if(output.length>10000)return {status:"UNRESOLVED",reason:"OUTPUT_LIMIT",steps:trace.length-1,trace,result:trace.at(-1)};
  t=next;trace.push(output);
 }
 return {status:step(t)===null?"NORMAL":"UNRESOLVED",steps:trace.length-1,trace,result:trace.at(-1)};
}
root.SKLab={parse,encode,step,evaluate};
if(typeof document!=="undefined"){
 let last=null;
 const out=document.getElementById("output");
 document.getElementById("run").addEventListener("click",()=>{
  try{
   last={protocol:"M45-ST29",engine:"browser-js",created_at:new Date().toISOString(),...evaluate(document.getElementById("expr").value)};
   out.textContent="狀態："+last.status+"\n步數："+last.steps+"\n"+last.trace.join("\n↓\n");
  }catch(e){last=null;out.textContent="錯誤："+e.message;}
 });
 document.getElementById("download").addEventListener("click",()=>{
  if(!last){out.textContent="請先執行計算";return;}
  const url=URL.createObjectURL(new Blob([JSON.stringify(last,null,2)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download="m45-st29-certificate.json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 });
}
})(typeof globalThis!=="undefined"?globalThis:this);
