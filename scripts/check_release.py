"""Regression check: a published page must use one complete immutable release."""
import hashlib, json, re
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'site'
page=(root/'index.html').read_text(encoding='utf-8')
scripts=re.findall(r'src="(releases/([a-f0-9]{16})/app.js)"',page)
styles=re.findall(r'href="(releases/([a-f0-9]{16})/styles.css)"',page)
assert len(scripts)==len(styles)==1,'HTML must reference versioned JS and CSS'
assert scripts[0][1]==styles[0][1],'JS and CSS must belong to one release'
files=['app.js','portfolio.js','snake-engine.mjs','styles.css','profile.json']
contents=[(root/name).read_bytes() for name in files]
revision=hashlib.sha256(b''.join(contents)).hexdigest()[:16]
assert scripts[0][1]==revision,'HTML release must match current content'
release=root/'releases'/revision
for name,data in zip(files,contents):
    assert (release/name).read_bytes()==data, f'{name} is missing or stale in release'
    changed=contents.copy();changed[files.index(name)]=data+b' '
    assert hashlib.sha256(b''.join(changed)).hexdigest()[:16]!=revision
assert "new URL('./profile.json',import.meta.url)" in (release/'app.js').read_text(encoding='utf-8'),'JSON must resolve within the same release, not the document root'
p=json.loads((release/'profile.json').read_text(encoding='utf-8'))
assert p['games'] and p['demonstrations'] and p['archiveProjects']
for g in p['games']:
    for image in [g['coverImage'],*g.get('images',[])]:assert (root/image).is_file(),image
print('Release consistency, cache invalidation, content and local image paths passed:',revision)
