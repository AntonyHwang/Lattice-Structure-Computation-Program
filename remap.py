import app
import sys

# alters elements to have the correct beam_id
def remap(elements, nodes, id):
	for e in elements:
		if e.nodes[0] in nodes and e.nodes[1] in nodes and e.nodes[2] in nodes:
			e.set_beam(id)

if __name__ == "__main__":
	pass