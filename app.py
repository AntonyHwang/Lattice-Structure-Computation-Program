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

def construct_lattice(nodes, elements, x, y, z):
    

def main():
    nodes = []
    elements = []
    nodes = read_nodes(nodes)
    elements = read_elements(elements)
    displacement_factor = direction_delta(nodes)
    print(str(displacement_factor.x) + " " + str(displacement_factor.y) + " " + str(displacement_factor.z))
    construct_lattice(nodes, elements, 10, 10, 10)

if __name__ == "__main__":
    main()