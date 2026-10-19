"""Build the static archive from Markdown + characters.json.
Run: python -m pip install -r library/requirements.txt && python library/build.py
Generated HTML requires no client-side dependencies or network requests.
"""
from pathlib import Path
import html,json,re,posixpath
from urllib.parse import urlsplit,unquote
import markdown
ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/'library'
m=json.loads((LIB/'characters.json').read_text(encoding='utf-8'))
# Shared profiles appear once, while all member names remain searchable.
by_profile={}
for entry in m['characters']:
 if entry.get('publication_hold'):continue
 key=entry['profile']
 if key not in by_profile:
  by_profile[key]=dict(entry)
  by_profile[key]['aliases']=list(entry.get('aliases',[]))+[entry['id'],entry['name']]
 else:
  by_profile[key]['aliases']+=list(entry.get('aliases',[]))+[entry['id'],entry['name']]
for entry in by_profile.values():
 if entry['profile']=='characters/gille-and-coffeeblender.md':
  entry['id']='gille-and-coffeeblender'
  entry['name']='Gille & CoffeeBlender'
 entry['aliases']=list(dict.fromkeys(entry['aliases']))
cast=sorted(by_profile.values(),key=lambda c:c['name'].casefold())
esc=html.escape

# The manifest drives both front doors, not just the website.
rows=[]
directory='# All Nous characters\n\n[← Archive home](../README.md) · [Search the visual library](../library/index.html)\n\nOne alphabetical cast. Every name opens a readable profile; downloads are optional. Doge Man, Super Shiba and 123mikeyD are one character.\n\n'
for c in cast:
 image=f'<img src="./{esc(c["browse_preview"])}" alt="{esc(c["name"])} reference artwork" width="180"><br>' if c.get('browse_preview') else 'Artwork not yet available<br>'
 # Front-page curation only; retain the archived profile and directory entry.
 if c['profile'] != 'characters/heartbreaker.md':
  rows.append(f'<td align="center"><a href="./{esc(c["profile"])}">{image}<strong>{esc(c["name"])}</strong></a></td>')
 directory+=f'- [{c["name"]}](./{Path(c["profile"]).name})'
 if c.get('aliases'):directory+=' — '+', '.join(dict.fromkeys(c['aliases']))
 directory+='\n'
(ROOT/'characters/README.md').write_text(directory,encoding='utf-8')
table='<table>\n'+'\n'.join('<tr>\n'+'\n'.join(rows[i:i+4])+'\n</tr>' for i in range(0,len(rows),4))+'\n</table>'
readme=ROOT/'README.md';text=readme.read_text(encoding='utf-8')
text=re.sub(r'(?<=<!-- BEGIN GENERATED CHARACTER GALLERY -->).*?(?=<!-- END GENERATED CHARACTER GALLERY -->)','\n'+table+'\n',text,flags=re.S)
readme.write_text(text,encoding='utf-8')

def relative(target, output):
 return posixpath.relpath(target, posixpath.dirname(output))

def document(title,body,output,description='Read the NRCU community archive. Profiles, artwork and stories; no model download required.'):
 css=relative('library/archive.css',output)
 return '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="'+esc(description)+'"><title>'+esc(title)+' · NRCU</title><link rel="stylesheet" href="'+css+'"></head><body>'+body+'</body></html>\n'

def header(output):
 home=relative('library/index.html',output)
 return '<a class="skip" href="#content">Skip to content</a><div class="shell"><header class="topbar"><a class="brand" href="'+home+'">NRCU / ARCHIVE</a><nav aria-label="Archive"><a href="'+home+'">All Nous</a><a href="https://github.com/123mikeyd/Nous_Research_Cinematic_Universe">GitHub</a></nav></header>'

cards=[]
for c in cast:
 note='Reference artwork'
 if c.get('visual_status')=='supplementary-reference-art':note='Supplementary art · story inside'
 if c['id']=='teknium':note='Established head reference'
 if c['id']=='fatcat':note='Concept art · story role open'
 if c['id']=='doge-man':note='Also Super Shiba / 123mikeyD'
 if c['id']=='ee-dd':note='Selected landscape avatar'
 if c['id']=='drahcir-rahl':note='The IT Juggernaut'
 pic='<div class="art"><img loading="lazy" src="../'+esc(c['browse_preview'])+'" alt="'+esc(c['name'])+' reference artwork"></div>' if c.get('browse_preview') else '<div class="art empty">Artwork not yet available</div>'
 search=' '.join([c['id'],c['name']]+c.get('aliases',[]))
 cards.append('<article class="card" data-id="'+esc(c['id'])+'" data-search="'+esc(search)+'"><a href="'+relative(c['reader'],'library/index.html')+'">'+pic+'<h2>'+esc(c['name'])+'</h2><p>'+esc(note)+'</p><span class="read">Read profile <span aria-hidden="true">↗</span></span></a></article>')
