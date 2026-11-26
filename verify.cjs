const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
const elements=new Map();let drawCalls=0;
class Element{constructor(){this.children=[];this.style={};this.dataset={};this.attributes={};this.listeners={};this.textContent='';this.value='';this.classList={toggle(){}};}appendChild(e){this.children.push(e);return e;}replaceChildren(){this.children=[];}setAttribute(k,v){this.attributes[k]=v;}addEventListener(k,fn){this.listeners[k]=fn;}getBoundingClientRect(){return {width:900,height:340,top:0,left:0};}getContext(){return new Proxy({},{get:()=>()=>{drawCalls++},set:()=>true});}}
for(const match of html.matchAll(/id="([^"]+)"/g))elements.set(match[1],new Element());
const document={getElementById:id=>elements.get(id),createElement:()=>new Element(),querySelectorAll:()=>elements.get('target-list').children};
const window={devicePixelRatio:1,addEventListener(){}};
const context=vm.createContext({window,document,console});
vm.runInContext(fs.readFileSync(path.join(__dirname,'data.js'),'utf8'),context);
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).filter(Boolean);
for(const script of scripts)vm.runInContext(script,context);
assert.equal(elements.get('target-select').children.length,8);
assert.equal(elements.get('target-name').textContent,'TrES-2 b');
assert.ok(drawCalls>20);
assert.ok(elements.get('light-curve').width>0);
assert.equal(elements.get('threshold').disabled,true);
assert.equal(elements.get('data-warning').hidden,false);
elements.get('target-select').listeners.change({target:{value:'1'}});
assert.equal(elements.get('target-name').textContent,'HAT-P-7 b');
for(const match of html.matchAll(/(?:src|href)="([^"]+)"/g)){assert.ok(fs.existsSync(path.join(__dirname,match[1])),match[1]);}
const visible=html.replace(/<style>[\s\S]*?<\/style>|<script[\s\S]*?<\/script>/g,'').replace(/<[^>]*>/g,'').trim();
assert.ok(visible.length>10);
assert.ok(!/fetch\(|XMLHttpRequest|https?:/.test(scripts.join('')));
console.log('PASS: scripts initialize, canvas drawing executes, eight targets populate, selection updates, unavailable state is explicit, local assets resolve, no runtime network.');
console.log('NOT SATISFIED: real seeded curves, initial transit markers, three categories, live threshold/folding/reveal with real data.');
