from collections import deque
import pandas as pd

data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=';', )
data.harassmentRisk = data.harassmentRisk.fillna(data.harassmentRisk.mean())
grafito = {}
origenes_1 = data.origin.unique()

for i in range(len(origenes_1)):
    grafito[origenes_1[i]] = {}


for i in data.index:
    if data["oneway"][i] == True:
        grafito[data["origin"][i]][data["destination"][i]] = (data["length"][i], data["harassmentRisk"][i])
        try:
            grafito[data["destination"][i]][data["origin"][i]] = (data["length"][i], data["harassmentRisk"][i])
        except KeyError:
            grafito[data['destination'][i]] = {data["origin"][i]: (data["length"][i], data["harassmentRisk"][i])}
    else:
        grafito[data["origin"][i]][data["destination"][i]] = (data["length"][i], data["harassmentRisk"][i])

def Camino(primero, k):
    if primero[k] == -1:
        print(k, end="->")
        return
    Camino(primero, primero[k])
    print(k, end="->")


def Vertices(primero, k):
    if primero[k] == -1:
        return 0
    else:
        return 1 + Vertices(primero, primero[k])


def Distancia(origen, destino, grafo):
    distancia = dict()
    primero = dict()
    sin_visitar = deque()
    for i in range(0, len(grafo)):
        num=grafo[i]
        primero[num] = -1
        distancia[num] = 10000000
        sin_visitar.appendleft(num)
    distancia[origen] = 0
    while True:
        menor = 400000
        num = ''
        for i in range(0, len(sin_visitar)):
            vertice=sin_visitar[i]
            if distancia[vertice] <= menor:
                menor = distancia[vertice]
                num = vertice
        actual=num
        if actual == destino:
            break
        sin_visitar.remove(actual)
        for i in range(0, len(grafo[actual])):
            adyacente=grafo[actual][i]
            alt = distancia[actual] + grafo[actual][adyacente][0]
            if alt < distancia[adyacente]:
                primero[adyacente] = actual
                distancia[adyacente] = alt
        if len(sin_visitar) == 0:
            break
    Camino(primero, destino)
    print()
    print(distancia[destino])


def Acoso(origen, destino, grafo):
    acoso = dict()
    primero = dict()
    sin_visitar = deque()
    for num in grafo:
        primero[num] = -1
        acoso[num] = 10000000
        sin_visitar.appendleft(num)
    acoso[origen] = 0
    while True:
        menor = 400000
        num = ''
        for i in range(0, len(sin_visitar)):
            vertice = sin_visitar[i]
            if acoso[vertice] <= menor:
                menor = acoso[vertice]
                num = vertice
        actual = num
        if actual == destino:
            break
        sin_visitar.remove(actual)
        for i in range(0, len(grafo[actual])):
            adyacencia = grafo[actual][i]
            alt = acoso[actual] + grafo[actual][adyacencia][0]
            if alt < acoso[adyacencia]:
                primero[adyacencia] = actual
                acoso[adyacencia] = alt
        if len(sin_visitar) == 0:
            break
    Camino(primero, destino)
    print()
    print(acoso[destino] / Vertices(primero, destino))


print(grafito)
