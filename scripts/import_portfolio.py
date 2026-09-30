"""Import public portfolio evidence and store media. Run explicitly, not in CI."""
import json, re, urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'sources'/'portfolio'
OUT.mkdir(parents=True,exist_ok=True)
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
def image(url,name):
    from PIL import Image
    import io
    p=OUT/(name+'.webp')
    Image.open(io.BytesIO(fetch(url))).convert('RGB').save(p,'WEBP',quality=85)
    return str(p.relative_to(ROOT)).replace('\\','/')
old='https://sites.google.com/view/sayedturzo'
soup=BeautifulSoup(fetch(old),'html.parser')
videos=[]
for frame in soup.select('iframe[src]'):
    match=re.search(r'youtube.com/embed/([\w-]{11})',frame['src'])
    if match and not any(v['youtubeId']==match[1] for v in videos):
        videos.append({'youtubeId':match[1],'title':frame.get('title','Project demonstration'),'source':old})
gallery=[]
for i,img in enumerate(soup.select('img[src]')):
    if 'sitesv-images' not in img['src']:continue
    parent=img.find_parent('section') or img.parent.parent
    text=parent.get_text(' ',strip=True)
    try:gallery.append({'image':image(img['src'],f'archive-{i:02}'),'context':text[:500],'source':old})
    except Exception as e:print('Image skipped:',i,str(e))
apps=[]
packages=['com.sae.bulletrush','com.sae.ballsorting','com.SAE.DoubleDash','com.sae.busstoprush','com.SAE.splatball','com.Saestudio.tipsyway']
for package in packages:
    url='https://play.google.com/store/apps/details?id='+package+'&hl=en'
    try:
        s=BeautifulSoup(fetch(url),'html.parser')
        title=s.select_one('h1').get_text(' ',strip=True)
        shots=[]
        for img in s.select('img[alt="Screenshot image"]'):
            src=img.get('src')
            if src and src not in shots:shots.append(src)
        slug=re.sub('[^a-z0-9]+','-',title.lower()).strip('-')
        local=[image(src,slug+'-'+str(i)) for i,src in enumerate(shots)]
        icon=s.select_one('img[alt="Icon image"]')
        if icon:icon=image(icon['src'],slug+'-icon')
        yt=re.findall(r'(?:youtube.com/embed/|youtu.be/)([\w-]{11})',str(s))
        apps.append({'title':title,'id':slug,'url':url,'images':local,'icon':icon,'youtubeId':yt[0] if yt else None})
        print(title,len(local),'screenshots')
    except Exception as e:print('App skipped:',package,str(e))
evidence={'source':old,'videos':videos,'gallery':gallery,'apps':apps}
(ROOT/'portfolio-evidence.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Imported',len(videos),'videos,',len(gallery),'archive images,',len(apps),'apps')
