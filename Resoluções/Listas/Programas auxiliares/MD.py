from random import random
from numpy import zeros, copy, sqrt
import sys

# Define arquivo de saida
saida = open('MD.xyz','w')

# Função que escreve a trajetória, que deve ser lida usando o programa VMD
def dump():
    saida.write('{0:d} \n'.format(N))
    saida.write('\n')
    for i in range(N):
        saida.write( '1 {0:.3f} {1:.3f} 0.000 \n'.format( x[i], y[i]) )

# Função que calcula a força entre duas partículas. O primeiro 'if' implementa o raio de cut-off. O 'if' dentro do 'else' é útil em casos onde na configuração inicial existem átomos muito próximos, e evita que átomos saiam da caixa. Recomendo remover este segundo if após ter certeza que a configuração a ser usada é estável.
def f(r):
    if r>rcut:
        return 0.0
    else:
        f = 24.0*eps*( 2.0*(1/r)**(13) -  (1.0/r)**(7))
        if (f<100000):
            return f
        else:
            return 100000.0

# Define as posições iniciais
def init_pos():
    for i in range(N):
        x[i] = L/(Nx) * (i % (Nx)) + random()*rfac*(L/Nx) 
        divy = N/Ny
        y[i] = L/Ny * int((i / divy)) + random()*rfac*(L/Ny) 

# Define as velocidades iniciais
def init_vel():
    for i in range(N):
         vx[i] = 2.0*v0*(random()-0.5)
         vy[i] = 2.0*v0*(random()-0.5)

# Inicializa as posições e velocidades anteriores
def init_prev():
    for i in range(N):
         xprev[i] = x[i]-vx[i]*dt
         yprev[i] = y[i]-vy[i]*dt

# Programa que determina a força resultante sobre cada átomo
def calcforces():
    for j in range(N):
        if (j!=i):
            xji = x[j]-x[i]
            if (xji>0.5*L):
                xji = xji - L
            elif (xji <-0.5*L):
                xji = xji + L
                
            yji = y[j]-y[i]
            if (yji>0.5*L):
                yji = yji - L
            elif (yji <-0.5*L):
                yji = yji + L
            rji = sqrt (xji**2 + yji**2)
            fji = f(rji)
            coseno = -xji/rji
            seno = -yji/rji
            fx[i]+= fji*coseno
            fy[i]+= fji*seno


eps = 1.0
######################### Parâmetros da simulação ########################
# Número de átomos na simulação
N = 4
# Nx e Ny definem como será o arranjo 2D de átomos. N = Nx * Ny
Nx = 2
Ny = 2
# A velocidade inicial dos átomos é aleatória, e se situa no intervalo [-v0,v0]
v0 = 1.0
# A variável abaixo determina quão aleatória pode ser a posição inicial. Valores altos podem gerar configurações iniciais com átomos muito próximos. Valores entre 0 e 0.4 parecem funcionar bem.
rfac = 0.4
# A caixa é assumida quadrada, logo basta fornecer um valor de L
L = 10
# Passo da simulação (time-step)
dt = 0.005
# Número de passos
Npassos = 20000
# Raio de cut-off
rcut = 3.0
# O valor abaixo define o intervalo de tempo entre dois quadros da trajetória
tsave = 0.1

########################### Fim dos parâmetros  ##########################

if (Nx*Ny != N):
    print ("O arranjo escolhido de átomos não é consistente com o número total de átomos.")
    sys.exit()
    
x = zeros(N,float)
y = zeros(N,float)
vx = zeros(N,float)
vy = zeros(N,float)
xprev = zeros(N,float)
yprev = zeros(N,float)
xnew = zeros(N,float)
ynew = zeros(N, float)
fx = zeros(N,float)
fy = zeros(N,float)

init_pos()
init_vel()
init_prev()
    
dump()
t = 0
tol1 = 1.0e-6
tol2 = 1.0e-4

while (t < (Npassos*dt)):
    t+=dt
    for i in range(N):
        fx[i] = 0.0
        fy[i] = 0.0
        calcforces()

        xnew[i] = 2.0*x[i] - xprev[i] + fx[i]*dt**2
        if xnew[i]<0.0:
            xnew[i]+=L
            x[i]+=L 
            xprev[i]+=L
        elif xnew[i] > L:
            xnew[i]-=L
            x[i]-=L
            xprev[i]-=L

        ynew[i] = 2.0*y[i] - yprev[i] + fy[i]*dt**2
        if ynew[i]<0.0:
            ynew[i]+=+L
            y[i]+=L
            yprev[i]+=L
        elif ynew[i] > L:
            ynew[i]-=L
            y[i]-=L
            yprev[i]-=L

        vx[i] = (xnew[i]-xprev[i])/(2*dt)
        vy[i] = (ynew[i]-yprev[i])/(2*dt)

    xprev = copy(x)
    yprev = copy(y)
    x = copy(xnew)
    y = copy(ynew)
    #dump()
    if ((t+tol1)%tsave < tol2):
        print(t)
        dump()
      

saida.close()
