import os
ROOT=os.path.dirname(os.path.abspath(__file__))
import re
src=open(os.path.join(ROOT,'src','last-stick.html')).read()
src=src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
head=('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
'<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\'; style-src \'self\' \'unsafe-inline\' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src \'self\' data:; connect-src \'self\' https://vrkdyikakhgmcbzvgtfe.supabase.co; base-uri \'none\'; form-action \'none\'">'
'<meta name="theme-color" content="#16242B"><link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon-192.png" type="image/png"><link rel="apple-touch-icon" href="icon-192.png">'
'<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Last Stick">'
'<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>')
cfg='<script>window.LS_CONFIG={url:"https://vrkdyikakhgmcbzvgtfe.supabase.co",tools:false,key:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZya2R5aWtha2hnbWNienZndGZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE5NzI0MDYsImV4cCI6MjEwNzU0ODQwNn0.Wk1rzEAXZSQNa_FwLAar1dX7r6H7ByIpiDFizJ3OZGs"};</script>'
sw="<script>if('serviceWorker' in navigator&&/^https?:$/.test(location.protocol)){window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});}</script>"
i=src.index('<script>')
out=head+src[:i]+cfg+src[i:]+sw+'</body></html>'
open(os.path.join(ROOT,'index.html'),'w').write(out)
