# import progressbar
# from time import sleep
import sys
import time
import numpy as np
import math
import progressbar
import beam

class Lattice(object):
    def __init__(self, elements, nodes):
        self.elements, self.nodes = elements, nodes

class Line(object):
    def __init__(self, dv, nodes):
        self.dv, self.nodes = dv, nodes
        self.idx = -1
    def toString(self):
        return "vector: [" + str(self.dv[0]) + " " + str(self.dv[1]) + " " + str(self.dv[2]) + "]\tnodes " + str(self.nodes) 
    def __hash__(self):
        return hash(self.dv[0], self.dv[1], self.dv[2])
    def __eq__(self, other):
        return self.dv[0] / other.dv[0] == self.dv[1] / other.dv[1] and self.dv[1] / other.dv[1] == self.dv[2] / other.dv[2] 
    def append(self, node):
        self.nodes = np.append(self.nodes, node)

class Node(object):
    def __init__(self, x, y, z):
        self.xyz = np.array([x,y,z])
    def __hash__(self):
        return hash(self.xyz[0], self.xyz[1], self.xyz[2])
    def __eq__(self, other):
        return self.xyz[0] == other.xyz[0] and self.xyz[1] == other.xyz[1] and self.xyz[2] == other.xyz[2]

def node_to_string(node):
    return str(node[0]) + "," + str(node[1]) + "," + str(node[2])

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_nodes():
    nodes = []
    with open('nodes.txt') as node_file:
        for line in node_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
                    nodes.append(Node(float(words[1]), float(words[2]), float(words[3])))
    node_file.close()
    return nodes

def read_elements(nodes):
    elements = []
    global ELEMENT_ATTRIBUTES
    flag = False
    with open('elements.txt') as element_file:
        for line in element_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
                    if not flag:
                        #ELEMENT_ATTRIBUTES = words[1] + " " + words[2] + " " + words[3] + " " + words[4]
                        ELEMENT_ATTRIBUTES = "2 2 3 4"
                        flag = True
                    elements.append(np.array([nodes[int(words[6]) - 1], nodes[int(words[7]) - 1], nodes[int(words[8]) - 1]]))
    element_file.close()
    return elements

# reads a mesh file with name "file" (excluding extension) and returns two lists
# The first list is a list of nodes from the .msh file
# The second is a lsit of elements from the .msh file
def read_msh(file):
    reading_nodes = False
    reading_elements = False
    nodes = []
    elements = []

    with open(file + ".msh") as mesh:
        for line in mesh:
            if not line.strip():
                continue
            else:
                words = line.split()
                count = 0
                if reading_nodes:
                    if words[0] == "$EndNodes":
                        reading_nodes = False
                    else:
                        if is_number(words[0]) and len(words) > 1:
                            nodes.append(Node(float(words[1]), float(words[2]), float(words[3])))
                else:
                    if reading_elements == False and reading_nodes == False:
                        if words[0] == "$Elements":
                            reading_elements = True
                        elif words[0] == "$Nodes":
                            reading_nodes = True
                    else:
                        if is_number(words[0]) and len(words) > 1:
                            elements.append(np.array([nodes[int(words[len(words) - 3]) - 1],
                                                    nodes[int(words[len(words) - 2]) - 1],
                                                    nodes[int(words[len(words) - 1]) - 1]]))
                        elif words[0] == "$EndElements":
                            read_elements = False
    mesh.close()
    return nodes, elements

def normal(element):
    p1 = np.array([element[0].xyz[0], element[0].xyz[1], element[0].xyz[2]]) / math.sqrt((element[0].xyz[0] * element[0].xyz[0]) + (element[0].xyz[1] * element[0].xyz[1]) + (element[0].xyz[2] * element[0].xyz[2])) 
    p2 = np.array([element[1].xyz[0], element[1].xyz[1], element[1].xyz[2]]) / math.sqrt((element[1].xyz[0] * element[1].xyz[0]) + (element[1].xyz[1] * element[1].xyz[1]) + (element[1].xyz[2] * element[1].xyz[2]))
    p3 = np.array([element[2].xyz[0], element[2].xyz[1], element[2].xyz[2]]) / math.sqrt((element[2].xyz[0] * element[2].xyz[0]) + (element[2].xyz[1] * element[2].xyz[1]) + (element[2].xyz[2] * element[2].xyz[2]))

    u = p2 - p1
    v = p3 - p1

    return np.cross(u, v)

def direction_delta(nodes):
    maxX = max(node.xyz[0] for node in nodes)
    minX = min(node.xyz[0] for node in nodes)
    maxY = max(node.xyz[1] for node in nodes)
    minY = min(node.xyz[1] for node in nodes)
    maxZ = max(node.xyz[2] for node in nodes)
    minZ = min(node.xyz[2] for node in nodes)
    return Node(maxX - minX, maxY - minY, maxZ - minZ)

def max_xyz(nodes):
    max_x = nodes[0].xyz[0]
    max_y = nodes[0].xyz[1]
    max_z = nodes[0].xyz[2]

    for node in nodes:
        if node.xyz[0] > max_x:
            max_x = node.xyz[0]
        if node.xyz[1] > max_y:
            max_y = node.xyz[1]
        if node.xyz[2] > max_z:
            max_z = node.xyz[2]
    return [max_x,max_y,max_z]

