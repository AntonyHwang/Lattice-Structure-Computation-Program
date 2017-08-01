import numpy as np
import math
import pprint
from app import Line

#group lines by comapring dv
def group_lines(lines):
    idx_num = 0
    for num1 in range (0, len(lines)):
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

def check_exist(n, list):
    for node in list:
        if n == node:
            return True
    return False

#https://stackoverflow.com/questions/2486093/millions-of-3d-points-how-to-find-the-10-of-them-closest-to-a-given-point
def get_line(line, nodes, boundary_nodes, start_node, p_idx, p_vec):
    line.append(start_node)
    point = start_node
    new_nodes = np.delete(nodes, p_idx)
    d = ((nodes-point)**2).sum(axis=1)
    ndx = d.argsort()
    #find nearest neighbour
    for num in range(1, 3):
        if not check_exist(nodes[ndx[num]], boundary_nodes):
            vec = nodes[ndx[num]] - point
            if vec == p_vec or p_idx == -1:
                line.dv = vec
                get_line(line, new_nodes, boundary_nodes, nodes[ndx[num]], ndx[num], vec)
            else:
                return line

#https://stackoverflow.com/questions/2486093/millions-of-3d-points-how-to-find-the-10-of-them-closest-to-a-given-point
def lines(nodes, boundary_nodes):
    lines = np.array([])
    for node in boundary_nodes:
        line = Line(np.array([0,0,0]), np.array([]))
        line = get_line(line, nodes, boundary_nodes, node, -1, 0)
        np.append(lines, line)
    lines = group_lines(lines)
    return lines

if __name__ == "__main__":
    get_line()
