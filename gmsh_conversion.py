import os

def stl_to_msh(stl_name, output_name):
	# Calls gmsh to convert a .stl file to a .msh file
	#
	# Args:
	# 		stl_name: name of the .stl file minus '.stl' extension
	#       output_name: name of the .msh output file minus '.msh' extension
	os.system('scripts\\to_msh.bat ' + stl_name + ' ' + output_name)

def msh_to_stl(msh_name, output_name):
	# Calls gmsh to convert a .msh file to a .stl file
	#
	# Args:
	# 		msh_name: name of the .msh file minus '.msh' extension
	#       output_name: name of the .stl output file minus '.stl' extension
	os.system('scripts\\to_stl.bat ' + msh_name + ' ' + output_name)

if __name__ == "__main__":
	pass