"""Read-only audit of public profile links. Does not delete links or modify content."""
from pathlib import Path
import json, re, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'profile.json').read_text(encoding='utf-8'))
links=[{'name':g['title'],'url':g['url']} for g in p['games']+p['worlds']]
links += [{'name':key,'url':p[key]} for key in ['portfolio','linkedin','siteUrl'] if p.get(key)]
links += [{'name':'GitHub','url':'https://github.com/'+p['username']}]
def check(link):
    result=dict(link)
    try:
        req=urllib.request.Request(link['url'],headers={'User-Agent':'Mozilla/5.0 (compatible; ProfileLinkAudit/1.0)'})
        with urllib.request.urlopen(req,timeout=20) as response:
            text=response.read(500000).decode('utf-8',errors='replace')
            title=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
            result.update(status=response.status,finalUrl=response.url,title=re.sub(r'\s+',' ',title.group(1)).strip() if title else '',signals=[s for s in ['not found','not available','no longer available','this site can’t be reached','domain for sale'] if s in text.lower()])
    except urllib.error.HTTPError as error:result.update(status=error.code,error=str(error))
    except Exception as error:result.update(status=None,error=str(error))
    return result
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,links))
path=ROOT/'tmp'/'link-audit.json';path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for result in results:print(json.dumps(result,ensure_ascii=False))
