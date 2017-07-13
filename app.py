class Element(object):
    def __init__(self, n1, n2, n3):
        self.n1, self.n2, self.n3 = n1, n2, n3

class Node(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

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
                    elements.append(Element(words[6], words[7], words[8]))
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

def construct_lattice(shape, nodes, elements, displacement_factor, x, y, z):
    if shape == 90:
        x_nodes = []
        xy_nodes = []
        xyz_nodes = []
        for num in range(0, x):
            for node in nodes:
                x_nodes.append(Node(node.x + displacement_factor.x, node.y, node.z))
        for num in range(0, y):
            for node in x_nodes:
                xy_nodes.append(Node(node.x, node.y + displacement_factor.y, node.z))
        for num in range(0, z):
            for node in xy_nodes:
                xyz_nodes.append(Node(node.x, node.y, node.z + displacement_factor.z))
        return xyz_nodes

def write_to_file(nodes, elements):
    new_node_file = open("output/nodes.txt", "w")
    new_node_file.write('\n')
    new_node_file.write(" LIST ALL SELECTED NODES.   DSYS=      0\n")
    new_node_file.write(" SORT TABLE ON  NODE  NODE  NODE\n")
    new_node_file.write('\n')
    count = 0
    for node in nodes:
        count = count + 1
        new_node_file.write("\t" + str(count) + "\t" + str(node.x) + "\t" + str(node.y) + "\t" + str(node.z) + '\n')
    new_node_file.close()

def main():
    nodes = []
    elements = []
    nodes = read_nodes(nodes)
    elements = read_elements(elements)
    displacement_factor = direction_delta(nodes)
    print(str(displacement_factor.x) + " " + str(displacement_factor.y) + " " + str(displacement_factor.z))
    nodes = construct_lattice(90, nodes, elements, displacement_factor, 10, 10, 10)
    #calculate elements
    write_to_file(nodes, elements)

if __name__ == "__main__":
    main()