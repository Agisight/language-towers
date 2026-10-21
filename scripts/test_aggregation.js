// Offline reference tests: same algorithm as the browser's evaluateGroup.
const assert=require('node:assert/strict');
const isScore=v=>typeof v==='number'&&Number.isFinite(v)&&v>=0&&v<=100;
function aggregate({providers,technologies,scores}){
 const ids=providers.filter(p=>p!=='overall');
 const parts=technologies.map(t=>{
  const known=ids.map(p=>scores[p]?.[t]).filter(isScore);
  return known.length?Math.max(...known):null;
 });
 const known=parts.filter(isScore);
 return {value:known.length?Math.round(known.reduce((a,b)=>a+b,0)/known.length):null,known:known.length,total:parts.length};
}
let r=aggregate({providers:['apple','google','overall'],technologies:['mt','localization','apps'],scores:{apple:{mt:0,localization:70,apps:40},google:{mt:80,localization:20,apps:60}}});
assert.deepEqual(r,{value:70,known:3,total:3});
r=aggregate({providers:['apple','google'],technologies:['mt','tts'],scores:{apple:{mt:0},google:{mt:null}}});
assert.deepEqual(r,{value:0,known:1,total:2});
r=aggregate({providers:['apple','google'],technologies:['mt'],scores:{apple:{mt:null},google:{}}});
assert.deepEqual(r,{value:null,known:0,total:1});
console.log('PASS: per-technology OR, 0 vs null, and partial evidence');
