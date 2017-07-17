#METHOD !
# class Lattice(object):
#     def __init__(self, elements, nodes):
#         self.elements, self.nodes = elements, nodes
#
# class Element(object):
#     def __init__(self, idx, n1, n2, n3):
#         self.idx, self.n1, self.n2, self.n3 = idx, n1, n2, n3
#
#
# class Node(object):
#     def __init__(self, idx, x, y, z):
#         self.idx, self.x, self.y, self.z = x, y, z
#     def __hash__(self):
#     	return hash((self.idx, self.x, self.y, self.z))
#     def __eq__(self, other):
#     	return self.idx == other.idx, self.x == other.x and self.y == other.y and self.z == other.z
#     def toString(self):
#     	return "(" + str(self.idx) +"," + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
#######################################################################################################################

#METHOD 2
class Lattice(object):
    def __init__(self, elements, nodes):
        self.elements, self.nodes = elements, nodes

class Element(object):
    def __init__(self, n1, n2, n3):
        self.n1, self.n2, self.n3 = n1, n2, n3

class Node(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)
    def toString(self):
    	return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
#######################################################################################################################

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

def read_elements(elements):
    with open('elements.txt') as element_file:
        for line in element_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
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
    return Node(maxX - minX, maxY - minY, maxZ - minZ)

def check_node_existence(list, n):
    if n in list:
        return 1
    else:
        return 0

def construct_lattice(shape, nodes, elements, total_nodes, displacement_factor, x, y, z):
    duplicates = 0
    new_index = 0;
    node_index = 0
    x_nodes = []
    xy_nodes = []
    xyz_nodes = []

    x_elements = []
    xy_elements = []
    xyz_elements = []

    if shape == 90:
        for num in range(0, x):
            for node in nodes:
                if check_node_existence(nodes, Node(node.x + num * displacement_factor.x, node.y, node.z)):
                    #x_elements.append(Element(element.n1 + num * total_nodes - duplicates, element.n2 + num * total_nodes - duplicates, element.n3 + num * total_nodes - duplicates))
                    x_nodes.append(Node(node.x + num * displacement_factor.x, node.y, node.z))
                    count = count + 1
                else:
                    duplicates = duplicates + 1
                    # for element in elements:
                    #     if element.n1 == node_index:
                    #         element.n1 = new_index
                    #     if element.n2 == node_index:
                    #         element.n2 = new_index
                    #     if element.n3 == node_index:
                    #         element.n3 = new_index
            # node_index = node_index + 1
            for element in elements:
                x_elements.append(
                    Element(element.n1 + num * total_nodes - duplicates,
                            element.n2 + num * total_nodes - duplicates,
                            element.n3 + num * total_nodes - duplicates))

        for num in range(0, y):
            for node in x_nodes:
                for node in nodes:
                    if check_node_existence(nodes, Node(node.x + num * displacement_factor.x, node.y, node.z)):
                        # x_elements.append(Element(element.n1 + num * total_nodes - duplicates, element.n2 + num * total_nodes - duplicates, element.n3 + num * total_nodes - duplicates))
                        xy_nodes.append(Node(node.x + num * displacement_factor.x, node.y, node.z))
                        count = count + 1
                    else:
                        duplicates = duplicates + 1
                        # for element in elements:
                        #     if element.n1 == node_index:
                        #         element.n1 = new_index
                        #     if element.n2 == node_index:
                        #         element.n2 = new_index
                        #     if element.n3 == node_index:
                        #         element.n3 = new_index
                # node_index = node_index + 1
                for element in elements:
                    xy_elements.append(
                        Element(element.n1 + num * total_nodes - duplicates,
                                element.n2 + num * total_nodes - duplicates,
                                element.n3 + num * total_nodes - duplicates))
        for num in range(0, z):
            for node in nodes:
                if check_node_existence(nodes, Node(node.x + num * displacement_factor.x, node.y, node.z)):
                    #x_elements.append(Element(element.n1 + num * total_nodes - duplicates, element.n2 + num * total_nodes - duplicates, element.n3 + num * total_nodes - duplicates))
                    xyz_nodes.append(Node(node.x + num * displacement_factor.x, node.y, node.z))
                    count = count + 1
                else:
                    duplicates = duplicates + 1
                    # for element in elements:
                    #     if element.n1 == node_index:
                    #         element.n1 = new_index
                    #     if element.n2 == node_index:
                    #         element.n2 = new_index
                    #     if element.n3 == node_index:
                    #         element.n3 = new_index
            # node_index = node_index + 1
            for element in elements:
                xyz_elements.append(
                    Element(element.n1 + num * total_nodes - duplicates, element.n2 + num * total_nodes - duplicates, element.n3 + num * total_nodes - duplicates))

        #removes duplicates
        # new_nodes = list(set(xyz_nodes))
        # new_elements = list(set(xyz_elements))
        print("duplicates idenetified: " + str(duplicates))
        # #uncomment to test repeats
        #return Lattice(list(set(xyz_elements)), list(set(xyz_nodes)))

        # uncomment to test elements
        return Lattice(xyz_elements, xyz_nodes)

def write_to_file(lattice):
    new_node_file = open("output/nodes.txt", "w")
    count = 0
    for node in lattice.nodes:
        count = count + 1
        new_node_file.write("\t" + str(count) + "\t" + str(node.x) + "\t" + str(node.y) + "\t" + str(node.z) + '\n')
    new_node_file.close()

    new_element_file = open("output/elements.txt", "w")
    count = 0
    for element in lattice.elements:
        count = count + 1
    #     new_element_file.write("\t" + str(count) + "\t" + lattice.nodes[element.n1].toString() + "\t" + lattice.nodes[element.n2].toString() + "\t" + lattice.nodes[element.n3].toString() + '\n')
    # new_element_file.close()

def main():
    nodes = []
    elements = []
    nodes = read_nodes(nodes)
    total_nodes = len(nodes)
    print("nodes per unit: {}".format(total_nodes))
    elements = read_elements(elements)
    displacement_factor = direction_delta(nodes)
    print(str(displacement_factor.x) + " " + str(displacement_factor.y) + " " + str(displacement_factor.z))
    lattice = construct_lattice(90, nodes, elements, total_nodes, displacement_factor, 2, 2, 2)
    write_to_file(lattice)

if __name__ == "__main__":
    main()
