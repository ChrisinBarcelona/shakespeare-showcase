import xml.etree.ElementTree as ET, json, re, sys
M='/tmp/shakespeare-material/texts/moby/'
want={ # id: (file, act, scene)
 'mac13':('macbeth',1,3),'mac32':('macbeth',3,2),'mac55':('macbeth',5,5),'mac41':('macbeth',4,1),
 'ham13':('hamlet',1,3),'ham31':('hamlet',3,1),'ham34':('hamlet',3,4),'ham45':('hamlet',4,5),'ham47':('hamlet',4,7),'ham51':('hamlet',5,1),'ham52':('hamlet',5,2),
 'mnd21':('midsummer_nights_dream',2,1),'mnd32':('midsummer_nights_dream',3,2),
 'shr21':('taming_of_the_shrew',2,1),'r312':('richard_iii',1,2),'cor45':('coriolanus',4,5),'ayl21':('as_you_like_it',2,1)}
def txt(e): return ''.join(e.itertext()).strip()
out={}
for k,(f,a,s) in want.items():
  root=ET.parse(M+f+'_moby.xml').getroot()
  acts=root.findall('ACT');act=acts[a-1];scenes=act.findall('SCENE');sc=scenes[s-1]
  items=[]
  for el in sc:
    if el.tag=='TITLE': title=txt(el)
    elif el.tag=='STAGEDIR': items.append({'d':txt(el)})
    elif el.tag=='SPEECH':
      sp=[txt(x) for x in el.findall('SPEAKER')]
      lines=[]
      for x in el:
        if x.tag=='LINE': lines.append(txt(x))
        elif x.tag=='STAGEDIR': lines.append('['+txt(x)+']')
      items.append({'s':' / '.join(sp),'l':lines})
  out[k]={'play':txt(root.find('TITLE')),'act':a,'scene':s,'title':title,'items':items}
json.dump(out,open('scenes.json','w'))
# speaker word counts
for k,v in out.items():
  c={}
  for it in v['items']:
    if 's' in it:
      w=sum(len(re.sub(r'\[.*?\]','',l).split()) for l in it['l'])
      c[it['s']]=c.get(it['s'],0)+w
  print(k,v['title'][:40],sorted(c.items(),key=lambda x:-x[1])[:9])
