import os

def stl_to_msh(stl_name, output_name):
	os.system('scripts\\to_msh.bat ' + stl_name + ' ' + output_name)

def msh_to_stl(msh_name, output_name):
	os.system('scripts\\to_stl.bat ' + msh_name + ' ' + output_name)

if __name__ == "__main__":
	pass