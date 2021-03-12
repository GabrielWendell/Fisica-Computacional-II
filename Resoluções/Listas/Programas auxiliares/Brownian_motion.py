import vpython as vp
import random as rd
import numpy as np

L = 101

i = 50
j = 50

d = vp.canvas()
s = vp.sphere()

s.pos = vp.vector(i,j,0)
d.autoscale = False

for t in np.arange(1e6):
    vp.rate(30)
    s.pos = vp.vector(i-50, j-50, 0)
    a = rd.randint(1,4)
    
    if a == 1: 
        if i == L: continue
        i += 1
    elif a == 2:
        if i == 0: continue
        i -= 1
    elif a == 3:
        if j == L: continue
        j += 1
    elif a == 4:
        if j == 0: continue
        j -= 1