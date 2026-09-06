from PIL import Image, ImageFilter
import numpy as np
from collections import deque
from pathlib import Path
import json

OUT=Path(__file__).parent
SOURCE=OUT/'source'/'generated-sheet.png'
im=Image.open(SOURCE).convert('RGB')
a=np.asarray(im).astype(np.int16)
h,w=a.shape[:2]
# Flood only neutral background connected to the perimeter; enclosed eye whites remain.
neutral=(a.max(2)-a.min(2)<42)&(a.min(2)>145)
bg=np.zeros((h,w),bool)
q=deque()
for x in range(w):
 for y in (0,h-1):
  if neutral[y,x]:bg[y,x]=True;q.append((y,x))
for y in range(h):
 for x in (0,w-1):
  if neutral[y,x] and not bg[y,x]:bg[y,x]=True;q.append((y,x))
while q:
 y,x=q.popleft()
 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
  if 0<=yy<h and 0<=xx<w and neutral[yy,xx] and not bg[yy,xx]:
   bg[yy,xx]=True;q.append((yy,xx))
rgba=np.dstack((a.astype(np.uint8),np.where(bg,0,255).astype(np.uint8)))
clean=Image.fromarray(rgba)
clean.putalpha(clean.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.35)))
# The generated sheet has seven columns. Explicit observed row boundaries avoid cutting poses.
xs=[0,177,331,487,642,797,951,1136]
ys=[0,164,320,478,649,817,958,1108,1260,1385]
rows=[]
for r in range(9):
 row=[]
 for c in range(7):
  tile=clean.crop((xs[c],ys[r],xs[c+1],ys[r+1]))
  box=tile.getbbox()
  if box:tile=tile.crop(box)
  # Consistent pixel scale preserves breathing and other pose changes.
  scale=min(1.07,170/tile.width,186/tile.height)
  tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
  frame=Image.new('RGBA',(192,208))
  frame.alpha_composite(tile,((192-tile.width)//2,198-tile.height))
  row.append(frame)
 rows.append(row)
# Reuse the complete waiting pose for review: the generated final row was clipped at the feet.
rows[8]=[x.copy() for x in rows[6]]
counts=[6,8,8,4,5,8,6,6,6]
sheet=Image.new('RGBA',(1536,1872))
for r,n in enumerate(counts):
 for c in range(8):
  idx=round(min(c,n-1)*6/(n-1))
  sheet.alpha_composite(rows[r][idx],(192*c,208*r))
sheet.save(OUT/'spritesheet.png')
rows[0][0].resize((384,416),Image.Resampling.LANCZOS).save(OUT/'preview.png')
frames=[rows[0][i].resize((384,416),Image.Resampling.LANCZOS) for i in range(6)]
frames[0].save(OUT/'preview.webp',save_all=True,append_images=frames[1:],duration=[700,350,350,200,200,700],loop=0,lossless=True)
(OUT/'pet.json').write_text(json.dumps({'displayName':'肥嘟嘟 · 美团袋鼠','description':'参考美团袋鼠肥嘟嘟原头像与表情图制作的本地桌宠','spriteVersionNumber':1,'spritesheetPath':'spritesheet.png'},ensure_ascii=False,indent=2))
assert sheet.size==(1536,1872) and sheet.mode=='RGBA'
assert sheet.getextrema()[3]==(0,255)
print('Validated transparent 1536 x 1872 sheet, 8 x 9 cells')
