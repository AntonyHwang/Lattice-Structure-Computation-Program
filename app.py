class Lattice(object):
    def __init__(self, elements, nodes):
        self.elements, self.nodes = elements, nodes

class Element(object):
    def __init__(self, n1, n2, n3):
        self.n1, self.n2, self.n3 =  n1, n2, n3

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

def read_nodes(nodes):
    with open('nodes.txt') as node_file:
        for line in node_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
                    nodes.append(Node(int(words[0]), float(words[1]), float(words[2]), float(words[3])))
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
    return Node(0, maxX - minX, maxY - minY, maxZ - minZ)

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

def remove_duplicates(nodes):
    duplicates_list = [-1] * len(nodes)

    for idx in range(0, len(nodes)):
        prev = idx - 1
        if idx != 0:
            if nodes[idx].x == nodes[prev].x and nodes[idx].y == nodes[prev].y and nodes[idx].z == nodes[prev].z:
                duplicates_list[idx] = nodes[prev].idx
                # duplicates_list.append([nodes[idx].idx, nodes[prev].idx])
                nodes[idx].idx = nodes[prev].idx
    print(duplicates_list)
    print("duplicates: " + str(len(duplicates_list)))
    #duplicates_list.sort(key=lambda k: [k[0]])
    print("duplicates: " + str(len(duplicates_list)))
    return duplicates_list

def contains(list, idx):
    for x in list:
        if x[0] == idx:
            return x[1]
        else:
            return 0

def map(elements, duplicate_lists):
    for element in elements:
        n1_idx = duplicate_lists[element.n1]
        n2_idx = duplicate_lists[element.n1]
        n3_idx = duplicate_lists[element.n1]
        if n1_idx != -1:
            element.n1 = n1_idx
        if n2_idx != -1:
            element.n2 = n2_idx
        if n3_idx != -1:
            element.n3 = n3_idx
    return elements

def construct_lattice(shape, nodes, elements, total_nodes, displacement_factor, x, y, z):
    current_nodes_idx = 0

    x_nodes = []
    xy_nodes = []
    xyz_nodes = []

    x_elements = []
    xy_elements = []
    xyz_elements = []

    if shape == 90:
        for num in range(0, x):
            for node in nodes:
                x_nodes.append(Node(current_nodes_idx, node.x + num * displacement_factor.x, node.y, node.z))
            for element in elements:
                x_elements.append(Element(element.n1 + total_nodes, element.n2 + total_nodes, element.n3 + total_nodes))

        for num in range(0, y):
            for node in x_nodes:
                xy_nodes.append(Node(current_nodes_idx, node.x, node.y + num * displacement_factor.y, node.z))
            for element in x_elements:
                xy_elements.append(Element(element.n1 + total_nodes, element.n2 + total_nodes, element.n3 + total_nodes))

        for num in range(0, z):
            for node in xy_nodes:
                current_nodes_idx += 1
                xyz_nodes.append(Node(current_nodes_idx, node.x, node.y, node.z + num * displacement_factor.z))
            for element in xy_elements:
                xyz_elements.append(Element(element.n1 + total_nodes, element.n2 + total_nodes, element.n3 + total_nodes))

        print(str(len(xyz_nodes)))
        xyz_nodes.sort(key=lambda k: [k.x, k.y, k.z])
        print("num nodes: " + str(len(xyz_nodes)))
        duplicates_list = remove_duplicates(xyz_nodes)
        elements = map(xyz_elements, duplicates_list)

        nodes = list(set(xyz_nodes))
        nodes.sort(key=lambda k: [k.idx])
        return Lattice(elements, nodes)

def write_to_file(lattice):
    new_node_file = open("output/nodes.txt", "w")
    for node in lattice.nodes:
        new_node_file.write("\t" + str(node.idx) + "\t" + str(node.x) + "\t" + str(node.y) + "\t" + str(node.z) + '\n')
    new_node_file.close()

    new_element_file = open("output/elements.txt", "w")
    count = 0
    for element in lattice.elements:
        count = count + 1
        new_element_file.write("\t" + str(count) + "\t" + lattice.nodes[element.n1].toString() + "\t" + lattice.nodes[element.n2].toString() + "\t" + lattice.nodes[element.n3].toString() + '\n')
    new_element_file.close()

def main():
    nodes = []
    elements = []
    nodes = read_nodes(nodes)
    total_nodes = len(nodes)
    print("nodes per unit: {}".format(total_nodes))
    elements = read_elements(elements)
    displacement_factor = direction_delta(nodes)
    print(str(displacement_factor.x) + " " + str(displacement_factor.y) + " " + str(displacement_factor.z))
    lattice = construct_lattice(90, nodes, elements, total_nodes, displacement_factor, 10, 10, 10)
    write_to_file(lattice)

if __name__ == "__main__":
    main()
