import numpy.random as rd
import vpython as vp
import numpy as np

rd.seed(1)
# seed(5)

N = 20
J = 1
T = 1 # ou 2
kb = 1
beta = 1
steps = 100000 # 0000

s = np.empty((N,N),int)

for i in range(N):
    for j in range(N):
        if rd.random()<0.5:
            s[i,j]=1
        else:
            s[i,j]=-1
            
def energy(s):

    s1 = s[:-1,:]*s[1:,:]
    s2 = s[:,:-1]*s[:,1:]
    
    E = -J*(np.sum(s1) + np.sum(s2))
    
    return E

E1 = energy(s)
spin_repr = np.empty((N,N),vp.sphere)

for i in range(N):
    for j in range(N):
        spin_repr[i,j] = vp.sphere()
        spin_repr[i,j].pos = i-N//2,j-N//2,0
        
for k in range(steps):
    vp.rate(500)
    i = rd.randint(N)
    j = rd.randint(N)
    
    s[i,j] *=-1
    
    E2 = energy(s)
    
    dE = E2 - E1
    # print(dE)

    if dE >0 :
        if rd.random()< np.exp(-beta*dE):
            E1 = E2 # Podemos flipar os resultados
            M = np.sum(s)
        else:
            s[i,j]*=-1
    else:
        E1 = E2 # Podemos flipar os resultados porque a energia decai.

    if s[i,j]==1:
        spin_repr[i,j].color = vp.color.red
    else:
        spin_repr[i,j].color = vp.color.green