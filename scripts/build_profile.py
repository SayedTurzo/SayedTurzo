"""Generate README, local artwork, and site content from profile.json. Requires Pillow."""
from pathlib import Path
import json, math, html, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
def font(size, bold=False):
    candidates = ['C:/Windows/Fonts/seguisb.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for path in candidates:
        if Path(path).exists(): return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)

def hero():
    frames=[]
    for frame in range(48):
        im=Image.new('RGB',(1200,430),P['theme']['background']);d=ImageDraw.Draw(im)
        d.line((40,390,1160,390),fill='#30353f')
        d.text((52,43),'SAYED / PLAYLAB',font=font(15,True),fill=P['theme']['accent'])
        d.text((48,98),P['name'],font=font(76,True),fill='#f2f3ed')
        d.text((52,203),P['headline'],font=font(30),fill='#b9bfcb')
        d.text((52,294),'UNITY   /   UNREAL ENGINE   /   ROBLOX',font=font(17,True),fill=P['theme']['accent'])
        d.text((52,348),'GAMEPLAY  ·  MULTIPLAYER  ·  VR & SIMULATION',font=font(13),fill='#9299a6')
        theta=frame/48*2*math.pi
        cx,cy=955,202
        # Rotating wireframe sphere: original procedural artwork, no external asset.
        for latitude in range(-60,61,20):
            phi=math.radians(latitude);pts=[]
            for longitude in range(0,361,6):
                a=math.radians(longitude)+theta
                x=math.cos(phi)*math.cos(a);y=math.sin(phi);z=math.cos(phi)*math.sin(a)
                scale=130*(1+z*.10);pts.append((cx+x*scale,cy+(y*.93+z*.24)*scale))
            d.line(pts,fill='#687d40',width=1)
        for longitude in range(0,180,20):
            pts=[]
            for latitude in range(0,361,4):
                a=math.radians(longitude)+theta;b=math.radians(latitude)
                x=math.cos(b)*math.cos(a);y=math.sin(b);z=math.cos(b)*math.sin(a)
                pts.append((cx+x*130,cy+(y*.93+z*.24)*130))
            d.line(pts,fill=P['theme']['accent'],width=1)
        angle=theta
        px=cx+170*math.cos(angle);py=cy+58*math.sin(angle)
        d.ellipse((cx-170,cy-58,cx+170,cy+58),outline='#514667',width=1)
        d.ellipse((px-8,py-8,px+8,py+8),fill=P['theme']['secondary'])
        d.text((840,351),'IMAGINATION → INTERACTION',font=font(12),fill='#9299a6')
        frames.append(im)
    frames[0].save(ASSETS/'hero.gif',save_all=True,append_images=frames[1:],duration=85,loop=0,optimize=True)

def cover(g):
    im=Image.new('RGB',(1000,730),'#121820');accent=g.get('accent',P['theme']['accent'])
    if g.get('coverImage'):
        image_path=(ROOT/g['coverImage']).resolve()
        if not image_path.is_relative_to(ROOT): raise ValueError('coverImage must be inside the repository')
        with Image.open(image_path) as source: im.paste(ImageOps.fit(source.convert('RGB'),(1000,475)),(0,0))
    else:
        d=ImageDraw.Draw(im)
        for i in range(14):
            radius=30+i*17;d.ellipse((500-radius,235-radius*.55,500+radius,235+radius*.55),outline='#304052',width=2)
        d.text((65,115),g['title'],font=font(60,True),fill=accent)
        d.text((65,230),g['platform'].upper()+' / GAME DEVELOPMENT',font=font(20),fill='#a9b6c5')
    d=ImageDraw.Draw(im)
    d.line((0,475,1000,475),fill=accent,width=4)
    d.text((40,505),g['platform'].upper()+'   /   CONTRIBUTED TO THIS GAME',font=font(18,True),fill=accent)
    words=g['title'].split();lines=['']
    for word in words:
        candidate=(lines[-1]+' '+word).strip()
        if d.textlength(candidate,font=font(39,True))>900:lines.append(word)
        else:lines[-1]=candidate
    for i,line in enumerate(lines):d.text((40,547+i*47),line,font=font(39,True),fill='#f2f5f7')
    d.text((40,677),'EXPLORE GAME',font=font(16,True),fill='#a0a9b7')
    d.text((920,653),'↗',font=font(48),fill=accent)
    im.save(ASSETS/(g['id']+'.png'))

