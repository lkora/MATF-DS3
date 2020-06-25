from collections import defaultdict 
import os.path
from os import path
import numpy as np
from collections import defaultdict 

# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")

def input_problem():
    print("---- NOTE ----\nThe file must be in the following format:\nsource sink\nN0 N1\nN1 N3\nN0 N3\n....\n....")
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

    # Read if the graph is directed or undirected
    line = next(f).split()
    source = int(line[0])
    sink = int(line[1])
    # Read the graph
    
    graph = [[int(x) for x in line.split()] for line in f]    
    f.close() # File not needed, all is in tmp_array

    
    return source, sink, graph


#This class represents a directed graph using adjacency matrix representation
class Graph:
	def __init__(self,graph):
		self.graph = graph # residual graph
		self.size = len(graph)		

	# Returns true if there is a path from source 'source' to sink 'sink' in
	# residual graph. Also fills parent[] to store the path
	def BFS(self, source, sink, parent):
		# Mark all the vertices as not visited
		visited = [False] * (self.size)
		# Create a queue for BFS
		queue = []
		# Mark the source node as visited and enqueue it
		queue.append(source)
		visited[source] = True

		while queue:
			u = queue.pop(0)
			# Get all adjacent vertices of the dequeued vertex u
			# If a adjacent has not been visited, then mark it
			# visited and enqueue it
			for ind, val in enumerate(self.graph[u]):
				if visited[ind] == False and val > 0 :
					queue.append(ind)
					visited[ind] = True
					parent[ind] = u

		# If there is a path from source to sink return true, else false
		return True if visited[sink] else False
			
	
	# Returns tne maximum flow from source to sink in the given graph
	def FordFulkerson(self, source, sink):
		# This array is filled by BFS and to store path
		parent = [-1] * (self.size)

		max_flow = 0 # There is no flow initially

		# Augment the flow while there is path from source to sink
		while self.BFS(source, sink, parent):
			# Finding minimum residual capacity of the edges along the path filled by BFS. 
			path_flow = float("Inf")
			s = sink
			while(s != source):
				path_flow = min (path_flow, self.graph[parent[s]][s])
				s = parent[s]
			# Add path flow to overall flow
			max_flow += path_flow
			# Update residual capacities of the edges and reverse edges along the path
			v = sink
			while(v != source):
				u = parent[v]
				self.graph[u][v] -= path_flow
				self.graph[v][u] += path_flow
				v = parent[v]

		return max_flow


def main():
	source, sink, graph = input_problem()
	g = Graph(graph) 
	
	print("The maximum possible flow is %d " % g.FordFulkerson(source, sink)) 


if __name__ == '__main__':
   main()