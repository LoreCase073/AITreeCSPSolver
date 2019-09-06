import random
import csv
from timeit import default_timer as timer



# ---------------------------------------------------------------------


class Grafo:
    def __init__(self):
        self.graph = {}
        self.vertices = []


    # k è la dimensione del quadrato, n il numero di elementi che definirò
    # al suo interno

    def createMap(self, n, k):
        i = 0
        while i < n:
            xt = random.randrange(0, k - 1)
            yt = random.randrange(0, k - 1)
            if ((xt, yt) not in self.vertices):
                newPoint = (xt, yt)
                self.vertices.append(newPoint)
                i=i+1
        self.graph = self.createGraph()
        print(self.graph)

    # crea un grafo da una serie di punti come descritto nell'esercizio 6.9 del libro
    def createGraph(self):
        checked = {}
        completi = []
        for p in self.vertices:
            self.graph[p] = []
            checked[p] = []
            checked[p].append(p)
        finito = False
        while finito == False:
            if (len(completi) != len(self.vertices)):  # controllo che quelli già completi non siano tutti quelli di listaP
                notCheckedList = list(set(self.vertices) - set(
                    completi))  # crea lista di elementi non completamente controllati per i vari archi
                currentP = random.choice(notCheckedList)  # scelgo elemento a caso della lista dei non completi
                possibiliArc = list(set(self.vertices) - set(checked[
                                                          currentP]))  # creo lista di elementi non ancora archi e non ancora controllati se possibile fare arco
                currentP2 = self.minimumDistance(currentP, possibiliArc)  # prendo elemento da possibili nuovi archi con p2
                checked[currentP].append(currentP2)  # inserisco tra i controllati per currentP
                if (len(checked[currentP]) == len(
                        self.vertices)):  # se questo è l'ultimo elemento da controllare per creare arco con questo nodo lo metto nei completi
                    completi.append(currentP)
                interseca = False
                for nodo in self.graph.keys():
                    if self.graph[nodo] != []:
                        for a in self.graph[nodo]:
                            if (self.segmentIntersect(currentP, currentP2, nodo,
                                                 a)):  # controllo per ogni arco se c'è una intersezione con quello che vorrei creare
                                interseca = True
                                break
                if (
                        interseca == False):  # se non c'è intersezione creo l'arco e lo metto nel dict del grafo, faccio anche il contrario per avere archi bidirezionali
                    self.graph[currentP].append(currentP2)
                    self.graph[currentP2].append(currentP)
            else:
                finito = True  # esco dal ciclo solo se non ci sono altri elementi da controllare
        return self.graph  # restituisco il mio grafo con i punti che avevo inserito in precedenza


        # qui ci sono le funzioni che servono per implementare il segment intersect



    def direction(self, pi, pj, pk):
        return (pk[0] - pi[0]) * (pj[1] - pi[1]) - (pj[0] - pi[0]) * (pk[1] - pi[1])



    def onSegment(self, pi, pj, pk):
        if (min(pi[0], pj[0]) < pk[0] and pk[0] < max(pi[0], pj[0]) and min(pi[1], pj[1]) < pk[1] and pk[1] < max(pi[1],pj[1])):
            return True
        else:
            return False

    def segmentIntersect(self, p1, p2, p3, p4):
        d1 = self.direction(p3, p4, p1)
        d2 = self.direction(p3, p4, p2)
        d3 = self.direction(p1, p2, p3)
        d4 = self.direction(p1, p2, p4)
        if (((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))):
            return True
        elif (d1 == 0 and self.onSegment(p3, p4, p1)):
            return True
        elif (d2 == 0 and self.onSegment(p3, p4, p2)):
            return True
        elif ((d3 == 0) and self.onSegment(p1, p2, p3)):
            return True
        elif (d4 == 0 and self.onSegment(p1, p2, p4)):
            return True
        elif (d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0):
            return True
        elif ((p1 == p3 and p3 == p4) or (p1 == p4 and p2 == p3)): # controllo che non siano lo stesso arco
            return True
        else:
            return False



    # restituisce l'elemento di minima distanza di una lista di punti
    def minimumDistance(self, p1, listaP):
        minimo = (p1[0] - listaP[0][0]) * (p1[0] - listaP[0][0]) + (p1[1] - listaP[0][1]) * (p1[1] - listaP[0][1])
        minP = listaP[0]
        for p in listaP:
            if (minimo > (p1[0] - p[0]) * (p1[0] - p[0]) + (p1[1] - p[1]) * (p1[1] - p[1])):
                minimo = (p1[0] - p[0]) * (p1[0] - p[0]) + (p1[1] - p[1]) * (p1[1] - p[1])
                minP = p
        return minP




# -----------------------------------------



