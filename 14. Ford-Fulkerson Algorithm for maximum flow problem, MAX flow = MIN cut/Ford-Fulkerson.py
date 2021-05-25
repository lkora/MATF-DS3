import os.path
import networkx as nx
import matplotlib.pyplot as plt
from os import path
from networkx.algorithms import flow
from networkx.algorithms.flow import shortest_augmenting_path

from numpy.lib.utils import source

# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")


def input_graph():
	print("---- NOTE ----\nThe file must be in the following format:\nX\t\t\tX - Number of nodes\nsource sink\nN0 N1\nN1 N3\nN0 N3\n....\n....")
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
	source = next(f).split()
	sink = (source[1])
	source = (source[0])

	# Read the graph
	graph = [[(x) for x in line.split()] for line in f]
	for i in graph:
		i[2] = int(i[2])
		i = tuple(i)
	f.close() # File not needed, all is in tmp_array


	return graph, no_nodes, source, sink

class Graph:
	def __init__(self, nodes): 
		self.graph = []
		self.nodes = nodes
		self.total = 0
		
	def add_edge(self, p, c, weight):
		self.graph.append([p, c, weight])
    
	# BFS iterative implementation using queue
	def find(self, parent, i): 
		if parent[i] == i: 
			return i 
		return self.find(parent, parent[i]) 
  
    # A function that does union of two sets of x and y 
	def union(self, parent, rank, x, y): 
		xroot = self.find(parent, x) 
		yroot = self.find(parent, y) 
  
        # Attach smaller rank tree under root of  
        # high rank tree (Union by Rank) 
		if rank[xroot] < rank[yroot]: 
			parent[xroot] = yroot 
		elif rank[xroot] > rank[yroot]: 
			parent[yroot] = xroot 
  
        # If ranks are the same, then make it a root  
        # and increment the rank by one 
		else: 
			parent[yroot] = xroot 
			rank[xroot] += 1


def main():
	graph, no_nodes, source, sink = input_graph()

	G = nx.DiGraph()
	for i in graph:
		G.add_edge(i[0], i[1], capacity=i[2])

	# Plotting
	plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.05, hspace=0)
	plt.tight_layout()
	options = {
		'node_color': 'cyan',
		'node_size': 150,
		'width': 2,
		'arrowstyle': '-|>',
		'arrowsize': 12,
		#"connectionstyle":'arc3, rad = 0.1'
	}

	# plt.subplot(1, 2, 1)
	pos = nx.spring_layout(G)
	nx.draw_networkx(G, pos, arrows=True, **options)
	labels = nx.get_edge_attributes(G, 'capacity')
	nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
	plt.plot()

	

	flow_value, F = nx.maximum_flow(G, source, sink, flow_func=shortest_augmenting_path)
	print(flow_value)
	# F = nx.DiGraph(F)
	# plt.subplot(1, 2, 2)
	# nx.draw_networkx(F, pos, arrows=True, **options)
	# labels = nx.get_edge_attributes(F, 'capacity')
	# nx.draw_networkx_edge_labels(F, pos, edge_labels=labels)
	# plt.plot()
	
	plt.show()




	

if __name__ == '__main__':
    main()