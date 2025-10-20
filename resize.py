import os
from PIL import Image, ImageDraw

directory = './train/'

ratio = 0.5

cnt = 0
for name in os.listdir(directory):
  img = Image.open(directory+name)
  w, h = img.size[0], img.size[1]
  res = img.resize((int(w*ratio), int(h*ratio)))
  res.save('./50%/'+name)
  cnt += 1
  print('Done '+str(cnt))