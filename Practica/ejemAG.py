import random
import math

def Alg_Genetico(ecuacion, l,M,K, p_mut):
    pob = genera(l,K)
    probab = eval_apt(pob, l, ecuacion)
    i=0
    while i<M:
        n_pob = seleccion(pob, probab)
        hijos = cruce(n_pob)
        pob = mutacion(hijos, p_mut, l)
        probab = eval_apt(pob, l, ecuacion)
        i=i+1
    return pob


def genera(l, k):
    pob = [[random.randint(0, 1) for _ in range(l)] for _ in range(k)]
    return pob

def eval_apt(pob, l, ecuacion):
    apt_crom = []
    apt_pob = 0
    for i in range(len(pob)):
        crom = pob[i]
        apt = evalua(crom, l, ecuacion)
        apt_pob += apt
        apt_crom.append(apt)
    probab=[]
    for i in range(len(pob)):
        prob_crom = apt_crom[i] / apt_pob
        probab.append(prob_crom)
    return probab

def evalua(crom, l, ecuacion):
    x = decodifica(crom, l)
    y = ecuacion(x)
    apt = 15 - abs(y)
    return apt

def ecuacion(x):
    valor = 5*x**5 - 3*x**4 - x**3 - 5*x**2 - x - 3
    return valor

def decodifica(crom, l):
    xi = 0.5
    xf = 1.5
    Max = 2 ** l
    cromPot = [crom[i] * 2**(l-i-1) for i in range(l)]
    valorDecimal = sum(cromPot)
    valDeco = ((xf - xi)/Max) * (valorDecimal) + xi
    return valDeco

def seleccion(pob, probab):
    j = 0
    K = len(pob)
    limite = 2 * max(probab)
    pob_nueva = []
    while j < K:
        i = 0
        while i < K:
            aleat = random.uniform(0, limite)
            if probab[i] > aleat:
                pob_nueva.append(pob[j])
                j += 1
                if j >= K:
                    break
            i += 1
            if i == K:
                i = 0
    return pob_nueva

def cruce(pob_nueva):
    i = 0
    K = len(pob_nueva)
    hijos = []
    while i < K-1:
        crom1 = pob_nueva[i]
        crom2 = pob_nueva[i+1]
        pt = random.randint(1, len(crom1)-1)
        hijo1 = crom1[:pt] + crom2[pt:]
        hijo2 = crom2[:pt] + crom1[pt:]
        hijos.append(hijo1)
        hijos.append(hijo2)
        i=i+2
    return hijos

def mutacion(hijos, p_mut, l):
    K = len(hijos)
    totalbits = K * l
    segmento = 1/p_mut
    n_mutaciones = int(totalbits / segmento)
    i = 0
    while i < n_mutaciones:
        muta = random.randint(0, totalbits-1)
        x = math.floor(muta/l)
        y = muta % l
        hijos[x][y] = 1 - hijos[x][y]
        i += 1
    return hijos

if __name__ == "__main__":
    resultado = Alg_Genetico(ecuacion, l=8, M=50, K=10, p_mut=0.05)
    print("Poblacion final: ", resultado)