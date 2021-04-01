import matplotlib.pyplot as plt
from vpython import *
import random as rd
import numpy as np
import time


tau = 10000
T0 = 1000
N = 50

def cool_T(t):
    return T0 * np.exp(-t/tau)

grid = np.zeros([N,N], int)
grid_vert = np.zeros([N,N], bool)

def loc_Dim(t):
    pos_x, pos_y = rd.randint(0,N-2), rd.randint(0,N-2)
    side, down = 1, 1
    vert = 0
    
    if pos_x == N-1:
        side = -side
    elif pos_y == N-1:
        down = -down
        
    if rd.choice(['side','down']) == 'side':
        vert = -1
        dim = [[pos_x, pos_y], [pos_x+side, pos_y]]
    else:
        vert = 1
        dim = [[pos_x, pos_y], [pos_x, pos_y+down]]
    
    if grid[dim[0][0],dim[0][1]] == 0 and grid[dim[1][0],dim[1][1]] == 0:
        grid[dim[0][0],dim[0][1]], grid[dim[1][0],dim[1][1]] = 1, 1
        grid_vert[dim[0][0],dim[0][1]], grid_vert[dim[1][0],dim[1][1]] = vert, vert
        
        return 1
        
    elif grid[dim[0][0],dim[0][1]] != 0 and grid[dim[1][0],dim[1][1]] != 0:
        if anly(t) == True:
            if grid_vert[dim[0][0],dim[0][1]] == vert and grid_vert[dim[1][0],dim[1][1]] == vert:
                grid[dim[0][0],dim[0][1]], grid[dim[1][0],dim[1][1]] = 0, 0
                grid_vert[dim[0][0],dim[0][1]], grid_vert[dim[1][0],dim[1][1]] = 0, 0
                
                return -1
            
            return 0
        else:
            return 0
        
    elif grid[dim[0][0],dim[0][1]] == 0 and grid[dim[1][0],dim[1][1]] != 0:
        
        return 0
    elif grid[dim[0][0],dim[0][1]] != 0 and grid[dim[1][0],dim[1][1]] == 0:
        
        return 0

def anly(t):
    if P_a(1000, 0, cool_T(t)) > rd.random():
        return True
    else:
        return False

def P_a(E_j, E_i, T):
    beta = 1/T
    
    if E_j <= E_i:
        return 1
    else:
        return np.exp(-beta*(E_j - E_i))

t = 0
eps = 1e-5
pontE = []
t0 = time.time()
dimers = 0

while eps <= cool_T(t):
    t += 1
    dimers += loc_Dim(t)
    pontE.append(-dimers) 
    
t1 = time.time()

N = 20
grid = np.zeros([N,N], int)
grid_vert = np.zeros([N,N], int)

my_scene = canvas(title='Cobrimento de dímeros',
     width=600, height=200,
     center=vector(0,0,0),
     background=color.black)

for i in range(N):
    for j in range(N):
        ball = sphere(pos=vector(i,j,0),
                        radius=0.2,
                        color=vector(255,255,255))

def putDim(t):
    pos_x, pos_y = rd.randint(0,N-2), rd.randint(0,N-2)
    side, down = 1, 1
    vert = 0
    if pos_x == N-1:
        side = -side
    elif pos_y == N-1:
        down = -down
        
    if rd.choice(['side','down']) == 'side':
        vert = -1
        dim = [[pos_x, pos_y], [pos_x+side, pos_y]]
    else:
        vert = 1
        dim = [[pos_x, pos_y], [pos_x, pos_y+down]]
    
    if grid[dim[0][0],dim[0][1]] == 0 and grid[dim[1][0],dim[1][1]] == 0:
        grid[dim[0][0],dim[0][1]], grid[dim[1][0],dim[1][1]] = 1, 1
        if vert == 1:
            for p in range(2):
                ball = sphere(pos=vector(dim[p][0],dim[p][1],0),
                            radius=0.2,
                            color=vector(50,0,0))
            grid_vert[dim[0][0],dim[0][1]], grid_vert[dim[1][0],dim[1][1]] = vert, vert
            
        elif vert == -1:
            for p in range(2):
                ball = sphere(pos = vector(dim[p][0],dim[p][1],0),
                            radius = 0.2,
                            color = vector(0,0,50))
            grid_vert[dim[0][0],dim[0][1]], grid_vert[dim[1][0],dim[1][1]] = vert, vert
        return 1
        
    elif grid[dim[0][0],dim[0][1]] != 0 and grid[dim[1][0],dim[1][1]] != 0:
    
        if anly(t) == True:
            if grid_vert[dim[0][0],dim[0][1]] == vert and grid_vert[dim[1][0],dim[1][1]] == vert:
                grid[dim[0][0],dim[0][1]], grid[dim[1][0],dim[1][1]] = 0, 0
                grid_vert[dim[0][0],dim[0][1]], grid_vert[dim[1][0],dim[1][1]] = 0, 0
                for p in range(2):
                    ball = sphere(pos=vector(dim[p][0],dim[p][1],0),
                                radius=0.2,
                                color=vector(255,255,255))
                return -1
            return 0
        else:
            return 0
        
    elif grid[dim[0][0],dim[0][1]] == 0 and grid[dim[1][0],dim[1][1]] != 0:
        return 0
    elif grid[dim[0][0],dim[0][1]] != 0 and grid[dim[1][0],dim[1][1]] == 0:
        return 0

t = 0
eps = 1e-5
while eps <= cool_T(t):
    t += 1
    loc_Dim(t)
t1 = time.time()