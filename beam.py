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
                  if (np.array_equal(norm(lines[num1].dv),norm(lines[num2].dv))):
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

    for num in range(0, len(lines)):
        if lines[num].idx != -1:
            beam = Beam(lines[num].idx, [])
            #print(type(lines[num].nodes[0]))
            beam.nodes.extend(lines[num].nodes)
            for num2 in range(0, len(lines)):
                # print(lines[num].idx, lines[num2].idx)
                if num != num2 and lines[num].idx == lines[num2].idx:
                    # print("reached")
                    #add nodes
                    lines[num2].idx = -1
                    beam.nodes.extend(lines[num2].nodes)
                    # print(lines[num2].nodes)
            lines[num].idx = -1
           #print(beam.idx)
            beams.append(beam)

    return beams


def beams_by_octant(nodes, mid_point):
  truth_values = [True, False]
  idx = 0
  beams = []
  count = 0

  # print(str(mid_point[0]) +'\t' + str(mid_point[1]) + '\t' + str(mid_point[2]))

  for x in truth_values:
    for y in truth_values:
      for z in truth_values:
        beams.append(Beam(count, get_nodes_octant(x, y, z, nodes, mid_point)))
        count += 1

  # print("midpoint: "+ np.array_str(mid_point))
  # for b in beams:
  #   print('\n\n' + str(b.idx) + '\t' + str(len(b.nodes)))
  #   for n in b.nodes:
  #     print(n.toString())

  return beams


def get_nodes_octant(x_pos, y_pos, z_pos, nodes, mid_point):
  
  ret = []
  BUFFER = 0.05

  if x_pos and y_pos and z_pos: # (+, +, +)
    for n in nodes:
      if n.xyz[0] >= mid_point[0] - BUFFER and n.xyz[1] >= mid_point[1] - BUFFER and n.xyz[2] >= mid_point[2] - BUFFER:
        ret.append(n)
    return ret

  elif x_pos and y_pos and not z_pos: # (+, +, -)
    for n in nodes:
      if n.xyz[0] >= mid_point[0] - BUFFER and n.xyz[1] >= mid_point[1] - BUFFER and n.xyz[2] <= mid_point[2] + BUFFER:
        ret.append(n)
    return ret

  elif x_pos and not y_pos and not z_pos: # (+, -, -)
    for n in nodes:
      if n.xyz[0] >= mid_point[0] - BUFFER and n.xyz[1] <= mid_point[1] + BUFFER and n.xyz[2] <= mid_point[2] + BUFFER:
        ret.append(n)
    return ret

  elif x_pos and not y_pos and z_pos: # (+, -, +)
    for n in nodes:
      if n.xyz[0] >= mid_point[0] - BUFFER and n.xyz[1] <= mid_point[1] + BUFFER and n.xyz[2] >= mid_point[2] - BUFFER:
        ret.append(n)
    return ret

  elif not x_pos and y_pos and z_pos: # (-, +, +)
    for n in nodes:
      if n.xyz[0] <= mid_point[0] + BUFFER and n.xyz[1] >= mid_point[1] - BUFFER and n.xyz[2] >= mid_point[2] - BUFFER:
        ret.append(n)
    return ret

  elif not x_pos and not y_pos and z_pos: # (-, -, +)
    for n in nodes:
      if n.xyz[0] <= mid_point[0] + BUFFER and n.xyz[1] <= mid_point[1] + BUFFER and n.xyz[2] >= mid_point[2] - BUFFER:
        ret.append(n)
    return ret

  elif not x_pos and y_pos and not z_pos: # (-, +, -)
    for n in nodes:
      if n.xyz[0] <= mid_point[0] + BUFFER and n.xyz[1] >= mid_point[1] - BUFFER and n.xyz[2] <= mid_point[2] + BUFFER:
        ret.append(n)
    return ret

  else: # (-, -, -)
    for n in nodes:
      if n.xyz[0] <= mid_point[0] + BUFFER and n.xyz[1] <= mid_point[1] + BUFFER and n.xyz[2] <= mid_point[2] + BUFFER:
        ret.append(n)
    return ret

