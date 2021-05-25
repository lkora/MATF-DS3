import os.path
from ._print import print_split

def input_graph():
	print("---- NOTE ----\nThe file must be in the following format:\nX\t\t\tX - Number of nodes\nN0 N1 W0\nN1 N3 W1\nN0 N3 W2\n....\n where Np --- > Nk (branch) and W (weight)")
	print_split()
	file_name = input("Enter the file name: ")
	# Creating absolute path to the file in folder examples
	file_dir = os.path.dirname(__file__)
	rel_path = "examples/" + file_name
	abs_file_path = os.path.join(file_dir, rel_path)
	# Checking if the file exists
	if os.path.exists(abs_file_path) == False:
		# File not found, throw error
		print("The file doesn't exist!")
		raise Exception("The file didn't load because it doesn't exist")
	# File found, opening
	f = open(abs_file_path, 'r')

	no_nodes = next(f).split()
	no_nodes = int(no_nodes[0])

	# Read the graph
	graph = [[(x) for x in line.split()] for line in f]
	for i in graph:
		i[2] = int(i[2])
		i = tuple(i)
	f.close() # File not needed, all is in tmp_array


	return graph, no_nodes
