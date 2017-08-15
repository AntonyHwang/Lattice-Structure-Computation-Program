import app
import time
import os


def unitTest(nodes, elements, displacement_factor):
# Runs general unit tests on app.py

# Runs general unit tests incrementing the x, y, z levels each time. Writes the
# output to output\test_output.txt

# Args:
# 	nodes: A list of nodes
# 	elements: A list of elements
# 	displacement_factor: A Node with the displacement factors

	output = open("output\\test_output.txt", "w")
	count = 0
	for i in range(0,10):
		for j in range(0, 10):
			for k in range(0, 10):
				print("running test #" + str(count) + "...")
				count += 1
				start_time = time.time()
				app.generate_lattice(nodes, elements, nodes[len(nodes) - 1].idx, displacement_factor, i, j, k)
				output.write("test: " + str(count) + "\t(" + str(i) +"x" + str(j) + "x" + str(k) + ")\t" + str(time.time() - start_time) + " seconds\t" + str(os.path.getsize(".\\output\\lattice.msh")) + " bytes" +'\n')
	output.close()


def individual_test(nodes, elements, displacement_factor, x, y, z, num_of_tests):
# Runs individual tests on app.py

# Runs a test for a certain lattice structure size. Runs it a set number of times.
# Writes the output to output\test_output.txt

# Args:
# 	nodes: A list of nodes
# 	elements: A list of elements
# 	displacement_factor: A Node with the displacement factors
# 	x: The 'X' dimension of the lattice
# 	y: The 'Y' dimension of the lattice
# 	z: The 'Z' dimension of the lattice
# 	num_of_tests: The number of times to repeat the test

	output = open("output\\test_output.txt", "w")
	count = 0
	total_time = 0
	total_bytes = 0
	for i in range(0,num_of_tests):
		print("running test# " + str(i) + "...")
		start_time = time.time()
		app.generate_lattice(nodes, elements, nodes[len(nodes) - 1].idx, displacement_factor, x, y, z)
		temp_time = time.time() - start_time
		total_time += temp_time
		total_bytes += os.path.getsize(".\\output\\lattice.msh")
		output.write("test: " + str(i) + "\t\t(" + str(x) +"x" + str(y) + "x" + str(z) + ")\t" + str(temp_time) + " seconds\t" + str(os.path.getsize(".\\output\\lattice.msh")) + " bytes" + '\n')
	output.write("\n\n\taverage time: " + str(total_time/num_of_tests) + "\taverage size: " + str(total_bytes/num_of_tests))
	print("average time: " + str(total_time/num_of_tests) + "\t average file size (in bytes): " + str(total_bytes/num_of_tests))
	output.close()


def main():
	nodes = app.read_nodes([])
	elements = app.read_elements([])
	displacement_factor = app.direction_delta(nodes)
	# unitTest(nodes, elements, displacement_factor)
	individual_test(nodes, elements, displacement_factor, 0, 0, 0, 10)


if __name__ == "__main__":
	main()