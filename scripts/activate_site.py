"""Activate README play links only after the deployed page responds correctly."""
from pathlib import Path
import json, time, urllib.request
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'profile.json'
p=json.loads(path.read_text(encoding='utf-8'))
for attempt in range(6):
    try:
        with urllib.request.urlopen(p['siteUrl'],timeout=15) as response:
            page=response.read().decode('utf-8')
        if 'id="snake"' not in page:raise RuntimeError('Deployed page does not contain the game')
        p['sitePublished']=True
        path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('Verified playable site; activating public README links.')
        break
    except Exception:
        if attempt==5:raise
        time.sleep(5)
