import json,re
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse
DOCS=[]
def chunk_text(text,source='粘贴文档'):
    parts=[p.strip() for p in re.split(r'\n\s*\n|(?<=[。！？.!?])\s+',text) if p.strip()]
    return [{'id':len(DOCS)+i+1,'source':source,'text':p} for i,p in enumerate(parts)]
def terms(s): return set(re.findall(r'[\w一-龥]{2,}',s.lower()))
def retrieve(q,k=4):
    qt=terms(q); scored=[]
    for d in DOCS:
        dt=terms(d['text']); score=len(qt&dt)/(len(qt) or 1)
        if score: scored.append((score,d))
    return [d for _,d in sorted(scored,key=lambda x:x[0],reverse=True)[:k]]
HTML='''<!doctype html><meta charset="utf-8"><title>企业级 RAG 问答系统</title><style>body{font:16px system-ui;max-width:1000px;margin:30px auto;background:#f5f7fb;color:#172033}textarea,input{width:100%;padding:12px;margin:6px 0;border:1px solid #ccd5e2;border-radius:8px}button{padding:10px 16px;background:#285de8;color:white;border:0;border-radius:8px;cursor:pointer}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:white;padding:20px;border-radius:14px;box-shadow:0 4px 18px #12254d12}.hit{border-left:4px solid #285de8;padding:10px;margin:9px 0;background:#f0f4ff}@media(max-width:700px){.grid{grid-template-columns:1fr}}</style><h1>企业级 RAG 问答系统</h1><p>本地复现：导入 → 切分 → 检索 → 引用式回答</p><div class=grid><section class=card><h2>1. 文档入库</h2><input id=src placeholder="来源名称，例如 product.md"><textarea id=doc rows=12 placeholder="粘贴企业知识库文档..."></textarea><button onclick=ingest()>建立索引</button><p id=status></p></section><section class=card><h2>2. 检索问答</h2><input id=q placeholder="输入问题，例如：退款期限是多少？"><button onclick=ask()>检索并回答</button><div id=out></div></section></div><script>async function ingest(){let r=await fetch('/ingest',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({source:src.value||'粘贴文档',text:doc.value})});status.textContent=(await r.json()).message}async function ask(){let r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:q.value})});let x=await r.json();out.innerHTML='<h3>回答</h3><p>'+x.answer+'</p><h3>引用片段</h3>'+x.hits.map(h=>'<div class=hit><b>'+h.source+'</b><br>'+h.text+'</div>').join('')}</script>'''
class H(BaseHTTPRequestHandler):
 def do_GET(self): self.send_response(200);self.send_header('Content-Type','text/html;charset=utf-8');self.end_headers();self.wfile.write(HTML.encode())
 def do_POST(self):
  n=int(self.headers.get('Content-Length',0)); x=json.loads(self.rfile.read(n)); global DOCS
  if self.path=='/ingest': DOCS.extend(chunk_text(x.get('text',''),x.get('source','文档'))); out={'message':f'已建立索引，当前 {len(DOCS)} 个片段'}
  else:
   hits=retrieve(x.get('q','')); out={'answer':'根据检索到的内容：'+('；'.join(h['text'] for h in hits) if hits else '没有找到相关片段，请补充文档或换个问法。'),'hits':hits}
  self.send_response(200);self.send_header('Content-Type','application/json;charset=utf-8');self.end_headers();self.wfile.write(json.dumps(out,ensure_ascii=False).encode())
HTTPServer(('127.0.0.1',8097),H).serve_forever()
