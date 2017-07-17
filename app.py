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
        self.x, self.y, self.z = x, y, z
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

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

def get_xyz(list, idx):
    try:
        return list[idx]
    except:
        return idx


def get_idx(list, node):
    return list.index(node)

def construct_lattice(shape, nodes, elements, total_nodes, displacement_factor, x, y, z):

    unique_nodes = list(set(nodes))
    duplicates = 0
    # new_index = 0;
    # node_index = 0
    # new_nodes = []
    x_nodes = []
    xy_nodes = []
    xyz_nodes = []

    # x_elements = []
    # xy_elements = []
    # xyz_elements = []

    if shape == 90:
        for num1 in range(0, x):
            for node in nodes:
                x_nodes.append(Node(node.x + num1 * displacement_factor.x, node.y, node.z))

        for num2 in range(0, y):
            for node in x_nodes:
                xy_nodes.append(Node(node.x, node.y + num2 * displacement_factor.y, node.z))

        for num3 in range(0, z):
            for node in xy_nodes:
                xyz_nodes.append(Node(node.x, node.y, node.z + num3 * displacement_factor.z))

        for node in xyz_nodes:
            if node not in unique_nodes:
                unique_nodes.append(node)
            else:
                duplicates += 1

        print("uniq nodes: " + str(len(unique_nodes)))

        # for element_num in range(0, x * y * z - 1):
        #     elements.append(Element(0, 0, 0))
        #     n1_idx = get_idx(unique_nodes, get_xyz(xyz_nodes, elements[element_num].n1))
        #     n2_idx = get_idx(unique_nodes, get_xyz(xyz_nodes, elements[element_num].n2))
        #     n3_idx = get_idx(unique_nodes, get_xyz(xyz_nodes, elements[element_num].n3))
        #     elements[element_num].n1 = n1_idx
        #     elements[element_num].n2 = n2_idx
        #     elements[element_num].n3 = n3_idx

        print("duplicates identified: " + str(duplicates))
        # #uncomment to test repeats
        #return Lattice(list(set(xyz_elements)), list(set(xyz_nodes)))

        # uncomment to test elements
        return Lattice(elements, unique_nodes)

def write_to_file(lattice):
    new_node_file = open("output/nodes.txt", "w")
    count = 0
    for node in lattice.nodes:
        count = count + 1
        new_node_file.write("\t" + str(count) + "\t" + str(node.x) + "\t" + str(node.y) + "\t" + str(node.z) + '\n')
    new_node_file.close()

    # new_element_file = open("output/elements.txt", "w")
    # count = 0
    # for element in lattice.elements:
    #     count = count + 1
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
