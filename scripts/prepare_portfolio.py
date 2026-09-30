"""Verify imported YouTube demonstrations and prepare editable portfolio content."""
import json, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
e=json.loads((ROOT/'portfolio-evidence.json').read_text(encoding='utf-8'))
def verify(v):
    url='https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v='+v['youtubeId']
    try:
        data=json.load(urllib.request.urlopen(url,timeout=20))
        v['title']=data['title'];v['verified']=True
    except Exception as error:v['verified']=False;v['error']=str(error)
    title=v['title'].lower()
    v['category']=('Multiplayer' if any(x in title for x in ['multiplayer','online chat','moba','lobby']) else 'AI & simulation' if any(x in title for x in ['neural','learning',' ai','vr','metaverse','metcity','egold']) else 'Games & gameplay' if any(x in title for x in ['trailer','sniper','shark','survival','aveline','cycling','rrts']) else 'Tools & systems')
    return v
with ThreadPoolExecutor(max_workers=8) as pool:e['videos']=list(pool.map(verify,e['videos']))
(ROOT/'portfolio-evidence.json').write_text(json.dumps(e,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=json.loads((ROOT/'profile.json').read_text(encoding='utf-8'))
p['portfolio']=p['siteUrl'];p['previousPortfolio']=e['source']
p['publisher']='https://play.google.com/store/apps/dev?id=6711372526826018293&hl=en'
p['fullName']='Abu Sayed Bin Abdullah';p['location']='Bangladesh'
p['bio']='Game developer from Bangladesh creating published mobile games, Roblox experiences, multiplayer worlds and VR simulations. I turn ideas into responsive gameplay and the systems behind it.'
descriptions={'bullet-rush':'A mobile run-and-gun shooter with enemy waves, weapon upgrades and one-touch controls.','ball-sorting-puzzle':'A colour-sorting puzzle built around simple touch controls and increasingly challenging bottle puzzles.','double-dash':'An arcade driving challenge: steer two cars at once, dodge obstacles and collect power-ups.','bus-stop-rush':'A traffic puzzle about managing buses and passengers at busy city stops.'}
for i,g in enumerate(e['apps']):
    g.update(platform='Android',description=descriptions[g['id']],accent='#c5ff61' if i%2==0 else '#a99cff',symbol=str(i+3).zfill(2),featured=i<2,coverImage=g['images'][0] if g['images'] else g['icon'],publisher='Gamalith Studio',role='Published game')
    if not any(x['id']==g['id'] for x in p['games']):p['games'].append(g)
p['demonstrations']=[v for v in e['videos'] if v['verified']]
p['gallery']=e['gallery']
p['cvUrl']='https://drive.google.com/file/d/1TVAkTZdBTZc5MHnD8kPyGQgVpTpO0IQR/view'
p['education']=[{'qualification':'B.Sc. in Computer Science','institution':'BRAC University','year':'2020'}]
rows=[('Next IT LTD.','Unity Developer','11/2023 – Present','Interactive mini games and smart restaurant systems. Code refactoring, game AI, UI animation, VFX, HDRP optimization and split-screen touch input.'),('Supertal Pte. Ltd.','Senior Game Developer','03/2023 – 10/2023','Persib Bandung metaverse: multiplayer networking, REST APIs, FSM-based NPC interactions, Addressables, asset bundles and Firebase / PlayFab integration.'),('Royex Technologies','Senior Game Developer','08/2022 – 12/2022','Multiplayer metaverse projects, animation blend trees, finite state machines, dedicated servers on AWS, WebGL and in-game voice chat.'),('March Robotics And IT Solutions','Senior Unity Developer','03/2022 – 08/2022','VR training simulations, VR system implementation and databases supporting multiple connections.'),('Hi Tech Bangla, Bangladesh','Unity Game Developer','07/2021 – 12/2021','Tactical communication training simulations with VR / AR integration and radio communication in Unity.'),('Games 4 Life','Unity Game Developer','06/2021 – 10/2021','Hyper-casual games from scratch, game design documentation, localization, in-app purchases and UI.'),('Free Pixel LTD','Game Developer','02/2021 – 06/2021','Live operations and in-game events. Playable ads using Luna Playables, Cocos2d-js and ImpactJS.'),('Zelox Entertainment','Unity Game Developer','08/2020 – 03/2021','2D / 3D game reskins, original Unity games and render pipeline conversion.'),('MediEvil Studio','Game Developer','03/2020 – Present','Hyper-casual games, multiplayer networking, metaverse projects and Unity shaders.')]
p['experience']=[dict(company=c,role=r,dates=d,detail=t) for c,r,d,t in rows]
p['skills'][2]['items']+=['PurrNet','DarkRift 2','REST APIs','Addressables']
p['specialties']=['Gameplay & game systems','Multiplayer & networking','VR & interactive simulation','Unity tools & optimization']
(ROOT/'profile.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared',len(p['games']),'games,',len(p['demonstrations']),'verified videos,',len(p['gallery']),'archive images')
print('Video exclusions:',[(v['youtubeId'],v.get('error')) for v in e['videos'] if not v['verified']])
print('Image contexts:',[(g['image'],g['context'][:90]) for g in p['gallery']])
