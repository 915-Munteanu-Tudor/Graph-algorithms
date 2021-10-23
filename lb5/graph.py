import copy
from collections import defaultdict
import math

import numpy as np
import random


class DDictGraph:
    def __init__(self, n):
        """Creates a graph with n vertices (numbered from 0 to n-1)
        and no edges"""
        self._dict_undirected = defaultdict(list)
        self.Time = 0
        self.vrtx = 0
        self.edges = 0
        self.count = 0
        self.dictgrf = {}
        self._dictOut = {}
        self._dictIn = {}
        self._dictCost = {}
        self._newdictOut = {}
        self._newdictIn = {}
        self._newdictCost = {}
        self._sol = []
        self._adjMatrix = []
        for i in range(n):
            self._dictOut[i] = []
            self._dictIn[i] = []


    def nrVertixes(self):
        "Returns the nmber of vertixes of the graph"
        return len(self._dictIn.keys())

    def inDegree(self, x):
        "Returns the out degree of the x vertex"
        try:
            if x in self._dictIn.keys():
                return len(self._dictIn[x])
            else:
                return "Does not exist!"
        except KeyError as ke:
            if x not in self._dictIn.keys():
                return "Does not exist!"
            else:
                return 0

    def outDegree(self, x):
        "Returns the in degree of the x vertex"
        try:
            if x in self._dictOut.keys():
                return len(self._dictOut[x])
            else:
                return "Does not exist!"
        except KeyError as ke:
            if x not in self._dictOut.keys():
                return "Does not exist!"
            else:
                return 0

    def parseX(self):
        """Returns an iterable containing all the vertices"""
        return self._dictOut.keys()

    def parseNout(self, x):
        """Returns an iterable containing the outbound neighbours of x"""
        # if x in self._dictOut.keys() and len(self._dictOut[x]) != 0:
        return self._dictOut[x]
        # elif x in self._dictOut.keys() and len(self._dictOut[x]) == 0:
        #     return "No outbound neighbours"
        # else: return "Does not exist!"

    def parseNin(self, x):
        """Returns an iterable containing the inbound neighbours of x"""
        if x in self._dictIn.keys() and len(self._dictOut[x]) != 0:
            return self._dictIn[x]
        elif x in self._dictIn.keys() and len(self._dictOut[x]) == 0:
            return "No inbound neighbours"
        else:
            return "Does not exist!"

    def isEdge(self, x, y):
        """Returns True if there is an edge from x to y, False otherwise"""
        try:
            return y in self._dictOut[x]
        except KeyError:
            return "No edge"

    def addEdge(self, x, y, cost):
        """Adds an edge from x to y.
        Precondition: there is no edge from x to y"""
        if self.isEdge(x, y) != True and (x in self._dictIn.keys() or x in self._dictOut.keys()) and (
                y in self._dictIn.keys() or y in self._dictOut.keys()):
            self._dictOut[x].append(y)
            self._dictIn[y].append(x)
            self._dictCost[(x, y)] = cost
            self._dict_undirected[x].append(y)
            self._dict_undirected[y].append(x)
            return True
        else:
            print("There is an edge between x and y or the vertexes does not exist.\n")

    def removeEdge(self, x, y):
        "Remove the edge between x and y if it exists"
        if self.isEdge(x, y) == True:
            self._dictOut[x].remove(y)
            self._dictIn[y].remove(x)
            del self._dictCost[(x, y)]
            print("The edge from " + str(x) + " to " + str(y) + " was deleted!\n")
            return True
        else:
            print("There is no edge between x and y.\n")

    def modifyEdge(self, x, y, cost):
        "Modifies the cost of an edge if it exists"
        if self.isEdge(x, y):
            self._dictCost[(x, y)] = cost
            return True
        else:
            print("There is no edge from x to y.\n")

    def retriveEdgeCost(self, x, y):
        "Returns the cost of an edge if it exists."
        if self.isEdge(x, y) == True:
            return self._dictCost[(x, y)]
        else:
            return "The edge does not exist"

    def removeVertex(self, x):
        "remove x from every vertex dict in and dict out"
        "Removes an vertex if it exists"
        z = 0
        if x in self._dictIn.keys():
            z = len(self._dictIn[x]) + len(self._dictIn[x])
            del self._dictIn[x]
            del self._dictOut[x]
            for i in self._dictIn.keys():
                if x in self._dictIn[i]:
                    self._dictIn[i].remove(x)
            for j in self._dictOut.keys():
                if x in self._dictOut[j]:
                    self._dictOut[j].remove(x)
            for k in self._dictCost.keys():
                if k.__contains__(x):
                    self._dictCost[k] = -99999
                # del self._dictCost[k]
            print("The vertex was removed.\n")
            return z, True
        else:
            print("This vertex is not in the graph.\n")
            return z, False

    def addVertex(self, x):
        "Adds a vertex if it does not already exist"
        if x in self._dictOut.keys() or x in self._dictIn.keys():
            print("The vertex already exists so it can't be added.\n")
        else:
            self._dictOut[x] = []
            self._dictIn[x] = []
            # print("Vertex " + str(x) + " was added.\n")
            return True

    def copyGraph(self):
        "This function copies all the 3 dictionaries related to the graph, and it can be modified independently"
        self._newdictIn = copy.deepcopy(self._dictIn)
        self._newdictOut = copy.deepcopy(self._dictOut)
        self._newdictCost = copy.deepcopy(self._dictCost)
        print("The graph was coppied.\n")

    # def accessible(self, s):
    #     """Returns the set of vertices of the graph g that are accessible
    #     from the vertex s"""
    #     acc = set()
    #     acc.add(s)
    #     list = [s]
    #     while len(list) > 0:
    #         x = list[0]
    #         list = list[1:]
    #         for y in self.parseNout(x):
    #             if y not in acc:
    #                 acc.add(y)
    #                 list.append(y)
    #     return acc

    def bf(self, s, x):
        """
        The algorith below visits all the vertices that are accessible from the start vertex.
        They are visited in the order of increasing distances from the starting vertex.
        A previous vector or map is computed, allowing us to compute the minimum length path from the starting vertex to any choosen accessible vertex.
        :param x: ending vertex
        :param s: given starting vertex
        """
        q = []
        z = x
        prev = {}
        dist = {}
        visited = set()
        # we put the starting node in the queue and visit it
        q.append(s)
        visited.add(s)
        dist[s] = 0
        while len(q) != 0:
            # we get the first node in the queue and iterate through all outbound nodes
            x = q.pop(0)
            for y in self.parseNout(x):
                # we only process it if it's not visited yet
                if y not in visited:
                    # we put the node in the queue to be processed later and also mark it as visited
                    q.append(y)
                    visited.add(y)
                    # the distance is the distance of its parent + 1
                    dist[y] = dist[x] + 1
                    # we save its parent
                    prev[y] = x

        if z in visited:
            if z in dist:
                # return the distance and the dict of parents so we can compute the path
                return dist[z], prev
            else:
                return "Does not exist."

    def rec(self, vertex, vertex1, depth, children):
        # custom printing :)
        string = "\t" * depth
        string += str(vertex)
        print(string)
        if (vertex == vertex1):
            return
        index = children[vertex]
        self.rec(index, vertex1, depth + 1, children)

    def df(self, x, visited, processed):
        for y in self.parseNout(x):
            if y not in visited:
                visited.append(int(y))
                self.df(y, visited, processed)
        processed.append(x)

    def kosaraju(self):
        processed = []
        visited = []
        for s in self.parseX():
            if s not in visited:
                visited.append(s)
                self.df(s, visited, processed)
        visited.clear()
        c = 0
        comp = {}
        q = []
        while not len(processed) == 0:
            s = processed.pop()
            if s not in visited:
                c += 1
                comp[s] = c
                q.append(s)
                visited.append(s)
                while len(q) != 0:
                    x = q.pop()
                    try:
                        for y in self.parseNin(x):
                            if y not in visited:
                                visited.append(int(y))
                                q.append(int(y))
                                comp[int(y)] = c
                    except Exception:
                        continue
        return comp

    def matrixmultiplication(self, D, W, P):
        for i in range(self.nrVertixes()):
            for j in range(self.nrVertixes()):
                # D[i][j] = math.inf
                for k in range(self.nrVertixes()):
                    if D[i][k] + W[k][j] < D[i][j]:
                        D[i][j] = D[i][k] + W[k][j]
                        P[i][j] = k
                        # parent j cand trece prin i
        return D

    def slow_apsp(self):
        W = [[math.inf for i in range(self.nrVertixes())] for j in range(self.nrVertixes())]
        P = [[-1 for i in range(self.nrVertixes())] for j in range(self.nrVertixes())]
        for i in range(self.nrVertixes()):
            for j in range(self.nrVertixes()):
                if i == j:
                    W[i][j] = 0
                elif self.isEdge(i, j):
                    W[i][j] = self._dictCost[(i, j)]
                    P[i][j] = i
        D = copy.deepcopy(W)
        self.display_matrix(D)

        for m in range(2, self.nrVertixes()):
            D = self.matrixmultiplication(D, W, P)
            self.display_matrix(D)
        return D, P

    def predecessor_counting(self):
        sorted = []
        q = []

        count = {}
        for x in self.parseX():
            count[x] = self.inDegree(x)
            if count[x] == 0:
                q.append(x)
        while not len(q) == 0:
            x = q.pop(0)
            sorted.append(x)
            for y in self.parseNout(x):
                count[y] = count[y] - 1
                if count[y] == 0:
                    q.append(y)
        if len(sorted) < len(self.parseX()):
            sorted = None

        return sorted

    # def times_project(self):
    #     srtd = self.predecessor_counting()

    def display_matrix(self, D):
        print()
        for i in range(0, self.nrVertixes()):
            for j in range(0, self.nrVertixes()):
                print(str(D[i][j]), end=" ")
            print()
        print("\n")

    def write_text_file1(self, file_name, vertexes, edges):
        "Writes the graph and its modifications in the source file."
        open(file_name, "w").close()
        f = open(file_name, "w")
        string = str(vertexes) + " " + str(edges) + "\n"
        f.write(string)
        try:
            for vt in self._dictCost.keys():
                if self._dictCost[vt] != -99999:
                    string1 = str(vt[0]) + " " + str(vt[1]) + " " + str(self._dictCost[vt]) + "\n"
                    f.write(string1)
            for i in self._dictIn.keys():
                if self.inDegree(i) == 0 and self.outDegree(i) == 0:
                    f.write(str(i) + "\n")
            f.close()
        except Exception as e:
            print("An error occurred -" + str(e))

    def write_text_coppiedGrph(self, file_name, vertexes, edges):
        "Writes the copy of the graph in the corresponding file."
        open(file_name, "w").close()
        f = open(file_name, "w")
        string = str(vertexes) + " " + str(edges) + "\n"
        f.write(string)
        try:
            for vt in self._newdictCost.keys():
                if self._newdictCost[vt] != -99999:
                    string1 = str(vt[0]) + " " + str(vt[1]) + " " + str(self._dictCost[vt]) + "\n"
                    f.write(string1)
            for i in self._dictIn.keys():
                if self.inDegree(i) == 0 and self.outDegree(i) == 0:
                    f.write(str(i) + "\n")
            f.close()
        except Exception as e:
            print("An error occurred -" + str(e))

    def random_graph(self, vertexes, edges):
        "Creates a random graph represented by an adjacency matrix."

        nredges = edges
        if (vertexes * vertexes >= edges):
            x = []
            for i in range(vertexes):
                x.append(random.randint(0, 9999))
            for i in x:
                self.dictgrf[i] = []
            while nredges > 0:

                y = random.choice(list(self.dictgrf.keys()))
                z = random.choice(list(self.dictgrf.keys()))
                ok = 1
                for j in range(len(self.dictgrf[y])):
                    if self.dictgrf[y][j] == z:
                        ok = 0
                        break
                if ok == 1:
                    self.dictgrf[y].append(z)
                    nredges -= 1
            return True
        else:
            return False

    def write_textf_rdgrph(self, file_name, vertexes, edges):
        "Writes the random generated graph in the corresponding text file."
        open(file_name, "w").close()
        f = open(file_name, "w")
        if (vertexes is None and edges is None):
            f.write("The graph cannot be made.")
            return
        string = str(vertexes) + " " + str(edges) + "\n"
        f.write(string)
        try:
            for i in self.dictgrf.keys():
                for j in self.dictgrf[i]:
                    string1 = str(i) + " " + str(j) + " " + str(np.random.randint(-999, 999)) + "\n"
                    f.write(string1)
            f.close()
        except Exception as e:
            print("An error occurred -" + str(e))

    def BCCUtil(self, u, parent, low, disc, st):

        # Count of children in current node
        children = 0

        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        if u in self._dict_undirected.keys():
            # Recur for all the vertices adjacent to this vertex
            for v in self._dict_undirected[u]:
                # If v is not visited yet, then make it a child of u
                # in DFS tree and recur for it
                if disc[v] == -1:
                    parent[v] = u
                    children += 1
                    st.append((u, v))  # store the edge in stack
                    self.BCCUtil(v, parent, low, disc, st)

                    # Check if the subtree rooted with v has a connection to
                    # one of the ancestors of u
                    # Case 1 -- per Strongly Connected Components Article
                    low[u] = min(low[u], low[v])

                    # If u is an articulation point, pop
                    # all edges from stack till (u, v)
                    if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                        self.count += 1  # increment count
                        w = -1
                        while w != (u, v):
                            w = st.pop()

                elif v != parent[u] and low[u] > disc[v]:
                    '''Update low value of 'u' only of 'v' is still in stack
                    (i.e. it's a back edge, not cross edge).
                    Case 2 
                    -- per Strongly Connected Components Article'''

                    low[u] = min(low[u], disc[v])

                    st.append((u, v))

    # The function to do DFS traversal.
    # It uses recursive BCCUtil()
    def BCC(self):

        # Initialize disc and low, and parent arrays
        disc = [-1] * (len(self.parseX()))
        low = [-1] * (len(self.parseX()))
        parent = [-1] * (len(self.parseX()))
        st = []

        # Call the recursive helper function to
        # find articulation points
        # in DFS tree rooted with vertex 'i'
        for i in range(len(self.parseX())):
            if disc[i] == -1:
                self.BCCUtil(i, parent, low, disc, st)

            # If stack is not empty, pop all edges from stack
            if st:
                self.count = self.count + 1

                while st:
                    w = st.pop()
                    # print(w)
        return self.count

    def wcg(self):
        ans = self.bf(1, 2)
        print("F -> Farmer")
        print("W -> Wolf")
        print("G -> Goat")
        print("C -> Cabbage")
        print("The shortest path is " + str(ans[0]))
        for state in ans[1]:
            if state == 1:
                print("WGCF |")
            elif state == 2:
                print("     | WGCF")
            elif state == 3:
                print("WCF  | G")
            elif state == 4:
                print("   G | WCF")
            elif state == 5:
                print("WGF  | C")
            elif state == 6:
                print("    C | WGF")
            elif state == 7:
                print(" GCF | W")
            elif state == 8:
                print("   W | GCF")
            elif state == 9:
                print("  GF | WC")
            elif state == 10:
                print("  WC | GF")

    @property
    def dictOut(self):
        return self._dictOut

    @property
    def sol(self):
        return self._sol

    @sol.setter
    def sol(self, value):
        self._sol = value
    @property
    def adjMatrix(self):
        return self._adjMatrix

    @property
    def dictCost(self):
        return self._dictCost
