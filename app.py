import sys
import time
import numpy as np
import math
import progressbar
import beam
import remap
import gmsh_conversion as converter


class Lattice(object):
    # A collection of nodes and elements

    # Attributes:
    #     Elements: A list of Element objects
    #     Nodes: A list of Node objects
    

    def __init__(self, elements, nodes):
        # Constructor

        # Args:
        #     elements: A list representing elements in the lattice. This could be passed in empty and filled in later
        #     nodes: A list representing nodes in the lattice. This could be passed in empty and filled in later
        
        self.elements, self.nodes = elements, nodes


class Line(object):
    # Defines a Line, made up of nodes connected by a direction vector

    # Attributes:
    #     idx: An Integer representing an "id" for the line
    #     dv: A numpy (np) array that specifies the direction vector of the line
    #     nodes: A list of Node objects that lie on the line 
    

    def __init__(self, idx, dv, nodes):
        # Constructor

        # Args:
        #     idx: The index or identification number of the line. Default value is -1 meaning no id.
        #     dv: A numpy array that represents the direction vector
        #     nodes: The list of nodes on the line. Should be assigned in beam.py 
        

        self.idx, self.dv, self.nodes = -1, dv, nodes

    def toString(self):
        # Returns a string of the line formatted as 'vector: [dv[0] dv[1] dv[2]]    idx: [idx]    nodes'

        # Returns:
        #     A str of the Line obj formatted as 'vector: [dv[0] dv[1] dv[2]]    idx: [idx]   nodes'
        
        return "vector: [" + str(self.dv[0]) + " " + str(self.dv[1]) + " " + str(self.dv[2]) + "]\tidx: ["+ str(self.idx) +"]\tnodes "# + str(self.nodes)

    def __hash__(self):
        # Returns a hash of the direction vector

        return hash(self.dv[0], self.dv[1], self.dv[2])

    def __eq__(self, other):
        # Equates lines (allows '==') using the direction vectors. Checks if it is a scalar with the others

        return self.dv[0] / other.dv[0] == self.dv[1] / other.dv[1] and self.dv[1] / other.dv[1] == self.dv[2] / other.dv[2]

    def append(self, node):
        # Appends a node to the nodes list

        # Args:
        #     node: Node object to be appended to line

        self.nodes.append(node)


class Node(object):
    # Defines a Node much like that from a .msh. Represents a coordinate,

    # Attributes:
    #     xyz: A numpy array representing the coordinates of the Node
    #          xyz[0] == x coordinate
    #          xyz[1] == y coordinate
    #          xyz[2] == z coordinate
    
    def __init__(self, x, y, z):
    # Constructor
    
    # Args:
    #     x: Number (float) repersenting the x value
    #     y: Number (float) representing the y value
    #     z: Number (float) representing the z value

        self.xyz = np.array([x,y,z])
    
    def __hash__(self):
    # Returns a hash of the Node based on the x,y,z values

        return hash(self.xyz[0], self.xyz[1], self.xyz[2])
    
    def __eq__(self, other):
    # Enables the use of '==' to find equality between Nodes, even Nodes with a numpy array

    # Raises:
    #     TypeError: An error occured with the type that you are comparing

        try:
            return (self.xyz[0] == other.xyz[0] and self.xyz[1] == other.xyz[1] and self.xyz[2] == other.xyz[2])
        except:
            try:
                return self.xyz[0] == other[0] and self.xyz[1] == other[1] and self.xyz[2] == other[2]
            except:
                raise TypeError('Cannot compare type \'' + str(type(other)) + '\' with \'Node\' type')

    def toString(self):
        # Returns a str representation of the Node

        # Returns:
        #     A str represntation of the Node. Ex. 'x y z'

        return str(self.xyz[0]) + ' ' + str(self.xyz[1]) + ' ' + str(self.xyz[2])


