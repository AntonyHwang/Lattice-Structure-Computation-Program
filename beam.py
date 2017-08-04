import numpy as np
import math
import pprint
from app import Line, Node, Beam

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
    for num1 in range (0, len(lines)):
        if lines[num1].idx == -1:
          for num2 in range(0, len(lines)):
              #print("")
              # print(num1, num2)
              if num1 != num2:
                  if (np.array_equal(lines[num1].dv,lines[num2].dv)):
                      if lines[num1].idx == -1:
                          if lines[num2].idx == -1:
                              idx_num += 1
                              lines[num1].idx = idx_num
                              lines[num2].idx = idx_num
                          else:
                              lines[num1].idx = lines[num2].idx
                      else:
                          lines[num2].idx = lines[num1].idx
    return lines

def check_exist(n, l):
    for node in l:
        #print("x: " + str(n[0]) + " " + str(node[0]) + " y: " + str(n[1]) + " " + str(node[1]) + " z: " + str(n[2]) + " " + str(node[2]))
        #print("\n")
        if (n.xyz[0] == node.xyz[0] and n.xyz[1] == node.xyz[1] and n.xyz[2] == node.xyz[2]):
            return True
    return False

def get_next_node(mid_point, nodes, node_list, l_vec, dist, p_node, status):
    d = [((n.xyz - p_node) ** 2).sum() for n in nodes]
    ndx = np.argsort(d)
    n_node = nodes[ndx[0]].xyz
    vec = n_node - p_node
    m_vec = mid_point - p_node
    on_line = (np.cross(vec, l_vec) == np.array([0, 0, 0])).all()
    n_dist = np.linalg.norm(vec)
    m_dist = np.linalg.norm(m_vec)
    if (on_line and n_dist <= m_dist):
        status = 1
        node_list.append(n_node)
        new_nodes = np.delete(nodes, ndx[0])
        get_next_node(mid_point, new_nodes, node_list, l_vec, dist, n_node, status)

    elif(not on_line):
        new_nodes = np.delete(nodes, ndx[0])
        get_next_node(mid_point, new_nodes, node_list, l_vec, dist, p_node, status)

    #print("")
    #print(node_list)
    return node_list

#https://stackoverflow.com/questions/2486093/millions-of-3d-points-how-to-find-the-10-of-them-closest-to-a-given-point
def get_line(nodes, start_node, mid_point):
    node_list = []
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
    #print(node_list)
    new_nodes = np.delete(nodes, ndx[0])
    node_list = (get_next_node(mid_point, new_nodes, node_list, vec, dist, n_node, 0))
    # print(node_list)
    # print("")
    #get_next_node(new_nodes, node_list, vec, dist, n_node, 0)
    line.nodes = node_list
    return line

def beams(nodes, boundary_nodes, mid_point):
    lines = []
    beams = []
    for node in boundary_nodes:
        lines.append(get_line(nodes, node.xyz, mid_point))
    lines = group_lines(lines)

    # for line in lines:
    #   print(line.idx)

    for num in range(0, len(lines)):
        if lines[num].idx != -1:
            beam = Beam(lines[num].idx, [])
            beam.nodes.extend(lines[num].nodes)
            for num2 in range(0, len(lines)):
                # print(lines[num].idx, lines[num2].idx)
                if num != num2 and lines[num].idx == lines[num2].idx:
                    # print("reached")
                    #add nodes
                    lines[num2].idx = -1
                    beam.nodes.extend(lines[num2].nodes)
                    print(lines[num2].nodes)
            lines[num].idx = -1
            # print("")
            beams.append(beam)

    for beam in beams:
      # print beam.idx
      print len(beam.nodes)
    return beams







