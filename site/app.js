import {Snake} from './snake-engine.mjs';
const $=s=>document.querySelector(s);
const el=(tag,text,className)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(className)n.className=className;return n;};
function link(label,url){const a=el('a',label);a.href=url;return a;}
async function loadProfile(){
  const response=await fetch('./profile.json');if(!response.ok)throw new Error('Profile could not be loaded');const p=await response.json();
  for(const [key,value] of Object.entries(p.theme))document.documentElement.style.setProperty(key==='background'?'--bg':'--'+key,value);
  document.title=p.name+' / Game Developer';$('#bio').textContent=p.bio;$('#footer-name').textContent=p.name+' / Game Developer';
  const heading=$('h1');if(p.headline.endsWith('play.'))heading.replaceChildren(document.createTextNode(p.headline.slice(0,-5)),el('em','play.'));else heading.textContent=p.headline;
  $('#email').href='mailto:'+p.email;$('#socials').append(link('Portfolio ↗',p.portfolio),link('LinkedIn ↗',p.linkedin),link('GitHub ↗','https://github.com/'+p.username));
  const filters=['All',...new Set(p.games.map(g=>g.platform))];
  function renderGames(filter){$('#games').replaceChildren();for(const g of p.games.filter(g=>filter==='All'||g.platform===filter)){const a=link('',g.url);a.className='game-card';const image=el('img');image.src='./assets/'+g.id+'.png';image.alt='';image.loading='lazy';const copy=el('div',undefined,'copy'),top=el('div',undefined,'card-top');top.append(el('span',g.platform.toUpperCase()),el('span','↗'));copy.append(top,el('h3',g.title),el('p',g.description));a.append(image,copy);$('#games').append(a);}}
  for(const f of filters){const b=el('button',f);b.type='button';b.setAttribute('aria-pressed',String(f==='All'));b.onclick=()=>{for(const button of $('#filters').children)button.setAttribute('aria-pressed',String(button===b));renderGames(f);};$('#filters').append(b);}renderGames('All');
  for(const w of p.worlds){const a=link('',w.url);a.append(el('strong',w.title+' ↗'),el('p',w.description));$('#worlds').append(a);}
  for(const s of p.skills){const card=el('article',undefined,'skill-card'),items=el('p');for(const item of s.items)items.append(el('span',item));card.append(el('h3',s.category),items);$('#skills').append(card);}
  for(const x of p.experience){const row=el('article');row.append(el('strong',x.company),el('span',x.role),el('p',x.detail));$('#experience').append(row);}
}
loadProfile().catch(error=>{$('#bio').textContent='Unable to load profile data. Please refresh the page.';console.error(error);});
const canvas=$('#snake'),ctx=canvas.getContext('2d'),game=new Snake();let last=0,best=0;
try{best=Number(localStorage.getItem('st-neon-snake-best'))||0;}catch{}
function refresh(){const status={ready:'READY',running:'PLAYING',paused:'PAUSED',over:'GAME OVER',won:'YOU WIN'};$('#score').textContent=String(game.score).padStart(3,'0');$('#best').textContent=String(best).padStart(3,'0');$('#game-state').textContent=status[game.status];$('#pause').disabled=!['running','paused'].includes(game.status);$('#pause').textContent=game.status==='paused'?'Resume':'Pause';$('#start').textContent=game.status==='ready'?'Start game ↗':'Restart ↗';}
function draw(){ctx.fillStyle='#0b0f14';ctx.fillRect(0,0,600,600);ctx.strokeStyle='#18212b';ctx.lineWidth=1;for(let i=0;i<=20;i++){ctx.beginPath();ctx.moveTo(i*30,0);ctx.lineTo(i*30,600);ctx.moveTo(0,i*30);ctx.lineTo(600,i*30);ctx.stroke();}if(game.food){ctx.fillStyle='#c5ff61';ctx.shadowColor='#c5ff61';ctx.shadowBlur=18;ctx.beginPath();ctx.arc(game.food[0]*30+15,game.food[1]*30+15,8,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}game.body.forEach((p,i)=>{ctx.fillStyle=i===0?'#e6ffb5':'#a99cff';ctx.beginPath();ctx.roundRect(p[0]*30+3,p[1]*30+3,24,24,6);ctx.fill();});if(game.status!=='running'){ctx.fillStyle='#0b0f14bb';ctx.fillRect(0,0,600,600);ctx.textAlign='center';ctx.fillStyle='#f2f3ed';ctx.font='bold 36px sans-serif';ctx.fillText({ready:'NEON SNAKE',paused:'TAKE A BREATHER',over:'ONE MORE RUN?',won:'GRID COMPLETE'}[game.status],300,285);ctx.font='16px sans-serif';ctx.fillStyle='#a5adba';ctx.fillText(game.status==='paused'?'Press Space or Resume':'Hit '+(game.status==='ready'?'Start':'Restart')+' to play',300,323);}}
function start(){game.reset();game.status='running';last=performance.now();canvas.focus({preventScroll:true});refresh();draw();}
function pause(){if(game.status==='running')game.status='paused';else if(game.status==='paused'){game.status='running';last=performance.now();}refresh();draw();}
$('#start').onclick=start;$('#pause').onclick=pause;
canvas.addEventListener('keydown',event=>{const keys={ArrowUp:'up',w:'up',ArrowDown:'down',s:'down',ArrowLeft:'left',a:'left',ArrowRight:'right',d:'right'};const direction=keys[event.key]||keys[event.key.toLowerCase()];if(direction){event.preventDefault();game.turn(direction);}if(event.code==='Space'){event.preventDefault();pause();}});
document.querySelectorAll('[data-direction]').forEach(button=>button.onclick=()=>game.turn(button.dataset.direction));
let touch=null;canvas.addEventListener('pointerdown',event=>{touch=[event.clientX,event.clientY];canvas.setPointerCapture(event.pointerId);});canvas.addEventListener('pointerup',event=>{if(!touch)return;const dx=event.clientX-touch[0],dy=event.clientY-touch[1];if(Math.max(Math.abs(dx),Math.abs(dy))>12)game.turn(Math.abs(dx)>Math.abs(dy)?dx>0?'right':'left':dy>0?'down':'up');touch=null;});canvas.addEventListener('pointercancel',()=>touch=null);
document.addEventListener('visibilitychange',()=>{if(document.hidden&&game.status==='running')pause();});
const observer=new IntersectionObserver(entries=>{if(!entries[0].isIntersecting&&game.status==='running')pause();});observer.observe(canvas);
function frame(now){if(game.status==='running'&&now-last>=Math.max(65,150-game.score*.5)){game.step();last=now;if(game.score>best){best=game.score;try{localStorage.setItem('st-neon-snake-best',String(best));}catch{}}refresh();draw();}requestAnimationFrame(frame);}refresh();draw();requestAnimationFrame(frame);
