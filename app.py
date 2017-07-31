# import progressbar
# from time import sleep
import sys
import time
import numpy as np
import math
import progressbar

class Lattice(object):
    def __init__(self, elements, nodes):
        self.elements, self.nodes = elements, nodes
    

class Element(object):
    def __init__(self, n1, n2, n3):
        self.n1, self.n2, self.n3 =  n1, n2, n3
        p1 = np.array([self.n1.x, self.n1.y, self.n1.z]) / math.sqrt(n1.x * n1.x + n1.y * n1.y + n1.z * n1.z) 
        p2 = np.array([self.n2.x, self.n2.y, self.n2.z]) / math.sqrt(n2.x * n2.x + n2.y * n2.y + n2.z * n2.z)
        p3 = np.array([self.n3.x, self.n3.y, self.n3.z]) / math.sqrt(n3.x * n3.x + n3.y * n3.y + n3.z * n3.z)

        u = p2 - p1
        v = p3 - p1

        self.normal = np.cross(u, v)

    def toString(self):
        return "("+ str(self.n1) + "," + str(self.n2) + "," + str(self.n3) + ")"

class Node(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def toString(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_nodes(nodes):
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

def read_elements(nodes, elements):
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
                    elements.append(Element(nodes[int(words[6]) - 1], nodes[int(words[7]) - 1], nodes[int(words[8]) - 1]))
    element_file.close()
    return elements

def direction_delta(nodes):
    maxX = max(node.x for node in nodes)
    minX = min(node.x for node in nodes)
    maxY = max(node.y for node in nodes)
    minY = min(node.y for node in nodes)
    maxZ = max(node.z for node in nodes)
    minZ = min(node.z for node in nodes)
    return Node(maxX - minX, maxY - minY, maxZ - minZ)

# construct a lattice from an already existing unit structure
# could be purposed into multiplying larger lattices as well
# INTUITION: attempt to construct lattice by actively writing as oppsed to storing
#            data to write in a seperate function. This should make program functional 
#            for large values but will make runtime slower and result in a less modular
#            program overall
def generate_lattice(nodes, elements, total_nodes, displacement_factor, x, y, z):
    output = open("output/lattice.stl", 'w')
    output.write("solid Created by LatticeGenerator\n")
    
    bar = progressbar.ProgressBar(max_value=(x*y*z))

    x_delta = 0 
    y_delta = 0 
    z_delta = 0
    count = 0

    for curr_x in range(0,x):
        y_delta = 0
        x_delta += displacement_factor.x
        for curr_y in range(0,y):
            z_delta = 0
            y_delta += displacement_factor.y
            for curr_z in range(0,z):
                count += 1
                z_delta += displacement_factor.z
                bar.update(count)

                for e in elements:
                    output.write("facet normal " + str(e.normal[0]) 
                            + ' ' + str(e.normal[1])
                            + ' ' + str(e.normal[2]) + ' ' + '\n')
                    #Sprint(normal)
                    output.write("\touter loop" + '\n')
                    output.write("\t\tvertex " + str(e.n1.x + x_delta) + ' ' + str(e.n1.y + y_delta) + ' ' + str(e.n1.z + z_delta) + '\n')
                    output.write("\t\tvertex " + str(e.n2.x + x_delta) + ' ' + str(e.n2.y + y_delta) + ' ' + str(e.n2.z + z_delta) + '\n')
                    output.write("\t\tvertex " + str(e.n3.x + x_delta) + ' ' + str(e.n3.y + y_delta) + ' ' + str(e.n3.z + z_delta) + '\n')
                    output.write("\tendloop" + '\n')
                    output.write("endfacet" + '\n')
    output.write("endsolid Created by LatticeGenerator")


def main():
    nodes = []
    elements = []
    nodes = read_nodes([])
    total_nodes = len(nodes)
    print("nodes per unit: {}".format(total_nodes))
    elements = read_elements(nodes, [])
    displacement_factor = direction_delta(nodes)
    print(str(displacement_factor.x) + " " + str(displacement_factor.y) + " " + str(displacement_factor.z))
    print("\ninput values for lattice structure")
    x = int(input("x: "))
    y = int(input("y: "))
    z = int(input("z: "))
    start_time = time.time()
    generate_lattice(nodes, elements, total_nodes, displacement_factor, x, y, z)
    print("\nruntime: " + str(time.time() - start_time))

if __name__ == "__main__":
    main()
