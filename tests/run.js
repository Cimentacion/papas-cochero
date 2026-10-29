const {JSDOM}=require("jsdom");const fs=require("fs");
const html=fs.readFileSync("/home/claude/papas-cochero.html","utf8").replace("function endMatch(normal){","function endMatch(normal){window.__last={P:myPower(),O:M.oppStr*M.omod,n:onIds().length,sq:M.sq.length,min:M.min,e:M.sq.map(p=>Math.round(p.mE)).join(\" \"),st:M.sq.map(p=>p.atk+\"/\"+p.def+(p.known?\"\":\"?\")).join(\" \")};");
const errs=[];
const dom=new JSDOM(html,{url:"https://game.test/",runScripts:"dangerously",pretendToBeVisual:true,beforeParse(w){
  const noop=new Proxy(function(){},{get:(t,k)=>k==="measureText"?()=>({width:10}):(k==="getImageData"?()=>({data:new Uint8ClampedArray(4096)}):noop),apply:()=>noop,set:()=>true});
  w.HTMLCanvasElement.prototype.getContext=()=>noop;w.HTMLCanvasElement.prototype.toDataURL=()=>"data:,";
  w.scrollTo=()=>{};w.addEventListener("error",e=>errs.push(e.message));
}});
const w=dom.window,d=w.document;
const click=sel=>{const el=typeof sel==="string"?d.querySelector(sel):sel;if(!el)throw new Error("no "+sel);el.click()};
const act=(a,v)=>{const el=d.querySelector(`[data-act="${a}"]${v!=null?`[data-v="${v}"]`:""}`);if(!el)throw new Error("no act "+a+" "+v);el.click()};
try{
 act("c-sign");act("close");
 const S=()=>JSON.parse(w.localStorage.getItem("papascochero_v5"));
 w.eval("void 0");
 // hire until 13
 let guard=0;
 while(S().players.length<14&&guard++<40){
   const places=[...d.querySelectorAll('[data-act="place"]')].map(b=>b.dataset.v);
   let hired=false;
   for(const pl of places){act("place",pl);const h=d.querySelector('[data-act="hire"]');if(h){h.click();hired=true;break}}
   if(!hired||S().money<0){act("tab","club");try{act("sub","semana")}catch(e){};act("week");(act("tab","squad"),act("sub","fichar"))}
   if(S().money<30){w.eval("void 0")}
 }
 console.log("players",S().players.length,"money",S().money);
 (act("tab","squad"),act("sub","fichar"));act("scout","primo");act("tab","club");try{act("sub","semana")}catch(e){};act("sub","entreno");act("drill","partidillo");act("drill","rondos");act("drill","correr");
 act("tab","squad");act("sub","once");act("form","1-0-10");act("form","4-3-3");act("auto");
 act("tab","club");try{act("sub","semana")}catch(e){};act("startcomp");
 let matches=0;
 for(let k=0;k<40;k++){
   const st=S();
   if(st.phase==="pre"){console.log("SEASON END tierNext",st.tierNext,"season",st.season,"coach age",st.coach.age,"players",st.players.length,"trophies",st.trophies, "| modal:",d.getElementById("mod-b").textContent.slice(0,300));if(d.querySelector('[data-act="to-offers"]'))act("to-offers");if(d.querySelector('[data-act="offers-done"]'))act("offers-done");else if(!d.getElementById("modal").hidden)act("close");
     if(st.tierNext>=1&&matches>12)break; act("tab","club");try{act("sub","semana")}catch(e){};act("startcomp");continue}
   act("tab","club");try{act("sub","semana")}catch(e){};act("prep");act("conv-ok");act("to-trip");
   d.querySelectorAll('[data-act="gas"]').forEach((b,i)=>{b.click()});
   act("trip");act("close");act("amt",5);act("bet","W");act("betsc");act("kick");
   act("skip");
   act("post1");for(let k=0;k<6;k++){const pr=d.querySelector('#modal [data-act="press"]')||d.querySelector('#modal [data-act="pressans"]');if(!pr)break;pr.click()}if(d.querySelector('[data-act="post2"]'))act("post2");act("post3");
   const res=d.querySelector(".res").textContent;matches++;
   act("after");
   console.log("n",w.__last.n,"sq",w.__last.sq,(d.getElementById("mlog").textContent.match(/descuento[^.]*/g)||[]).join(" / "),"| reloj",d.getElementById("m-min").textContent);console.log(matches,res.replace(/\s+/g," ").slice(0,90),"money",S().money);
 }
}catch(e){console.log("FAIL",e.stack)}
console.log("errors",errs);
process.exit(0);
