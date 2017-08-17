import numpy as np
import math
import pprint
from app import Line, Node, Beam

def norm(vec):
    #Args:
    #   vec: direction vector
    #Calculates unit vector
    magnitude = np.linalg.norm(vec)
    if magnitude != 0:
      n_vec = vec / magnitude
      return n_vec
    else:
      return vec

def unit(vec):
    #Args:
    #   vec: direction vector
    #Calculates unit vector
    magnitude = np.linalg.norm(vec)
    if magnitude != 0:
        n_vec = vec / magnitude
        return n_vec
    else:
        return vec

def check_within(vec, l_vec):
    #Args:
    #   vec, l_vec: 2 direction vectors to be compared
    #Check angle of line formed within acceptable range
    angle = np.arccos(np.clip(np.dot(vec, l_vec), -1.0, 1.0))
    # if angle > (math.pi * 3.0 / 4.0) and angle < (math.pi * 5.0 / 4.0):
    if angle < (math.pi / 6.0):
        # print("true")
        return True
    else:
        # print("false")
        return False

def group_lines(lines):
    #Args:
    #   lines: list of line objects
    #Group lines with similiar direction vectors
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
    #Args:
    #   n, l: node and a list of nodes
    #Check if node exist in the list
    for node in l:
        if (n.xyz[0] == node.xyz[0] and n.xyz[1] == node.xyz[1] and n.xyz[2] == node.xyz[2]):
            return True
    return False

def get_next_node(mid_point, nodes, node_list, l_vec, p_node):
    #Args:
    #   mid_point, nodes, node_list, l_vec, p_node: mid point of the unit mesh, all nodes, new node list, direction vector of the line, previous node
    #Uses recursion to identify lines along the beams and nodes belongs to the line
    d = [((n.xyz - p_node) ** 2).sum() for n in nodes]
    ndx = np.argsort(d)
    n_node = nodes[ndx[0]].xyz
    vec = n_node - p_node
    m_vec = mid_point - p_node
    n_dist = np.linalg.norm(vec)
    m_dist = np.linalg.norm(m_vec)
    on_line = (unit(vec) == l_vec).all()
    if (check_within(unit(vec), l_vec) and n_dist <= m_dist):
        node_list.append(n_node)
        new_nodes = np.delete(nodes, ndx[0])
        get_next_node(mid_point, new_nodes, node_list, l_vec, n_node)

    elif(not on_line and n_dist <= m_dist):
        new_nodes = np.delete(nodes, ndx[0])
        get_next_node(mid_point, new_nodes, node_list, l_vec, p_node)

    return node_list

#https://stackoverflow.com/questions/2486093/millions-of-3d-points-how-to-find-the-10-of-them-closest-to-a-given-point
def get_beam_nodes(nodes, beam, mid_point):
    #Args:
    #   nodes, beam, mid_point: list of nodes, beam object, mid point of the unit mesh   
    #Starting from the boundary nodes, find the nearest none boundary node to calculate the line along the beam
    node_list = []
    line = Line(-1, np.array([]), [])
    for start_node in beam.b_nodes:
        node_list.append(start_node)
        d = [((n.xyz - start_node.xyz)**2).sum() for n in nodes]
        ndx = np.argsort(d)
        n_node = nodes[ndx[0]].xyz
        vec = n_node - start_node.xyz
        dv = unit(vec)
        node_list.append(n_node)
        new_nodes = np.delete(nodes, ndx[0])
        node_list = get_next_node(mid_point, new_nodes, node_list, dv, n_node)
    beam.nodes.extend(node_list)
    return beam

def get_beam_boundary(beam, boundary_nodes, idx, node_visited):
    #Args:
    #   beam, boundary_nodes, idx, node_visited: beam object, list of boundary nodes, index of node, array to record whether node is checked
    #Group boundary nodes into beams
    d = [((n.xyz - boundary_nodes[idx].xyz) ** 2).sum() for n in boundary_nodes]
    ndx = np.argsort(d)
    beam.b_nodes.append(boundary_nodes[idx])
    node_visited[idx] = 1
    if node_visited[ndx[1]] == 0:
        beam, boundary_nodes, node_visited = get_beam_boundary(beam, boundary_nodes, ndx[1], node_visited)
    if node_visited[ndx[2]] == 0:
        beam, boundary_nodes, node_visited = get_beam_boundary(beam, boundary_nodes, ndx[2], node_visited)
    if node_visited[ndx[3]] == 0:
        beam, boundary_nodes, node_visited = get_beam_boundary(beam, boundary_nodes, ndx[3], node_visited)
    if node_visited[ndx[4]] == 0:
        beam, boundary_nodes, node_visited = get_beam_boundary(beam, boundary_nodes, ndx[4], node_visited)

    return beam, boundary_nodes, node_visited

def beams(nodes, boundary_nodes, mid_point):
     #Args:
    #   nodes, boundary_nodes, mid_point: list of all the nodes, list of boundary nodes, mid point of the unit mesh
    #Identify beams
    print("boundary: " + str(len(boundary_nodes)))
    beams = []
    beam_idx = 0
    node_visited = [0] * len(boundary_nodes)
    for idx in range (0, len(boundary_nodes)):
        # print(node_visited[idx])
        if node_visited[idx] == 0:
            beam_idx += 1
            beam = Beam(beam_idx, [], [])
            beam, boundary_nodes, node_visited = get_beam_boundary(beam, boundary_nodes, idx, node_visited)
            beam = get_beam_nodes(nodes, beam, mid_point)
            beams.append(beam)

    for beam in beams:
        print("Beam ID: " + str(beam.idx))
        print(len(beam.b_nodes))

    # for beam in beams:
    #     beam = get_beam_nodes(nodes, beam, mid_point)
    print("Number of beams: " + str(len(beams)))
    print(len(beams))

    return beams

def beams_by_octant(nodes, mid_point):
  # Gets a list of Beam objects separated by octant

  # Args:
  #   nodes: A list of Node objects to separate into beams
  #   mid_point: A numpy array represetning the coordinate that is the midpoint of the shape

  # Returns:
  #   A list of Beam objects that have been defined by which octant they belong to.

  truth_values = [True, False]
  idx = 0
  beams = []
  count = 0

  # print(str(mid_point[0]) +'\t' + str(mid_point[1]) + '\t' + str(mid_point[2]))

  for x in truth_values:
    for y in truth_values:
      for z in truth_values:
        beams.append(Beam(count, [], get_nodes_octant(x, y, z, nodes, mid_point)))
        count += 1

  # print("midpoint: "+ np.array_str(mid_point))
  # for b in beams:
  #   print('\n\n' + str(b.idx) + '\t' + str(len(b.nodes)))
  #   for n in b.nodes:
  #     print(n.toString())

  return beams


def get_nodes_octant(x_pos, y_pos, z_pos, nodes, mid_point):
  # Gets all the nodes that lie in a specific ocatant (in 3d)

  # Takes whether or not x,y,z are positive and finds all the nodes in that octant
  # comapred to the mid_point

  # Args:
  #   x_pos, y_pos, z_pos: Booleans representing whether x,y,z are positive 
  #                        (or which octant the points should belong to)
  #   nodes: A list of all Node objects
  #   mid_point: A numpy array representing the middle coordinate of the shape.
  # Returns:
  #   A list of all the nodes that lie in the octant specified

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