class Element(object):
    # An Element much like that defined in a mesh or .msh

    # Attributes:
    #     nodes: A numpy array that holds all the nodes in the element. Only supports triangular elements
    #     attributes: A list of material attribute values for the mesh. This is default set to 2 2 0 1.
    #                 The third index in attributes represents the id of the element (which beam it belongs to)

    def __init__(self, n1, n2, n3):
    # Constructor. Atributes are default set to 2 2 0 1

    # Args:
    #     n1, n2, n3: Node objects that are passed in and set to the nodes list.

        self.nodes = np.array([n1, n2, n3])
        self.attributes = [2,2,0,1]
    
    def __hash__(self):
    # Returns a hash of the Element id.

        return hash(self.attributes[3])
    
    def __eq__(self,other):
    # Enables the use of '==' to find equality between elements. Compares by nodes.

        return self.n1 == other.n1 and self.n2 == other.n2 and self.n3 == other.n3
    
    def set_beam(self, beam_id):
    # Sets the beam id of the Element

    # Args:
    #     beam_id: The beam id number for the element

        self.attributes[3] = beam_id

    def align_with_beam(self, beam):
    # Sets the beamid of the Elemnt to the id of a Line passed in

    # Args:
    #     Line to pull id from

        self.attributes[3] = beam.idx
        #print("new attributes: " + self.attributes_string())
    
    def attributes_string(self):
    # Returns a string of material attributes for printing. Ex. '2 2 0 1'

    # Returns:
    #     A string of material attributes for printing. Ex. '2 2 0 1'

        return str(self.attributes[0]) + ' ' + str(self.attributes[1]) + ' ' + str(self.attributes[2]) + ' ' + str(self.attributes[3])

    def toString(self):
        return self.attributes_string() + ' ' +  self.nodes[0].toString() + ' ' +  self.nodes[1].toString() + ' ' +  self.nodes[2].toString()


class Beam(object):
    # Defines a beam object

    # Attributes:
    #     idx: An Integer that identifies a beam
    #     nodes: A list of Node objects in the beam
    
    def __init__(self, idx, b_nodes, nodes):
    # Constructor

    # Args:
    #     idx: An int that identifies the beam
    #     nodes: A list of Node objects in the beam. Can be empty and filled in later

        self.idx, self.b_nodes, self.nodes = idx, b_nodes, nodes

    def append(self, node):
    # Appends a node the the beam

    # Args:
    #     node: A Nod eobject to append to the numpy array in the beam

        self.nodes = np.append(self.nodes, node)
    
    def toString(self):
    # Returns a string representation of the Beam

    # Returns:
    #     A string representation of the Beam. Ex. 'idx: [idx]    nodes: [pointers]'
    
        return "idx: [" + str(self.idx) + "]\tnodes: [" + str(self.nodes) + "]"


def is_number(s):
    # Checks if the argument 's' is a float

    # Args:
    #     s: Object to check

    # Raises:
    #     ValueError: if 's' is not a float

    try:
        float(s)
        return True
    except ValueError:
        return False


def read_nodes(model):
    # Reads a ANSYS ASCII nodes file.

    # Returns:
    #     A list of nodes read from the node file

    nodes = []
    with open(model) as node_file:
        for line in node_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
                    nodes.append(Node(float(words[1]), float(words[2]), float(words[3])))
    node_file.close()
    return nodes


def read_elements(model, nodes):
    # Reads an ANSYS ASCII elements file. Needs to be named 'elements.txt' and be placed in the working directory
    
    # Returns:
    #     A list of elements read from the elements file

    elements = []
    global ELEMENT_ATTRIBUTES
    flag = False
    with open(model) as element_file:
        for line in element_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
                    if not flag:
                        flag = True
                    elements.append(Element(nodes[int(words[6]) - 1], nodes[int(words[7]) - 1], nodes[int(words[8]) - 1]))
    element_file.close()
    return elements


def read_msh(file):
# Reads a .msh file and returns a list of nodes and elements

# Args:
#     file: The path to the file needed to be read including the name (excluding the .msh extension)

# Returns:
#     nodes, elements: A list of nodes and elements respectively read from the .msh file


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
                            elements.append(Element(nodes[int(words[len(words) - 3]) - 1],
                                                    nodes[int(words[len(words) - 2]) - 1],
                                                    nodes[int(words[len(words) - 1]) - 1]))
                        elif words[0] == "$EndElements":
                            read_elements = False
    mesh.close()
    return nodes, elements


def normal(element):
# Calculates the normal of an element
    
# Args:
#     element: An element to find the normal of

