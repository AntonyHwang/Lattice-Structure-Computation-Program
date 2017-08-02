import numpy as np
import math
import pprint
from app import Line, Node

def norm(vec):
    magnitude = np.linalg.norm(vec)
    if magnitude != 0:
      n_vec = vec / magnitude
      return n_vec
    else:
      return vec

#group lines by comapring dv
def group_lines(lines):
    idx_num = 0
    for num1 in range (1, len(lines) + 1):
        #print(lines[num1])
        if lines[num1].idx == -1:
            for num2 in range(0, len(lines)):
                if lines[num1].dv == lines[num2].dv:
                    if lines[num2].dv == -1:
                        #generate new idx number
                        idx_num += 1
                        lines[num1].idx = idx_num
                    else:
                        lines[num1].idx == lines[num2].idx
                    break
        else:
            break
    return lines

def check_exist(n, l):
    for node in l:
        #print("x: " + str(n[0]) + " " + str(node[0]) + " y: " + str(n[1]) + " " + str(node[1]) + " z: " + str(n[2]) + " " + str(node[2]))
        #print("\n")
        if (n.xyz[0] == node.xyz[0] and n.xyz[1] == node.xyz[1] and n.xyz[2] == node.xyz[2]):
            return True
    return False

def get_next_node(nodes, node_list, l_vec, dist, p_node, status):
    stop = 0
    #print(" ")
    #print("l_vec:")
    #print(l_vec)
    d = [((n.xyz - p_node) ** 2).sum() for n in nodes]
    ndx = np.argsort(d)
    n_node = nodes[ndx[0]].xyz
    #print(len(ndx))
    vec = n_node - p_node
    #print("vec:")
    #print(vec)
    a = (np.cross(vec, l_vec) == np.array([0, 0, 0])).all()
    n_dist = np.linalg.norm(vec)
    # print(dist)
    # print(n_dist)
    # print(" ")
    if n_dist > dist + 5:
        stop = 1
    if (a):
        status = 1
        node_list.append(n_node)
        new_nodes = np.delete(nodes, ndx[0])
        get_next_node(new_nodes, node_list, l_vec, dist, n_node, status)

    elif(status == 1 and stop == 1):
        #print(node_list[1], node_list[2], node_list[3])
        # print("")
        # print(node_list[1], node_list[2])
        return node_list

    else:
        new_nodes = np.delete(nodes, ndx[0])
        get_next_node(new_nodes, node_list, l_vec, dist, p_node, status)


#https://stackoverflow.com/questions/2486093/millions-of-3d-points-how-to-find-the-10-of-them-closest-to-a-given-point
def get_line(nodes, start_node):
    node_list = []
    node_list2 = []
    line = Line(-1, np.array([]), [])
    node = start_node
    node_list.append(node)
    d = [((n.xyz - node)**2).sum() for n in nodes]
    ndx = np.argsort(d)
    n_node = nodes[ndx[0]].xyz
    vec = n_node - node
    dist = np.linalg.norm(vec)
    line.dv = vec
    node_list.append(n_node)
    new_nodes = np.delete(nodes, ndx[0])
    node_list2 = (get_next_node(new_nodes, node_list, vec, dist, n_node, 0))
    print(node_list2)
    #get_next_node(new_nodes, node_list, vec, dist, n_node, 0)
    return line

#https://stackoverflow.com/questions/2486093/millions-of-3d-points-how-to-find-the-10-of-them-closest-to-a-given-point
def lines(nodes, boundary_nodes):
    lines = []
    count =0
    for node in boundary_nodes:
        #print(node.xyz)
        lines.append(get_line(nodes, node.xyz))
    #lines = group_lines(lines)
    return lines