def toolkit():
    im=Image.new('RGB',(1200,((len(P['skills'])+1)//2)*235+10),P['theme']['background']);d=ImageDraw.Draw(im)
    for index,skill in enumerate(P['skills']):
        x=20+(index%2)*590;y=15+(index//2)*235;accent=P['theme']['accent'] if index%2==0 else P['theme']['secondary']
        d.rounded_rectangle((x,y,x+570,y+215),radius=20,fill='#141a23',outline='#293341',width=2)
        d.rounded_rectangle((x+25,y+26,x+31,y+51),radius=3,fill=accent)
        d.text((x+47,y+23),skill['category'],font=font(26,True),fill='#ecf0f5')
        px=x+26;py=y+82
        for item in skill['items']:
            width=d.textlength(item,font=font(20))+30
            if px+width>x+545:px=x+26;py+=46
            d.rounded_rectangle((px,py,px+width,py+35),radius=8,fill='#232d3c')
            d.text((px+15,py+3),item,font=font(20),fill='#cdd7e6');px+=width+10
    im.save(ASSETS/'toolkit.png')

def worlds():
    for index,w in enumerate(P['worlds']):
        im=Image.new('RGB',(600,390),'#141a23');d=ImageDraw.Draw(im);accent=P['theme']['secondary']
        for col in range(9):
            x=40+col*65;height=35+((col*37+index*43)%105)
            d.rectangle((x,190-height,x+38,190),outline='#617080',width=2)
            d.line((x,190-height,x+18,174-height,x+56,174-height,x+38,190-height),fill=accent,width=2)
        d.text((32,235),w['title'],font=font(35,True),fill='#edf3f9')
        d.text((32,290),'VIRTUAL WORLDS / UNITY',font=font(15),fill='#98a8ba')
        d.text((32,345),'EXPLORE WORLD',font=font(15,True),fill=accent)
        d.text((530,322),'↗',font=font(40),fill=accent)
        im.save(ASSETS/f'world-{index}.png')

def md(text): return str(text).replace('|','\\|').replace('\n',' ')
def a(label,url): return f'<a href="{html.escape(url,quote=True)}">{html.escape(label)}</a>'
def asset(name):
    path=ASSETS/name
    digest=hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.exists() else 'initial'
    return 'assets/'+name+'?v='+digest
def readme():
    live=P.get('sitePublished',False)
    main_link=a('▶ PLAY NEON SNAKE',P['siteUrl']+'#arcade') if live else a('PORTFOLIO ↗',P['portfolio'])
    out=['<!-- Generated by scripts/build_profile.py. Edit profile.json, then rebuild. -->',f'<p align="center"><img src="{asset("hero.gif")}" alt="{html.escape(P["name"])} — {html.escape(P["headline"])}" width="100%"></p>',f'<p align="center"><strong>Unity · Unreal Engine · Roblox · Multiplayer · VR</strong></p>',f'<p align="center">{html.escape(P["bio"])}</p>',f'<p align="center">{main_link} &nbsp; / &nbsp; {a("LET’S TALK ↗","mailto:"+P["email"])}</p>','## Games I’ve worked on']
    featured=[g for g in P['games'] if g.get('featured')]
    for i in range(0,len(featured),2):
        cards=[]
        for g in featured[i:i+2]:cards.append(f'<a href="{html.escape(g["url"],quote=True)}"><img src="{asset(g["id"]+".png")}" alt="{html.escape(g["title"])} — {html.escape(g["platform"])}. Visit game." width="49%"></a>')
        out.append('<p>'+ '\n'.join(cards)+'</p>')
    more=[g for g in P['games'] if not g.get('featured')]
    if more:out.append('<p><strong>More games</strong><br><br>'+ ' &nbsp; · &nbsp; '.join(a(g['title']+' ↗',g['url']) for g in more)+'</p>')
    out+=['## What I build with','<img src="'+asset('toolkit.png')+'" alt="'+html.escape('; '.join(s['category']+': '+', '.join(s['items']) for s in P['skills']))+'" width="100%">']
    if P['worlds']:
        out+=['## Multiplayer worlds & immersive experiences']
        out.append('<p>'+ '\n'.join(f'<a href="{html.escape(w["url"],quote=True)}"><img src="{asset(f"world-{index}.png")}" alt="{html.escape(w["title"]+": "+w["description"])}. Visit world." width="32%"></a>' for index,w in enumerate(P['worlds']))+'</p>')
    if live:out+=['## Your turn to play',f'**[Play Neon Snake →]({P["siteUrl"]}#arcade)** · Keyboard, swipe, mobile controls, and your personal best.']
    else:out+=['## Neon Snake', 'The browser game is built. Public access will appear here after GitHub Pages deployment is verified. [Deployment setup →](CUSTOMIZE.md#make-it-live-on-github)']
    out+=['## Contribution trail','<picture><source media="(prefers-color-scheme: dark)" srcset="assets/contributions-dark.svg"><img src="assets/contributions.svg" alt="GitHub contribution snake animation" width="100%"></picture>',f'<p align="center">{a("Portfolio",P["portfolio"])} · {a("LinkedIn",P["linkedin"])} · {a("Email","mailto:"+P["email"])}</p>']
    (ROOT/'README.md').write_text('\n\n'.join(out)+'\n',encoding='utf-8')

if __name__=='__main__':
    hero()
    for g in P['games']: cover(g)
    toolkit()
    worlds()
    readme()
    # Honest first-run state. The scheduled workflow replaces these with real contribution data.
    for name in ['contributions.svg','contributions-dark.svg']:
        path=ASSETS/name
        if not path.exists():path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="90"><rect width="1200" height="90" rx="12" fill="#151922"/><text x="40" y="52" fill="#9299a6" font-family="sans-serif" font-size="18">Contribution snake appears after the first Profile refresh workflow run.</text></svg>',encoding='utf-8')
    (ROOT/'site'/'profile.json').write_text(json.dumps(P,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    shutil.copytree(ASSETS,ROOT/'site'/'assets',dirs_exist_ok=True)
    # One immutable release keeps HTML, modules, styling and content in sync.
    # Existing visitors may otherwise receive new HTML with cached old JS/JSON.
    release_files=['app.js','portfolio.js','snake-engine.mjs','styles.css','profile.json']
    revision=hashlib.sha256(b''.join((ROOT/'site'/name).read_bytes() for name in release_files)).hexdigest()[:16]
    release=ROOT/'site'/'releases'/revision
    release.mkdir(parents=True,exist_ok=True)
    for name in release_files:shutil.copy2(ROOT/'site'/name,release/name)
    template=(ROOT/'site'/'index.template.html').read_text(encoding='utf-8')
    page=template.replace('href="styles.css"',f'href="releases/{revision}/styles.css"').replace('src="app.js"',f'src="releases/{revision}/app.js"')
    (ROOT/'site'/'index.html').write_text(page,encoding='utf-8')
    print('Built README, animated GIF, game cards and site content.')