# Returns:
#     a numpy array representing the normal of the element


    p1 = np.array([element.nodes[0].xyz[0], element.nodes[0].xyz[1], element.nodes[0].xyz[2]]) / math.sqrt((element.nodes[0].xyz[0] * element.nodes[0].xyz[0]) + (element.nodes[0].xyz[1] * element.nodes[0].xyz[1]) + (element.nodes[0].xyz[2] * element.nodes[0].xyz[2]))
    p2 = np.array([element.nodes[1].xyz[0], element.nodes[1].xyz[1], element.nodes[1].xyz[2]]) / math.sqrt((element.nodes[1].xyz[0] * element.nodes[1].xyz[0]) + (element.nodes[1].xyz[1] * element.nodes[1].xyz[1]) + (element.nodes[1].xyz[2] * element.nodes[1].xyz[2]))
    p3 = np.array([element.nodes[2].xyz[0], element.nodes[2].xyz[1], element.nodes[2].xyz[2]]) / math.sqrt((element.nodes[2].xyz[0] * element.nodes[2].xyz[0]) + (element.nodes[2].xyz[1] * element.nodes[2].xyz[1]) + (element.nodes[2].xyz[2] * element.nodes[2].xyz[2]))

    u = p2 - p1
    v = p3 - p1

    return np.cross(u, v)


def direction_delta(nodes):
# Returns a Node representing the max displacements between nodes

# Args:
#     nodes: A list of Node objects

# Returns:
#     A Node object where the x,y,z values represent the max displacements between nodes


    maxX = max(node.xyz[0] for node in nodes)
    minX = min(node.xyz[0] for node in nodes)
    maxY = max(node.xyz[1] for node in nodes)
    minY = min(node.xyz[1] for node in nodes)
    maxZ = max(node.xyz[2] for node in nodes)
    minZ = min(node.xyz[2] for node in nodes)
    return Node(maxX - minX, maxY - minY, maxZ - minZ)


def max_xyz(nodes):
# Finds the max values of a given list of nodes

# Args:
#     nodes: A list of Node objects to check

# Returns:
#     A list with three floats, a maximum x, y, and z


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



def generate_stl(nodes, elements, x, y, z):
# Generate a .stl file that represents a lattice volume

# Writes triangular elements to an stl file. This tracks just elements and 
# coordinates, so this will handle duplicate nodes.

# Args:
#     nodes: A list of nodes to be written
#     elements: A list of elements to be written
#     x: A 'x' length of the volume 
#     y: A 'y' length of the volume
#     z: A 'z' length of the volume

    displacement_factor = direction_delta(nodes)
    total_nodes = len(nodes)

    output = open("output/lattice.stl", 'w')
    output.write("solid Created by LatticeGenerator\n")

    bar = progressbar.ProgressBar(max_value=(x*y*z))
    
    # Progressbar Variables
    count = 0
    fraction = (x * y * z) * 0.01 # CHANGE FRACTION TO MAKE PROGRESSBAR SMOOTH

    # tracks the difference between current shape and original unit
    x_delta = 0
    y_delta = 0
    z_delta = 0

    for curr_x in range(0,x):
        y_delta = 0
        
        for curr_y in range(0,y):
            z_delta = 0
            
            for curr_z in range(0,z):
                count += 1
                if count % fraction <= 1:
                    bar.update(count)

                for e in elements:
                    norm = normal(e)
                    output.write("facet normal " + str(norm[0])
                            + ' ' + str(norm[1])
                            + ' ' + str(norm[2]) + ' ' + '\n')
                    # print(normal)
                    output.write("\touter loop" + '\n')
                    output.write("\t\tvertex " + str(e.nodes[0].xyz[0] + x_delta) +
                                 ' ' + str(e.nodes[0].xyz[1] + y_delta) +
                                 ' ' + str(e.nodes[0].xyz[2] + z_delta) + '\n')
                    output.write("\t\tvertex " + str(e.nodes[1].xyz[0] + x_delta) +
                                 ' ' + str(e.nodes[1].xyz[1] + y_delta) +
                                 ' ' + str(e.nodes[1].xyz[2] + z_delta) + '\n')
                    output.write("\t\tvertex " + str(e.nodes[2].xyz[0] + x_delta) +
                                 ' ' + str(e.nodes[2].xyz[1] + y_delta) +
                                 ' ' + str(e.nodes[2].xyz[2] + z_delta) + '\n')
                    output.write("\tendloop" + '\n')
                    output.write("endfacet" + '\n')
                z_delta += displacement_factor.xyz[2]
            y_delta += displacement_factor.xyz[1]
        x_delta += displacement_factor.xyz[0]
    output.write("endsolid Created by LatticeGenerator")


