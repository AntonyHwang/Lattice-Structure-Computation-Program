import app
import sys
import os
import time

# alters elements to have the correct beam_id
def align_line_and_element(elements, nodes, id):
	for e in elements:
		if e.nodes[0] in nodes and e.nodes[1] in nodes and e.nodes[2] in nodes:
			e.set_beam(id)

# rewrite the properties on a mesh, lattice
def write_properties_on_mesh(mesh_file, elements, total_nodes, num_of_beams, x = 1, y = 1, z = 1):
	print("Info\t: Started on " + time.strftime("%c"))
	
	total_elements = (x*y*z) * len(elements)
	reading_elements = False
	count = 0
	beam_id_variable = 0
	Node = False

	with open(mesh_file + '.msh', 'r') as mesh, open(mesh_file + '1.msh', 'w') as output:
		print("Info\t: Writing Nodes...")
		for i, line in enumerate(mesh):
			if Node:
				print("Info\t: " + line.strip() + " nodes in mesh")
				Node = False
			if "$Nodes" in line:
				Node = True
			if "$Elements" in line:
				print("Info\t: Done Writing Nodes")
				print("Info\t: Writing Elements...")
				print("Info\t: " + str(total_elements) + " elements in mesh")
				reading_elements = True
			if reading_elements:
				if "$EndElements" in line:
					reading_elements = False
				# print(line + '\t' +  str(count))
				if '2 2 0 1' in line:
					output.write(line.replace('2 2 0 1', str(elements[count].attributes[0]) + ' '  + str(elements[count].attributes[1]) + ' ' + str(elements[count].attributes[2]) + ' ' + str(elements[count].attributes[3] + beam_id_variable)))
					count += 1
					if count >= len(elements):
						beam_id_variable += num_of_beams
						count = 0
				else:
					output.write(line)
			else:
				output.write(line)
		print("Info\t: Done Writing Elements")

	os.remove(mesh_file + '.msh')
	os.rename(mesh_file + '1.msh', mesh_file + '.msh')
	print("Info\t: Finished on " + time.strftime("%c"))

if __name__ == "__main__":
	pass