# generate a .msh version of a lattice volume with the given unit value and x, y, and z dimensions
def generate_msh(nodes, elements, x, y, z):
    displacement_factor = direction_delta(nodes)
    total_nodes = len(nodes)

    output = open("output/lattice.msh", 'w')

    output.write("$MeshFormat\n")
    # MESH FORMAT
    output.write("2.2 0 8\n")
    output.write("$EndMeshFormat\n$Nodes\n")
    # WRITE NODES HERE
    # NUM OF NODES
    output.write(str(((x) * (y) * (z)) * total_nodes) + "\n")

    x_delta = 0
    y_delta = 0
    z_delta = 0    
    nodes_count = 0

    for num1 in range(0,x):
        x_delta += displacement_factor.xyz[0]
        y_delta = 0
        for num2 in range (0,y):
            y_delta += displacement_factor.xyz[1]
            z_delta = 0
            for num3 in range(0,z):
                z_delta += displacement_factor.xyz[2]
                for n in model.nodes:
                    output.write(str(n.idx + nodes_count) +
                                 " " + str(n.xyz[0] + x_delta) +
                                 " " + str(n.xyz[1] + y_delta) +
                                 " " + str(n.xyz[2] + z_delta) + ' ')
                nodes_count += total_nodes


# generate a .stl version of a lattice volume with the given unit value and x, y, and z dimensions
def generate_stl(nodes, elements, x, y, z):
    displacement_factor = direction_delta(nodes)
    total_nodes = len(nodes)

    output = open("output/lattice.stl", 'w')
    output.write("solid Created by LatticeGenerator\n")
    
    bar = progressbar.ProgressBar(max_value=(x*y*z))

    x_delta = 0 
    y_delta = 0 
    z_delta = 0
    count = 0

    for curr_x in range(0,x):
        y_delta = 0
        x_delta += displacement_factor.xyz[0]
        for curr_y in range(0,y):
            z_delta = 0
            y_delta += displacement_factor.xyz[1]
            for curr_z in range(0,z):
                count += 1
                z_delta += displacement_factor.xyz[2]
                bar.update(count)

                for e in elements:
                    norm = normal(e)
                    output.write("facet normal " + str(norm[0]) 
                            + ' ' + str(norm[1])
                            + ' ' + str(norm[2]) + ' ' + '\n')
                    #Sprint(normal)
                    output.write("\touter loop" + '\n')
                    output.write("\t\tvertex " + str(e[0].xyz[0] + x_delta) +
                                 ' ' + str(e[0].xyz[1] + y_delta) +
                                 ' ' + str(e[0].xyz[2] + z_delta) + '\n')
                    output.write("\t\tvertex " + str(e[1].xyz[0] + x_delta) +
                                 ' ' + str(e[1].xyz[1] + y_delta) +
                                 ' ' + str(e[1].xyz[2] + z_delta) + '\n')
                    output.write("\t\tvertex " + str(e[2].xyz[0] + x_delta) +
                                 ' ' + str(e[2].xyz[1] + y_delta) +
                                 ' ' + str(e[2].xyz[2] + z_delta) + '\n')
                    output.write("\tendloop" + '\n')
                    output.write("endfacet" + '\n')
    output.write("endsolid Created by LatticeGenerator")


def main():
    nodes = []
    elements = []
    nodes, elements = read_msh("lattice")
    max_values = max_xyz(nodes)
    boundry_nodes = []
    displacement_factor = direction_delta(nodes)
    count = 0
    non_boundry = []

    # FIND BOUNDRY NODES
    nodes.sort(key=lambda n:n.xyz[0])
    for n in nodes:
        if n.xyz[0] == (max_values[0] - displacement_factor.xyz[0]) or n.xyz[0] == max_values[0]:
            boundry_nodes.append(n)
    nodes.sort(key=lambda n:n.xyz[1])
    for n in nodes:
        if n.xyz[1] == (max_values[1] - displacement_factor.xyz[1]) or n.xyz[1] == max_values[1]:
            boundry_nodes.append(n)
    nodes.sort(key=lambda n:n.xyz[2])
    for n in nodes:
        if n.xyz[2] == (max_values[2] - displacement_factor.xyz[2]) or n.xyz[2] == max_values[2]:
            boundry_nodes.append(n)


    lines = beam.lines([n for n in nodes if n not in boundry_nodes], boundry_nodes)
    for line in lines:
        print(line.toString())
    print("there are " + str(len(boundry_nodes)) + " out of " + str(len(nodes)) + " boundry nodes")

    #nodes = read_nodes()
    print("nodes per unit: {}".format(len(nodes)))
    #elements = read_elements(nodes)
    
    print("\ninput values for lattice structure")
    x = int(input("x: "))
    y = int(input("y: "))
    z = int(input("z: "))
    start_time = time.time()
    generate_stl(nodes, elements, x, y, z)
    print("\nruntime: " + str(time.time() - start_time))

if __name__ == "__main__":
    main()
