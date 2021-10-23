def display_commands():
    """
    "Prints all the possible commands as a menu"
    """

    print("1 Get the numbers of vertices.")
    print("2 Parse the set vertices.")
    print("3 Find out if there is an edge from a vertex to another.")
    print("4 Get the in degree and the out degree of a vertex.")
    print("5 Parse the outbound edges of a vertex.")
    print("6 Parse the inbound edges of a vertex.")
    print("7 Modify the cost of an edge.")
    print("8 Retrive the cost of an edge.")
    print("9 Add a vertex.")
    print("a Remove a vertex.")
    print("b Add an edge.")
    print("c Remove an edge.")
    print("d Make a copy of the graph.")
    print("e Create a random graph with a specified number of vertexes and edges.")
    print("f Find the lowest length path between 2 given vertexes.")
    print("g Find the strongly connected components in the graph.")
    print("h BCC.")
    print("i WCG.")
    print("j Lowest cost path between 2 vertexes.")
    print("k DAG")
    print("l Number of distinct paths")
    print("m TSP")
    print("x Exit.")


class UserInterface:

    def commands(self):
        "Splits all the commands in arguments for the functions which will be called."
        self.command = input("Give an instruction: ")

        if self.command.startswith('1') or self.command.startswith('d') or self.command.startswith('2')\
                or self.command.startswith('g') or self.command.startswith('h') or self.command.startswith('i') or self.command.startswith('x') or self.command.startswith('k') or self.command.startswith('m'):
            return self.command, []
        elif self.command.startswith('4') or self.command.startswith('5') or self.command.startswith('6'):
            com = self.command.split(' ')
            return com[0], com[1]
        elif self.command.startswith('a') or self.command.startswith('9'):
            com = self.command.split(' ')
            return com[0], com[1]
        elif self.command.startswith('3') or self.command.startswith('c') or self.command.startswith('8') or self.command.startswith('e') or self.command.startswith('f') or self.command.startswith('j') or self.command.startswith('l'):
            com1 = self.command.split(' ')
            args = [com1[1], com1[2]]
            return com1[0], args
        elif self.command.startswith('b') or self.command.startswith('7'):
            com2 = self.command.split(' ')
            args = [com2[1], com2[2], com2[3]]
            return com2[0], args


