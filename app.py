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
        data = node_file.readlines()
        for line in data:
            if not line.strip():
                words = line.split()
                if is_number(words[0]):
                    nodes.append(Node(words[1], words[2], words[3]))
                    print(nodes)
    node_file.close()

def main():
    nodes = []
    read_nodes(nodes)