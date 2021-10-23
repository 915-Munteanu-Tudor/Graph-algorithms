def read_textfile(filename):
    "function used to read only the initial input from the source file."
    contor = 0
    list1 = []
    with open(filename, 'rt') as f:
        for line in f:
            line = line.strip()
            arguments = line.split(" ")
            if contor == 0:
                vertexes = arguments[0]
                edges = arguments[1]
            else:
                list = [arguments[0], arguments[1], arguments[2]]
                list1.append(list)
            contor += 1
    f.close()
    return vertexes, edges, list1


def read_dag(filename):
    "function used to read only the initial input from the source file."
    contor = 0
    list1 = []
    with open(filename, 'rt') as f:
        for line in f:
            line = line.strip()
            arguments = line.split(" ")
            if contor == 0:
                vertexes = arguments[0]
                edges = arguments[1]
            else:
                if len(arguments) == 3:
                    arg = arguments[2].split(",")
                    lst = [arguments[0], arguments[1], arg]
                    list1.append(lst)
                elif len(arguments) == 2:
                    lst = [arguments[0], arguments[1]]
                    list1.append(lst)

            contor += 1
    f.close()
    return vertexes, edges, list1
