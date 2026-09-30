"""Optional: fetch public Roblox thumbnails for Roblox games in profile.json."""
from pathlib import Path
import json, urllib.request, re
ROOT=Path(__file__).resolve().parents[1]
profile=json.loads((ROOT/'profile.json').read_text(encoding='utf-8'))
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'SayedTurzo-profile/1.0'}),timeout=30).read()
for game in profile['games']:
    if game['platform']!='Roblox': continue
    place=re.search(r'/games/(\d+)',game['url']).group(1)
    universe=json.loads(get(f'https://apis.roblox.com/universes/v1/places/{place}/universe'))['universeId']
    result=json.loads(get(f'https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe}&countPerUniverse=1&defaults=true&size=768x432&format=Png&isCircular=false'))
    thumbnail=result['data'][0]['thumbnails'][0]
    if thumbnail['state']!='Completed': raise RuntimeError('Thumbnail not ready: '+game['title'])
    path=ROOT/'assets'/'sources'/(game['id']+'.png');path.parent.mkdir(exist_ok=True)
    path.write_bytes(get(thumbnail['imageUrl']))
    game['coverImage']='assets/sources/'+game['id']+'.png'
    print('Saved public thumbnail:',game['title'])
(ROOT/'profile.json').write_text(json.dumps(profile,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
