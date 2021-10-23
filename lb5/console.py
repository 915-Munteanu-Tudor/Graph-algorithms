import copy
import math
from itertools import permutations
from sys import maxsize

from numpy.random import permutation

from ui import UserInterface, display_commands
from graph import DDictGraph
from read import read


# import random


class RunApp:

    def print_path(self, P, d):
        if P[d] != -1:
            self.print_path(P, P[d])
        print(d, end=" ")

    def ui_run(self):
        "here the app is run "
        global c, vertexes, edges
        option = str
        run = 1
        self.ui = UserInterface()
        while option != "input.txt" and option != "input_dag.txt":
            option = input("The file to read from is:")
            if option != "input.txt" and option != "input_dag.txt":
                print("This file does not exist")
        print()
        if option == "input.txt":
            vertexes, edges, list1 = read.read_textfile('input.txt')
            vertexes = int(vertexes)
            edges = int(edges)
            self.gr = DDictGraph(int(vertexes))
            self.gr.vrtx = int(vertexes)
            self.gr.edges = int(edges)
            for i in list1:
                self.gr.addEdge(int(i[0]), int(i[1]), int(i[2]))
        elif option == "input_dag.txt":
            vertexes, edges, list1 = read.read_dag("input_dag.txt")
            vertexes = int(vertexes)
            edges = int(edges)
            self.gr.vrtx = int(vertexes)
            self.gr.edges = int(edges)
            self.gr = DDictGraph(int(vertexes))
            for i in list1:
                if len(i) == 3:
                    for j in i[2]:
                        self.gr.addEdge(int(j), list1.index(i), 0)
        else:
            print("This file does not exist!")

        while run == 1:

            ok = 0
            display_commands()
            while ok == 0:
                try:
                    c, a = self.ui.commands()
                    ok = 1
                except (IndexError, TypeError):
                    print("\nThe inputted arguments are wrong.\n")
                    display_commands()
                    ok = 0

            try:
                if c == "1":
                    print(self.gr.nrVertixes(), "\n")
                elif c == "2":
                    if len(self.gr.parseX()) != 0:
                        for i in self.gr.parseX():
                            print(i)
                        print("\n")
                    else:
                        print("The graph has no vertex\n")
                elif c == "3":
                    try:
                        print(self.gr.isEdge(int(a[0]), int(a[1])), "\n")
                    except ValueError:
                        print("\n The arguments are not good\n")
                elif c == "4":
                    try:
                        print(self.gr.inDegree(int(a)))
                        print(self.gr.outDegree(int(a)), "\n")
                    except ValueError:
                        print("\n The arguments are not good\n")
                elif c == "5":
                    try:
                        print(self.gr.parseNout(int(a)))
                    except Exception:
                        print("\nDoes not exist!")
                    # for i in self.gr.parseNout(int(a)):
                    #     print(i)
                    print("")
                elif c == "6":
                    print(self.gr.parseNin(int(a)))
                    # for i in self.gr.parseNin(int(a)):
                    #     print(i)
                    print("")
                elif c == "7":
                    if self.gr.modifyEdge(int(a[0]), int(a[1]), int(a[2])) is True:
                        self.gr.write_text_file1('input_modify.txt', str(vertexes), str(edges))
                        print("The updated edge is " + a[0] + "," + a[1] + " and it's cost now is " + a[2], "\n")
                elif c == "8":
                    print(str(self.gr.retriveEdgeCost(int(a[0]), int(a[1]))) + "\n")
                elif c == "9":
                    try:
                        if self.gr.addVertex(int(a)) is True:
                            vertexes += 1
                            print("Vertex " + str(a) + " was added.\n")
                            self.gr.write_text_file1('input_modify.txt', str(vertexes), str(edges))
                    except ValueError:
                        print("\n The arguments are not good\n")

                elif c == "a":
                    z, val = self.gr.removeVertex(int(a))
                    if val is True:
                        vertexes -= 1
                        edges -= z
                        self.gr.write_text_file1('input_modify.txt', str(vertexes), str(edges))
                elif c == 'b':
                    if self.gr.addEdge(int(a[0]), int(a[1]), int(a[2])) is True:
                        print("\n")
                        # print("The edge from " + a[0] + " to " + a[1] + " with the value of " + a[2] + " was added!\n")
                        edges += 1
                        self.gr.write_text_file1('input_modify.txt', str(vertexes), str(edges))
                elif c == "c":
                    if self.gr.removeEdge(int(a[0]), int(a[1])) is True:
                        edges -= 1
                        self.gr.write_text_file1('input_modify.txt', str(vertexes), str(edges))
                elif c == "d":
                    self.gr.copyGraph()
                    self.gr.write_text_coppiedGrph('coppiedGrph.txt', str(vertexes), str(edges))
                elif c == "e":
                    x = self.gr.random_graph(int(a[0]), int(a[1]))
                    if x is True:
                        vertexes1 = int(a[0])
                        edges1 = int(a[1])
                        self.gr.write_textf_rdgrph('random_graph1.txt', str(vertexes1), str(edges1))
                        print("The random graph was added in the file!\n")
                        self.gr.dictgrf.clear()
                    else:
                        self.gr.write_textf_rdgrph('random_graph2.txt', None, None)
                        print("\nThe graph cannot be made.\n")
                elif c == "f":
                    try:
                        x, y = self.gr.bf(int(a[0]), int(a[1]))
                        print("The lowest distance between the two nodes is: ", x, "\n")
                        self.gr.rec(int(a[1]), int(a[0]), 0, y)
                        print("\n")
                    except Exception:
                        print("\nDoes not exist!\n")
                elif c == "g":
                    try:
                        print(self.gr.kosaraju())
                    except Exception:
                        print("\nDoes not exist!\n")
                elif c == "h":
                    print("The nr f biconected components is:", self.gr.BCC(), "\n")
                elif c == "i":
                    ans = self.gr.wcg()
                    print(ans)
                elif c == "j":
                    D, P = self.gr.slow_apsp()
                    print()
                    print(P)
                    print()
                    ok = True
                    for i in range(self.gr.nrVertixes()):
                        if D[i][i] < 0:
                            print("\nThere is a negative cost cycle in the graph!\n")
                            ok = False
                            break
                    if ok == True:
                        if D[int(a[0])][int(a[1])] == math.inf:
                            print("There is no path between the 2 vertexes")
                        else:
                            print("The lowest cost path has the cost: " + str(D[int(a[0])][int(a[1])]) + "\n")
                            print("The path is: ", end="")
                            self.print_path(P[int(a[0])], int(a[1]))
                            print("\n")
                elif c == "k":
                    if self.gr.predecessor_counting() is None:
                        print("\nThe graph is not DAG\n")

                    else:
                        # print()
                        srt = self.gr.predecessor_counting()
                        # print(srt)
                        print()

                        self.gr.addVertex(-1)
                        self.gr.addVertex(vertexes)
                        vertexes += 2
                        dct = {}

                        for i in self.gr.parseX():
                            if len(self.gr.parseNin(i)) == 0:
                                self.gr.addEdge(-1, i, 99)
                                edges += 1
                                # print("a")

                        for i in self.gr.parseX():
                            if len(self.gr.parseNout(i)) == 0:
                                self.gr.addEdge(i, vertexes - 2, 99)
                                edges += 1

                        self.gr.write_text_file1('input_modify.txt', str(vertexes), str(edges))

                        dct[-1] = []
                        dct[-1].extend([0, -1, 0, 0, 0, 0])
                        for i in range(0, vertexes - 2):
                            dct[i] = []
                            dct[i].extend([0, i, 0, 0, int(list1[i][1]), 0])
                        dct[vertexes - 2] = []
                        dct[vertexes - 2].extend([0, vertexes - 1, 0, 0, 0, 0])

                        srt.insert(0, -1)
                        srt.insert(vertexes - 1, vertexes - 2)

                        print("Topological sort: ", end="")
                        print(srt)
                        print()
                        dct[-1][0] = dct[-1][2]
                        for i in range(1, len(srt)):
                            maxv = -1
                            # print(self.gr.parseNin(srt[8]))
                            if self.gr.parseNin(srt[i]) != "No inbound neighbours":
                                for j in self.gr.parseNin(srt[i]):
                                    if maxv < dct[j][2]:
                                        maxv = dct[j][2]
                            dct[srt[i]][0] = maxv
                            dct[srt[i]][2] = dct[srt[i]][0] + dct[srt[i]][4]

                        dct[vertexes - 2][5] = dct[vertexes - 2][2]
                        dct[vertexes - 2][3] = dct[vertexes - 2][2]

                        # for i in range(0, vertexes-2):
                        #     dct[i][3] = dct[i][5] - dct[i][4]
                        # dct[vertexes - 2][3] = dct[vertexes - 2][5] - dct[vertexes - 2][1]

                        dct[-1][3] = dct[-1][5] = 0

                        for i in range(len(srt) - 2, -1, -1):
                            minv = 99999
                            if len(self.gr.parseNout(srt[i])) != 0:
                                for j in self.gr.parseNout(srt[i]):
                                    if minv > dct[j][3]:
                                        minv = dct[j][3]
                            dct[srt[i]][5] = minv
                            dct[srt[i]][3] = dct[srt[i]][5] - dct[srt[i]][4]

                        dct[vertexes - 2][5] = dct[vertexes - 2][3] = dct[vertexes - 2][2] = dct[vertexes - 2][0]
                        dct[-1][3] = dct[-1][5] = 0

                        for i in range(-1, vertexes - 1):
                            print(str(dct[i][0]) + " " + str(dct[i][2]) + " " + str(dct[i][3]) + " " + str(
                                dct[i][5]) + "\n")
                            if dct[i][5] - dct[i][2] == 0:
                                print("Critical activity: " + str(i) + "\n")

                        print("The total time of the project is: " + str(dct[vertexes - 2][0]) + "\n")


                elif c == "l":
                    dp = [0 for i in range(self.gr.nrVertixes())]
                    src = int(a[0])
                    dest = int(a[1])
                    dp[dest] = 1
                    arr = self.gr.predecessor_counting()
                    if arr is None:
                        print("Not a DAG")
                        return
                    for i in reversed(arr):
                        if i in self.gr.parseX():
                            for j in self.gr.parseNout(i):
                                dp[i] = dp[i] + dp[int(j)]
                    print("\nNumber of distinct paths: ", dp[src])
                    print()

                elif c == "m":

                    # grapf = [[0, 3, 0, 0, 0, 0], [0, 0, 2, 0, 0, 1], [2, 0, 0, 0, 8, 0], [5, 0, 4, 0, 0, 0],
                    #          [0, 0, 0, 5, 0, 0], [0, 0, 2, 0, 5, 0]]

                    # grapf = [[0, 0, 4, 0, 0], [2, 0, 0, 0, 0], [0, 0, 0, 3, 5], [6, 10, 0, 0, 7],
                    #          [0, 5, 0, 2, 0]]

                    # make the adjancy matrix out of the dict representation
                    self.gr._adjMatrix = [[0 for i in range(vertexes)] for j in range(vertexes)]
                    for i in self.gr.dictOut:
                        for j in self.gr.dictOut[i]:
                            if (i, j) in self.gr.dictCost.keys():
                                self.gr.adjMatrix[i][j] = self.gr.dictCost[(i, j)]

                    vrt = []
                    drum = []
                    drum.append(0)

                    # store all the vertexes apart from the source one
                    for i in range(self.gr.vrtx):
                        if i != 0:
                            vrt.append(i)

                    min_path = maxsize
                    # generates all the permutations of the list of vertexes
                    next_permutation = permutations(vrt)

                    for i in next_permutation:
                        #print(i)
                        # set initial values for each permutation
                        valid = 1
                        current_pathweight = 0
                        k = 0

                        # look for valid vertexes to form the path by checking the existence of the edges in
                        # permutation the vertex is added in the path if the edge exists, compute the min cost and
                        # continue the serch
                        for j in i:
                            if self.gr.adjMatrix[k][j] != 0:
                                current_pathweight += self.gr.adjMatrix[k][j]
                                drum.append(j)
                            else:
                                valid = 0
                                break
                            k = j

                        # adds the beginning node to complete the cycle and checks the edge
                        if self.gr.adjMatrix[k][0] != 0 and valid != 0:
                            current_pathweight += self.gr.adjMatrix[k][0]
                            drum.append(0)
                        else:
                            valid = 0

                        # if everything is valid, the min path cost and the path itself are updated and "drum" is reset
                        if valid == 1:
                            min_path = min(min_path, current_pathweight)

                            if current_pathweight == min_path:
                                # drum_final.clear()
                                self.gr._sol = copy.deepcopy(drum)

                        drum.clear()
                        drum.append(0)

                    # prints the path if it exists
                    if min_path != maxsize:
                        print("\nPath:", end='')
                        for i in self.gr.sol:
                            print(i, end='')

                        print()
                        print("Cost: " + str(min_path))
                        print()
                    else:
                        print("\nThe tsp problem has no solution")

                elif c == "x":
                    print("\nBye!")
                    break
                else:
                    print("\nBad command!\n")
            except (IndexError, ValueError):
                print("\nThe arguments are not good\n")
