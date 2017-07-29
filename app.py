# import progressbar
# from time import sleep
import sys
import time
import os
from os.path import dirname, abspath
from pymesh import stl  # Import module
from pymesh import obj  # Import module

# job_id = sys.argv[1]
# maxFaces = file_conversion.stpTox3d(job_id)
# print(maxFaces)
# # os.system('C:\\Users\\MD580\\Desktop\\Web-based-CAE-Cloud-Platform\\app\\scripts\\to_gmsh.bat stp_uploads\\{} gmsh_output\\{}'.format(job_id, job_id))
# val = dirname(dirname(abspath(__file__))) + "\\scripts"
# os.system(val + '\\to_gmsh.bat stp_uploads\\{} gmsh_output\\{}'.format(job_id, job_id))

class Dimension(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

class Mesh(object):
    def __init__(self, elements, nodes):
        self.elements, self.nodes = elements, nodes


class Element(object):
    def __init__(self, n1, n2, n3):
        self.n1, self.n2, self.n3 =  n1, n2, n3
    def toString(self):
        return "("+ str(self.n1) + "," + str(self.n2) + "," + str(self.n3) + ")"

class Node(object):
    def __init__(self, idx, x, y, z):
        self.idx, self.x, self.y, self.z = idx, x, y, z
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_nodes():
    nodes = []
    with open('input/nodes.txt') as node_file:
        for line in node_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
                    nodes.append(Node(int(words[0]),float(words[1]), float(words[2]), float(words[3])))
    node_file.close()
    return nodes

def read_elements():
    elements = []
    global ELEMENT_ATTRIBUTES
    flag = False
    with open('input/elements.txt') as element_file:
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
                    elements.append(Element(int(words[6]), int(words[7]), int(words[8])))
    element_file.close()
    return elements

def direction_delta(nodes):
    maxX = max(node.x for node in nodes)
    minX = min(node.x for node in nodes)
    maxY = max(node.y for node in nodes)
    minY = min(node.y for node in nodes)
    maxZ = max(node.z for node in nodes)
    minZ = min(node.z for node in nodes)
    return Node(0, maxX - minX, maxY - minY, maxZ - minZ)

def construct_lattice(displacement_factor, dimension):
    total_num = dimension.x * dimension.y * dimension.z
    count = 0
    unit_m = stl.Stl('output/stl/unit.stl')  # Load stl
    x_m = stl.Stl()  # Load stl
    y_m = stl.Stl()  # Load stl
    lattice = stl.Stl()  # Load stl
    
    for num1 in range (0, dimension.x):
        x_m.join(unit_m.translate_x(displacement_factor.x))
    
    unit_m = x_m
    for num2 in range (0, dimension.y):
        y_m.join(unit_m.translate_y(displacement_factor.y))

    unit_m = y_m
    for num3 in range (0, dimension.z):
        lattice.join(unit_m.translate_z(displacement_factor.z))

    lattice.save_stl("lattice.stl", update_normals=True)


def write_to_msh(mesh):
    msh_file = open("output/msh/unit.msh", "w")
    msh_file.write("$MeshFormat\n")
    # MESH FORMAT
    msh_file.write("2.2 0 8\n")
    msh_file.write("$EndMeshFormat\n$Nodes\n")
    # WRITE NODES HERE
    # NUM OF NODES
    msh_file.write(str(len(mesh.nodes)) + "\n")
    # NODES
    count = 0
    for node in mesh.nodes:
        count += 1
        msh_file.write(str(node.idx) + " " + str(node.x) + " " + str(node.y) + " " + str(node.z) + '\n')
    msh_file.write("$EndNodes\n$Elements\n")
    # WRITE ELEMENTS HERE
    # NUM OF ELEMENTS
    msh_file.write(str(len(mesh.elements)) + "\n")
    # ELEMENTS
    count = 0
    for element in mesh.elements:
        count = count + 1
        msh_file.write(str(count) + " " + ELEMENT_ATTRIBUTES + " " + str(element.n1) + " " + str(element.n2) + " " + str(element.n3) + '\n')
    msh_file.write("$EndElements\n")
    # new_msh_file.write("$STOP")
    msh_file.close()

def main():
    unit_mesh = Mesh
    dimension = Dimension
    unit_mesh.nodes = read_nodes()
    total_nodes = len(unit_mesh.nodes)
    print("nodes per unit: {}".format(total_nodes))
    unit_mesh.elements = read_elements()
    write_to_msh(unit_mesh)

    #val = dirname(dirname(abspath(__file__))) + "/Lattice-Structure-Computation-Program/scripts"
    #os.system(val + '/to_stl.bat output/msh/{} output/stl/{}'.format("unit.msh", "unit.stl"))

    displacement_factor = direction_delta(unit_mesh.nodes)
    print(str(displacement_factor.x) + " " + str(displacement_factor.y) + " " + str(displacement_factor.z))
    print("\ninput values for lattice structure")
    dimension.x = int(input("x: "))
    dimension.y = int(input("y: "))
    dimension.z = int(input("z: "))
    start_time = time.time()
    construct_lattice(displacement_factor, dimension)
    print("\nruntime: " + str(time.time() - start_time))

if __name__ == "__main__":
    main()
