# import progressbar
# from time import sleep

class Lattice(object):
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

def read_nodes(nodes):
    with open('nodes.txt') as node_file:
        for line in node_file:
            if not line.strip():
                continue
            else:
                words = line.split()
                if is_number(words[0]):
                    nodes.append(Node(int(words[0]),float(words[1]), float(words[2]), float(words[3])))
    node_file.close()
    return nodes

def read_elements(elements):
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

def remove_duplicates(nodes):
    max_node_num = max(node.idx for node in nodes)
    duplicates_list = [-1] * max_node_num
    for i in range(0, len(nodes)):
        prev = i - 1
        if i != 0:
            if nodes[i].x == nodes[prev].x and nodes[i].y == nodes[prev].y and nodes[i].z == nodes[prev].z:
                duplicates_list[nodes[i].idx - 1] = nodes[prev].idx
                nodes[i].idx = nodes[prev].idx
    return duplicates_list

def map(elements, duplicate_lists):
    for element in elements:
        n1_idx = duplicate_lists[element.n1 - 1]
        n2_idx = duplicate_lists[element.n2 - 1]
        n3_idx = duplicate_lists[element.n3 - 1]
        if n1_idx != -1:
            element.n1 = n1_idx
        if n2_idx != -1:
            element.n2 = n2_idx
        if n3_idx != -1:
            element.n3 = n3_idx
    return elements

# construct a lattice from an already existing unit structure
# could be purposed into multiplying larger lattices as well
# INTUITION: attempt to construct lattice by actively writing as oppsed to storing
#            data to write in a seperate function. This should make program functional 
#            for large values but will make runtime slower and result in a less modular
#            program overall
def generate_lattice(nodes, elements, total_nodes, displacement_factor, x, y, z):
    model = Lattice(elements, nodes)

    output = open("output/test.msh","w")
    output.write("$MeshFormat\n")
    # MESH FORMAT
    output.write("2.2 0 8\n")
    output.write("$EndMeshFormat\n$Nodes\n")
    # WRITE NODES HERE
    # NUM OF NODES
    output.write(str((x * y * z) * len(model.nodes)) + "\n")
    print("total: " + str((x * y * z) * len(model.nodes)))
    multiplier = 0
    for num1 in range(0,x):
        for num2 in range (0,y):
            for num3 in range(0,z):
                for n in model.nodes:
                    output.write(str(n.idx + total_nodes * multiplier) +
                                 " " + str(n.x + num1 * displacement_factor.x) +
                                 " " + str(n.y + num2 * displacement_factor.y) +
                                 " " + str(n.z + num3 * displacement_factor.z) + '\n')
                multiplier += 1
    output.write("$EndNodes\n$Elements\n")
    output.write(str((x * y * z) * len(model.elements)) + "\n")

    multiplier = 0
    count = 0
    for num1 in range(0,x):
        for num2 in range (0,y):
            for num3 in range(0,z):
                for e in model.elements:
                    count += 1
                    output.write(str(count) + " " + ELEMENT_ATTRIBUTES + 
                                       " " + str(e.n1 + multiplier * total_nodes) + 
                                       " " + str(e.n2 + multiplier * total_nodes) + 
                                       " " + str(e.n3 + multiplier * total_nodes) + '\n')
                multiplier +=1
    output.write("$EndElements\n")
    output.close()

