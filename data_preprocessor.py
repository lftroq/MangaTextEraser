# Import here
import os
import numpy as np
from PIL import Image, ImageDraw

directory = './50%/'

cnt = 0
for name in os.listdir(directory):
  if (name.endswith('.jpg') and name.startswith('0')):
    filename = name[2:len(name)-4]

    raw_img_fname = '0_'+filename +'.jpg'
    edited_img_fname = '1_'+filename +'.jpg'

    # Init variable
    edited_img_file = Image.open(directory+edited_img_fname).convert("RGB")
    raw_img_file = Image.open(directory+raw_img_fname).convert("RGB")

    edited_img = edited_img_file.load()
    raw_img = raw_img_file.load()

    img_width = raw_img_file.size[0]
    img_height = raw_img_file.size[1]

    DSU_par = np.zeros((img_height * img_width), dtype = int)
    DSU_sz = np.zeros((img_height * img_width), dtype = int)
    DSU_xl = np.zeros((img_height * img_width), dtype = int)
    DSU_yl = np.zeros((img_height * img_width), dtype = int)
    DSU_xr = np.zeros((img_height * img_width), dtype = int)
    DSU_yr = np.zeros((img_height * img_width), dtype = int)

    def ConvertToOX(u):
      return u[0] * img_height + u[1]

    # u = ConvertToOX({x, y}) (see code in main)
    def Find_set(u):
      if (DSU_par[u]==u):
        return u
      else:
        DSU_par[u] = Find_set(np.array(DSU_par[u]))
        return DSU_par[u]

    # u, v = ConvertToOX({x, y}) (see code in main)
    def Union_set(u, v):
      tu = Find_set(u)
      tv = Find_set(v)
      if(tu == tv):
        return
      if(DSU_sz[tu] < DSU_sz[tv]):
        u, v = v, u
      DSU_sz[tu] += DSU_sz[tv]
      DSU_par[tv] = tu
      DSU_xl[tu] = min(DSU_xl[tu], DSU_xl[tv])
      DSU_xr[tu] = max(DSU_xr[tu], DSU_xr[tv])
      DSU_yl[tu] = min(DSU_yl[tu], DSU_yl[tv])
      DSU_yr[tu] = max(DSU_yr[tu], DSU_yr[tv])

    def Init_DSU(row, col):
      for x in range(row):
        for y in range(col):
          u = ConvertToOX(np.array([x, y]))
          DSU_par[u] = u
          DSU_sz[u] = 1
          DSU_xl[u] = DSU_xr[u] = x
          DSU_yl[u] = DSU_yr[u] = y

    def checkDiff(a, b):
      sumdiff = 0
      for i in range(len(a)): sumdiff += abs(a[i] - b[i])
      return sumdiff > 100

    Init_DSU(img_width, img_height)
    diff = np.zeros([img_width, img_height]).astype(bool)

    # Processing

    for y in range(0, img_height):
      for x in range(0, img_width):
        if checkDiff(edited_img[x, y], raw_img[x, y]):
          diff[x, y] = True
          for xi in range(max(0, x-2), min(img_width, x+2)):
            for yi in range(max(0, y-10), y):
              if (diff[xi, yi] == True):
                Union_set(x * img_height + y, xi * img_height + yi)

    label = ''

    def write(res):
      global label
      label += '0 '
      for x in res:
        label += str(x)+' '
      label = label[:-1]
      label += '\n'

    def convert(box):
      dw = 1./img_width
      dh = 1./img_height
      x, y, w, h = (box[0] + box[1])/2.0, (box[2] + box[3])/2.0, box[1] - box[0], box[3] - box[2]
      x, y, w, h = x*dw, y*dh, w*dw, h*dh
      return (x, y, w, h)

    def drawRec(x, y, img):
      draw = ImageDraw.Draw(img)
      draw.rectangle([x, y], outline = "green", width = 2)
      write(convert((x[0], y[0], x[1], y[1])))

    lim = 1

    for x in range(0, img_width):
      for y in range(0, img_height):
        u = ConvertToOX(np.array([x, y]))
        if (diff[x, y] == False): continue
        if (Find_set(u) == u):
          topLeft_x = max(0, DSU_xl[u]-lim)
          topLeft_y = max(0, DSU_yl[u]-lim)
          bottomRight_x = min(img_width-1, DSU_xr[u]+lim-1)
          bottomRight_y = min(img_height-1, DSU_yr[u]+lim-1)
          drawRec((topLeft_x, topLeft_y), (bottomRight_x, bottomRight_y), raw_img_file)

    f = open('./label/'+'0_'+filename +'.txt', 'w')
    f.write(label)
    f.close()

    raw_img_file.save('./output/'+raw_img_fname)

    cnt += 1
    print('Done '+str(cnt))