body=header('library/index.html')+'''<main id="content"><section class="intro" aria-labelledby="title"><div><span class="eyebrow">Nous Research Cinematic Universe</span><h1 id="title">All Nous.<br>Every character.</h1></div><p>A community-built universe, ready to explore.<br>Find a familiar face or meet someone new. Open any character to read their story and see the art—no downloads needed.</p></section><div class="toolbar"><div class="search-wrap"><label for="search">Find a character by name or alias</label><input type="search" id="search" placeholder="Try Teknium, TurboFit, or Super Shiba…" autocomplete="off" aria-controls="characters"></div><button id="reset" type="button">Clear search</button></div><div class="results"><span id="count" role="status" aria-live="polite">'''+str(len(cast))+''' profiles</span><span>Alphabetical · One Nous cast</span></div><section id="characters" class="grid" aria-label="All Nous characters">'''+''.join(cards)+'''</section><section id="empty" class="empty-results" hidden><h2>No characters found</h2><p>Try a shorter name or an alias, or clear the search to see everyone.</p><button id="empty-reset" type="button">Show all characters</button></section><noscript><p>All characters are shown above. Enable JavaScript for instant search, or use your browser’s Find command.</p></noscript></main><footer class="archive-footer"><nav><a href="read/README.html">Stories, videos &amp; archive guide</a><a href="read/README.html#optional-3d-model-downloads">Optional model downloads</a><a href="read/CONTENT-NOTICE.html">Content notice</a><a href="https://123mikeyd.github.io/nrcu-platform-fighter/">Play the NRCU fighter</a></nav><p>Unofficial, fan-made, and made for the love of the craft. Original references and credits stay with each profile.</p></footer></div><script src="archive.js"></script>'''
(LIB/'index.html').write_text(document('All Nous — Character Library',body,'library/index.html'),encoding='utf-8')
# Individually gated supplementary art is generated from explicit per-sheet approval.
# Generate Markdown too, so the source page cannot expose pending variants.
for c in m['characters']:
 if c.get('publication_hold') or c.get('alternate_art_approval')!='individual-Mike-review-required':continue
 source=c['sheets_page']
 text=f'# {c["name"]} — Supplementary art\n\n[Character profile and established reference]({relative(c["profile"],source)}) · [Visual library]({relative("library/index.html",source)})\n\nIndividually approved supplementary art. The established primary reference and character lore remain unchanged.\n'
 for sheet in c.get('sheets',[]):
  if sheet.get('approval_status')!='approved-supplementary':continue
  label=sheet['label'];preview=relative(sheet['preview'],source)
  original=relative(sheet.get('original',sheet['preview']),source)
  text+=f'\n## {label}\n\n[![{c["name"]} — {label}]({preview})]({original})\n'
  if sheet.get('credit_markdown'):text+='\n'+sheet['credit_markdown']+'\n'
 text+='\n[Content notice]('+relative('CONTENT-NOTICE.md',source)+').\n'
 (ROOT/source).write_text(text,encoding='utf-8')
# All Markdown is rendered so profile cross-links stay readable locally and on Pages.
# A publication hold omits that character and its art pages from generated browsing.
held={c['profile'] for c in m['characters'] if c.get('publication_hold')}
held|={c.get('sheets_page','') for c in m['characters'] if c.get('publication_hold')}
# Remove stale generated readers when a previously visible character is held.
for source in held - {''}:
 stale=ROOT/('library/read/'+source.replace('.md','.html'))
 if stale.exists():stale.unlink()
files=[p for folder in ['characters','scenes','music-videos','squad'] for p in (ROOT/folder).rglob('*.md')]+[ROOT/'README.md',ROOT/'CONTENT-NOTICE.md']
for p in files:
 source=p.relative_to(ROOT).as_posix()
 if source in held:continue
 output='library/read/'+source.replace('.md','.html');dest=ROOT/output
 text=p.read_text(encoding='utf-8')

 rendered=markdown.markdown(text,extensions=['tables','fenced_code','toc'])
 # Optional download sections are collapsed, after the reading content.
 rendered=re.sub(r'(<h2 id="optional-3d-model-download">.*?)(?=<h2 |\Z)',lambda x:'<details><summary>Optional 3D model download</summary>'+re.sub(r'^<h2.*?</h2>','',x[1],flags=re.S)+'</details>',rendered,flags=re.S)
 def link(match):
  attr,url=match[1],html.unescape(match[2]);parsed=urlsplit(url)
  if parsed.scheme or parsed.netloc or url.startswith('#'):return match[0]
  target=posixpath.normpath(posixpath.join(posixpath.dirname(source),unquote(parsed.path)))
  if target in held:return attr+'="'+relative('library/index.html',output)+'"'
  if target.endswith('.md'):target='library/read/'+target[:-3]+'.html'
  elif target in ['scenes','music-videos','squad','images']:return attr+'="https://github.com/123mikeyd/Nous_Research_Cinematic_Universe/tree/main/'+target+'"'
  result=relative(target,output)
  if parsed.fragment:result+='#'+parsed.fragment
  return attr+'="'+esc(result)+'"'
 rendered=re.sub(r'(href|src)="([^"]*)"',link,rendered)
 # Reading images remain uncropped; lazy loading keeps long art collections light.
 rendered=rendered.replace('<img ','<img loading="lazy" ')
 # Standalone reference art opens at its original resolution, without a download CTA.
 rendered=re.sub(r'<p>(<img [^>]+>)</p>', lambda hit: '<figure><a href="'+re.search(r'src="([^"]+)"',hit[1])[1]+'" aria-label="Open full-size reference artwork">'+hit[1]+'</a><figcaption>Reference artwork · select to view full size</figcaption></figure>', rendered)
 title=re.search(r'^# (.+)',text,re.M)[1]
 body=header(output)+'<main id="content" class="reader"><a class="back" href="'+relative('library/index.html',output)+'">← All Nous characters</a>'+rendered+'<hr><p class="source"><a href="'+relative(source,output)+'">Original Markdown</a> · <a href="'+relative('library/index.html',output)+'">Back to the character library</a></p></main></div>'
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('\n'.join(line.rstrip() for line in document(title,body,output).splitlines())+'\n',encoding='utf-8')
print(json.dumps({'characters':len(cast),'readers':len(files)-len(held- {''}),'gallery':'library/index.html'}))
