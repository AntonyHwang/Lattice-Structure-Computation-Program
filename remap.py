import app
import sys
import os

# alters elements to have the correct beam_id
def align_line_and_element(elements, nodes, id):
	for e in elements:
		if e.nodes[0] in nodes and e.nodes[1] in nodes and e.nodes[2] in nodes:
			e.set_beam(id)

# rewrite the properties on a mesh, lattice
def write_properties_on_mesh(mesh_file, elements, total_nodes, x = 1, y = 1, z = 1):
	total_elements = (x*y*z) * len(elements)
	start_point = ((x*y*z) * total_nodes) + 8
	count = 0
	element_idx = 1

	with open(mesh_file + '.msh', 'r') as mesh, open(mesh_file + '1.msh', 'w') as output:
		for i, line in enumerate(mesh):
			if i >= start_point:
				output.write(line.replace('2 2 0 1', elements[count].attributes_string()))
				count += 1
				if count > len(elements):
					count = 0
			else:
				output.write(line)

	os.remove(mesh_file + '.msh')
	os.rename(mesh_file + '1.msh', mesh_file + '.msh')

if __name__ == "__main__":
	pass