def find_boundries(nodes):
    # find the nodes on the edges of a list of nodes

    # Takes a list of nodes and finds the nodes that line up with the max and min
    # values.

    # Args:
    #     nodes: A list of Node objects to be checked

    # Return:
    #     A list of nodes sitting at the boundries

    max_values = max_xyz(nodes)
    boundry_nodes = []
    displacement_factor = direction_delta(nodes)
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

    # print("there are " + str(len(boundry_nodes)) + " out of " + str(len(nodes)) + " boundry nodes")
    return boundry_nodes


def find_m_point(max_values, displacement_factor):
    # Uses maximum values of a collection of nodes to find the mid point

    # This is intended for use on a unit lattice. Uses max values and half of max displacement
    # to find the mid point of a unit lattice

    # Args:
    #     max_values: A list in the format of the result of max_xyz where [x,y,z]
    #     displacement_factor: A node representing the maximum displacements between x, y, and z
    # Returns:
    #     A numpy array with three elements where [x,y,z] that represents the mid point
    
    m_point = np.array([0.0, 0.0, 0.0])
    m_point[0] = max_values[0] - displacement_factor.xyz[0] / 2
    m_point[1] = max_values[1] - displacement_factor.xyz[1] / 2
    m_point[2] = max_values[2] - displacement_factor.xyz[2] / 2
    return m_point


def assign_beams(elements, beams):
    # Assigns nodes and elements to beams
    
    # Uses the functions in beam.py to find beams. Then assigns the elements to beams

    # Args:
    #     nodes: A list of Node objects
    #     elements: A list of Element objects

    for beam_n in beams:
        for e in elements:
            if e.nodes[0] in beam_n.nodes and e.nodes[1] in beam_n.nodes and e.nodes[2] in beam_n.nodes:
                e.align_with_beam(beam_n)


def to_first_ocant(nodes):
    # Moves all nodes to the first quadrant

    # if any value of nodes is negative, shifts the whole list of nodes to positive.

    # Args:
    #     nodes: A list of nodes to be operated on. Passed in and edited by reference

    minX = nodes[0].xyz[0]
    minY = nodes[0].xyz[1]
    minZ = nodes[0].xyz[2]

    for n in nodes:
        if minX > n.xyz[0]:
            minX = n.xyz[0]
        if minY > n.xyz[1]:
            minY = n.xyz[1]
        if minZ > n.xyz[2]:
            minZ = n.xyz[2]

    diff = [minX,minY,minZ]
    if minX < 0:
        diff[0] = minX * -1
    if minY < 0:
        diff[1] = minY * -1
    if minZ < 0:
        diff[2] = minZ * -1

    for n in nodes:
        n.xyz[0] += diff[0]
        n.xyz[1] += diff[1]
        n.xyz[2] += diff[2]


def main():
    model = int(input("45 or 90?: "))
    nodes = []
    elements = []
    nodes = read_nodes(str(model) + '\\nodes.txt')
    elements = read_elements(str(model) + '\\elements.txt', nodes)
    # nodes, elements = read_msh("lattice")
    displacement_factor = direction_delta(nodes)

    to_first_ocant(nodes)    

    beams = []

    if model == 90:
        max_values = max_xyz(nodes)
        boundry_nodes = find_boundries(nodes)
        mid_point = find_m_point(max_values, displacement_factor)
        beams = beam.beams([n for n in nodes if n not in boundry_nodes], boundry_nodes, mid_point)

    if model == 45:
        beams = beam.beams_by_octant(nodes, find_m_point(max_xyz(nodes), displacement_factor))


    assign_beams(elements, beams)

    #nodes = read_nodes()
    print("nodes per unit: {}".format(len(nodes)))
    #elements = read_elements(nodes)

    print("\ninput values for lattice structure")
    x = int(input("x: "))
    y = int(input("y: "))
    z = int(input("z: "))
    start_time = time.time()
    generate_stl(nodes, elements, x, y, z)

    print("\n\nConverting .stl to .msh...")
    converter.stl_to_msh('output\\lattice', 'output\\lattice')

    print("\n\nAssigning elements to beams...")
    remap.write_properties_on_mesh('output/lattice',elements, len(nodes), len(beams), x, y, z)
    print("\nruntime: " + str(time.time() - start_time))

    #converter.view_msh('output\\lattice.msh')


if __name__ == "__main__":
    main()