def construct_lattice(shape, nodes, elements, total_nodes, displacement_factor, x, y, z):
    final_nodes = []
    final_elements = []
    Emax = 0
    prev = -1
    emultiplier = 0

    # print("Constructing Lattice...")
    # bar = progressbar.ProgressBar(maxval= (x * y * z), \
    # widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    # bar.start()
    
    for num1 in range (0, x):
        for num2 in range (0, y):
            for num3 in range (0, z):

                # bar.update(i+1)
                
                if(prev != emultiplier):
                    #print("multiplier is now " + str(emultiplier))
                    prev = emultiplier
                #print("will add " + str(emultiplier * total_nodes) + " to each node index")
                for node in nodes:
                    #print("(" + str(node.x + num1 * displacement_factor.x) + "," + str(node.y + num2 * displacement_factor.y) + "," + str(node.z + num3 * displacement_factor.z) + ")\t" + str(len(final_nodes)))
                    temp = Node(node.idx + emultiplier * total_nodes, node.x + num1 * displacement_factor.x, node.y + num2 * displacement_factor.y, node.z + num3 * displacement_factor.z)
                    final_nodes.append(temp)
                for e in elements:
                    temp = Element(e.n1 + emultiplier * total_nodes, e.n2 + emultiplier * total_nodes, e.n3 + emultiplier * total_nodes)
                    Emax = max([temp.n1, temp.n2, temp.n3, Emax])
                    #print(temp.toString())
                    final_elements.append(temp)
                emultiplier +=1
    # bar.finish()
    final_nodes.sort(key=lambda k: [k.x, k.y, k.z])
    duplicates_list = remove_duplicates(final_nodes)
    final_elements = map(final_elements, duplicates_list)
    final_nodes = list(set(final_nodes))
    final_nodes.sort(key=lambda k: [k.idx])

    return Lattice(final_elements, final_nodes)

def write_to_file(lattice):
    print("writing " + str(len(lattice.nodes)) +" nodes...")
    new_node_file = open("output/nodes.txt", "w")
    count = 0
    for node in lattice.nodes:
        new_node_file.write("\t" + str(node.idx) + "\t" + str(node.x) + "\t" + str(node.y) + "\t" + str(node.z) + '\n')
    new_node_file.close()

    print("writing " + str(len(lattice.elements)) + " elements...")
    new_element_file = open("output/elements.txt", "w")
    count = 0
    for element in lattice.elements:
        count = count + 1
        new_element_file.write("\t" + str(count) + "\t" + str(element.n1) + "\t" + str(element.n2) + "\t" + str(element.n3) + '\n')
    new_element_file.close()

    new_msh_file = open("output/lattice.msh", "w")
    new_msh_file.write("$MeshFormat\n")
    # MESH FORMAT
    new_msh_file.write("2.2 0 8\n")
    new_msh_file.write("$EndMeshFormat\n$Nodes\n")
    # WRITE NODES HERE
    # NUM OF NODES
    new_msh_file.write(str(len(lattice.nodes)) + "\n")
    # NODES
    count = 0
    for node in lattice.nodes:
        count += 1
        new_msh_file.write(str(node.idx) + " " + str(node.x) + " " + str(node.y) + " " + str(node.z) + '\n')
    new_msh_file.write("$EndNodes\n$Elements\n")
    # WRITE ELEMENTS HERE
    # NUM OF ELEMENTS
    new_msh_file.write(str(len(lattice.elements)) + "\n")
    # ELEMENTS
    count = 0
    for element in lattice.elements:
        count = count + 1
        new_msh_file.write(str(count) + " " + ELEMENT_ATTRIBUTES + " " + str(element.n1) + " " + str(element.n2) + " " + str(element.n3) + '\n')
    new_msh_file.write("$EndElements\n")
    # new_msh_file.write("$STOP")
    new_msh_file.close()

def main():
    nodes = []
    elements = []
    nodes = read_nodes(nodes)
    total_nodes = nodes[len(nodes) - 1].idx
    print("nodes per unit: {}".format(total_nodes))
    elements = read_elements(elements)
    displacement_factor = direction_delta(nodes)
    print(str(displacement_factor.x) + " " + str(displacement_factor.y) + " " + str(displacement_factor.z))
    print("\ninput values for lattice structure")
    x = int(input("x: "))
    y = int(input("y: "))
    z = int(input("z: "))
    unit_lattice = construct_lattice(90, nodes, elements, total_nodes, displacement_factor, 1, 1, 1)
    generate_lattice(unit_lattice.nodes, unit_lattice.elements, total_nodes, displacement_factor, x, y, z)
    write_to_file(unit_lattice)

if __name__ == "__main__":
    main()