class ConstraintProblemTree:
    vertices = []
    tree = {}
    domains = {}
    parents = {}


    def __init__(self, cpg, domain):
        self.vertices = cpg.vertices
        self.spanningTree(cpg.graph)
        self.setDomains(domain)

    def spanningTree(self, grafo):
        connectedComponent = []
        nodes = list(grafo.keys())  # prendo i nodi del grafo
        for n in nodes:
            self.tree[n] = []
        connectedComponent.append(random.choice(nodes))  # prendo un nodo a caso dalla lista di nodi
        notConnected = set(nodes) - set(connectedComponent)
        while len(notConnected) != 0:
            currentNode = random.choice(connectedComponent)
            nextNode = random.choice(grafo[currentNode])
            if nextNode not in connectedComponent:
                connectedComponent.append(nextNode)
                self.tree[currentNode].append(nextNode)
                self.tree[nextNode].append(currentNode)
                notConnected.remove(nextNode)




    def treeCSPSolver(self):
        n = len(self.vertices)
        assignment = {}

        self.vertices = topologicalSort(self)
        for i in range(0,n):
            assignment[self.vertices[i]] = []
        for i in range(n,2):
            if self.directedAC(self.vertices[i],self.parents[i])==False:
                return False
        for i in range(0,n):
            c=self.assignValue(self.vertices[i],self.parents[self.vertices[i]], assignment)
            if(c==False):
                return False
        return assignment



    def assignValue(self, node, parent, assignment): # controlla i valori da assegnare e ritorna se è stato fatto un assegnamento oppure no
        check=False
        while check==False and len(self.domains[node])!=0:
            dValue=random.choice(self.domains[node])
            self.domains[node].remove(dValue)
            if self.checkValue(dValue, parent, assignment):
                assignment[node]=dValue
                check=True
        return check



    def checkValue(self, value, parent, assignment):  # all'assegnazione controlla se il valore
        if(parent==None):                             # è corretto
            return True
        if (value == assignment[parent]):

            return False
        else:
            return True

    def setDomains(self, n): # aggiunge i domains ai vari nodi
        d=[]
        for i in range(0,n):
            d.append(i)
        for node in self.vertices:
            self.domains[node] = list.copy(d)


    def directedAC(self, parent, node):  # fa arc consistency in un albero
        c=len(self.domains[parent])  # lunghezza dei valori del domain del parent
        for dValue in self.domains[parent]:
            if self.reviseMapColour(dValue, node)==False:   #qui metto i costraint da controllare
                self.domains[parent].remove(dValue)
                c=c-1
        if c==0:
            return False # non ci sono valori giusti
        else:
            return True


    def reviseMapColour(self, colour, node): # controlla se vi è necessità nel caso di map coloring di rimuovere valori durante AC
        domain=list.copy(self.domains[node])
        for nodeColour in domain:
            if(nodeColour==colour):
                domain.remove(colour)
        if len(domain)==0:
            return False
        else:
            return True





def topologicalSortRec(tree,parents, v, visited, stack):

    visited[v] = True
    for i in tree[v]:
        if visited[i] == False:
            parents[i]=v
            tree[i].remove(v)
            topologicalSortRec(tree, parents, i, visited, stack)
    stack.insert(0, v)


def topologicalSort(tree):

    tmpTree=dict.copy(tree.tree)
    visited = {}
    parents = {}
    for v in tree.vertices:
        visited[v] = False
        parents[v]=None
    stack = []
    v=None
    for i in tree.vertices:
        if visited[i] == False:
            parents[i]=v
            topologicalSortRec(tmpTree, parents, i, visited, stack)
    tree.parents=parents
    return stack





# ------------------------------------------------------------




def main():


    for i in range(10,200,5): #modificare per eseguire con grandezze incrementali
        start = timer()
        g_test = Grafo()
        n = i
        k = i
        g_test.createMap(n, k)
        domains = 3 #modificare per scegliere il numero di colori da avere nei domains

        t_test = ConstraintProblemTree(g_test, domains)
        solver_time_start = timer()
        result = t_test.treeCSPSolver()
        if result==False:
            with open('dataTreeCSP.csv', mode='a') as dataFile:
                dataFile = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                dataFile.writerow([n, domains, 'Failed'])

            with open('resultTreeCSP.csv', mode='a') as dataFile:
                dataFile = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                dataFile.writerow([n, 'Failed'])

            with open('treeCSPAdjacencyList.csv', mode='a') as dataFile:
                dataFile = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                dataFile.writerow([n, 'Failed'])
            print('Resolution failed!')
        else:
            solver_time_end = timer()
            solver_time = solver_time_end - solver_time_start
            print("Tempo per eseguire tree-csp-solver=", solver_time)
            end = timer()
            execution_time = end - start
            print("Risultato finale \n", result)
            print("Albero \n", t_test.tree)
            print("N=", n)
            print("Tempo: ", execution_time)

            with open('dataTreeCSP.csv', mode='a') as dataFile:
                dataFile = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                dataFile.writerow([n, domains, solver_time, execution_time])

            with open('resultTreeCSP.csv', mode='a') as dataFile:
                dataFile = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                dataFile.writerow([n, result])

            with open('treeCSPAdjacencyList.csv', mode='a') as dataFile:
                dataFile = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                dataFile.writerow([n, t_test.tree])







if __name__ == '__main__':
    main()





# -----------------------------


