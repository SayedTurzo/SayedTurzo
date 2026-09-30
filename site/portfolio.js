const $=s=>document.querySelector(s);
const make=(tag,text,cls)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n;};
function anchor(text,url){const a=make('a',text,'button');a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a;}
function picture(src,alt){const i=make('img');i.src=src;i.alt=alt;i.loading='lazy';i.onerror=()=>{i.hidden=true;};return i;}
export function portfolio(p){
  const dialog=$('#project-dialog'),detail=$('#project-detail');
  const close=()=>{dialog.close();detail.replaceChildren();};$('#close-project').onclick=close;
  dialog.addEventListener('click',e=>{if(e.target===dialog)close();});dialog.addEventListener('close',()=>detail.replaceChildren());
  function open(project){
    detail.replaceChildren();const title=make('h2',project.title);title.id='project-title';
    detail.append(make('p',project.platform||project.category||'PROJECT ARCHIVE','eyebrow'),title);
    if(project.description)detail.append(make('p',project.description,'lead'));
    if(project.role)detail.append(make('p',project.role+(project.publisher?' / '+project.publisher:''),'small'));
    if(project.youtubeId){const player=make('iframe');player.src='https://www.youtube-nocookie.com/embed/'+project.youtubeId;player.title=project.title;player.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';player.allowFullscreen=true;player.referrerPolicy='strict-origin-when-cross-origin';detail.append(player,anchor('Watch on YouTube ↗','https://www.youtube.com/watch?v='+project.youtubeId));}
    const gallery=make('div',null,'detail-gallery');for(const [i,src] of (project.images||[]).entries())gallery.append(picture(src,project.title+' — screenshot '+(i+1)));detail.append(gallery);
    if(project.url)detail.append(anchor(project.platform==='Roblox'?'Play on Roblox ↗':'View on Google Play ↗',project.url));
    dialog.showModal();
  }
  const renderGames=filter=>{const grid=$('#games');grid.replaceChildren();for(const g of p.games.filter(g=>filter==='All'||g.platform===filter)){const card=make('button',null,'game-card');card.type='button';card.setAttribute('aria-label','Explore '+g.title);const copy=make('div',null,'copy');copy.append(make('span',g.platform.toUpperCase(),'eyebrow'),make('h3',g.title),make('p',g.description),make('span','Explore project ↗','project-cta'));card.append(picture(g.coverImage,g.title+' artwork'),copy);card.onclick=()=>open({...g,images:g.images||[g.coverImage]});grid.append(card);}};
  const platforms=['All',...new Set(p.games.map(g=>g.platform))];$('#filters').replaceChildren();$('#filters').hidden=false;
  for(const f of platforms){const b=make('button',f);b.setAttribute('aria-pressed',String(f==='All'));b.onclick=()=>{for(const n of $('#filters').children)n.setAttribute('aria-pressed',String(n===b));renderGames(f);};$('#filters').append(b);}renderGames('All');
  $('#socials').replaceChildren(anchor('GitHub ↗','https://github.com/'+p.username),anchor('LinkedIn ↗',p.linkedin),anchor('Google Play ↗',p.publisher));
  const bio=make('div',null,'identity');bio.append(picture(p.portrait,p.name+' portrait'),make('div',p.fullName+' / '+p.location));$('.hero-copy').prepend(bio);
  const hero=$('.hero-art');hero.replaceChildren(picture(p.heroImage,p.heroImageAlt||p.name+' portrait'),make('div',p.heroImageLabel||'GAMEPLAY / SYSTEMS / WORLDS','art-label'));hero.classList.add('hero-photographic');hero.classList.toggle('hero-portrait',p.heroImage===p.portrait);
  const specialties=make('div',null,'specialties');for(const text of p.specialties)specialties.append(make('span',text));$('.hero').after(specialties);
  const cv=anchor('View current CV ↗',p.cvUrl);$('.actions').append(cv);
  let category='All',expanded=false;
  function videos(){const matches=p.demonstrations.filter(v=>(category==='All'||v.category===category)&&v.title.toLowerCase().includes($('#project-search').value.toLowerCase()));const grid=$('#showcase-grid');grid.replaceChildren();for(const v of matches.slice(0,expanded?matches.length:6)){const b=make('button',null,'demo-card');b.type='button';b.append(picture('https://i.ytimg.com/vi/'+v.youtubeId+'/hqdefault.jpg',v.title),make('span','▶ WATCH DEMO','project-cta'),make('p',v.category,'eyebrow'),make('h3',v.title));b.onclick=()=>open(v);grid.append(b);}$('#showcase-empty').hidden=matches.length>0;$('#show-more').hidden=matches.length<=6;$('#show-more').textContent=expanded?'Show fewer demonstrations ↑':'Explore all '+matches.length+' demonstrations ↓';}
  for(const c of ['All',...new Set(p.demonstrations.map(v=>v.category))]){const b=make('button',c);b.setAttribute('aria-pressed',String(c==='All'));b.onclick=()=>{category=c;expanded=false;for(const n of $('#showcase-filters').children)n.setAttribute('aria-pressed',String(n===b));videos();};$('#showcase-filters').append(b);}
  $('#project-search').oninput=videos;$('#show-more').onclick=()=>{expanded=!expanded;videos();};videos();
  for(const g of p.archiveProjects){const b=make('button',null,'archive-card');b.append(picture(g.images[0],g.title+' screenshot'),make('h3',g.title),make('p',g.description),make('span','View gallery ↗','project-cta'));b.onclick=()=>open(g);$('#archive-grid').append(b);}
  $('#experience').replaceChildren();for(const x of p.experience){const row=make('article'),role=make('div');role.append(make('span',x.role),make('p',x.dates,'dates'));row.append(make('strong',x.company),role,make('p',x.detail));$('#experience').append(row);}
  const education=make('div',null,'education');education.append(make('h3','Education'));for(const x of p.education)education.append(make('p',x.qualification+' / '+x.institution+' / '+x.year));$('#about').append(education);
  const name=make('p',p.fullName+' · '+p.location);$('#contact').append(name);
  if(p.phone)$('#socials').append(anchor('Call ↗','tel:'+p.phone));
}
