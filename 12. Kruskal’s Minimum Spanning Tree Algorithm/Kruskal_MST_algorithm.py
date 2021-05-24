import os.path
from os import path

# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")


def input_graph():
    print("---- NOTE ----\nThe file must be in the following format:\nX\t\t\tX - Number of nodes\nN0 N1\nN1 N3\nN0 N3\n....\n....")
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
    no_nodes = next(f).split()
    no_nodes = int(no_nodes[0])

    # Read the graph
    graph = [[int(x) for x in line.split()] for line in f]    
    f.close() # File not needed, all is in tmp_array

    
    return graph, no_nodes

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
  
    # The main function to construct MST using Kruskal's algorithm 
	def kruskal(self): 
		result = [] 
		i = 0 # Sorted graph index
		e = 0 # result[] index

		# Step 1: Sort the graph weights in non-decreasing order.   
		self.graph = sorted(self.graph, key = lambda item:item[2]) 

		parent = []
		rank = [] 

        # Create node subsets with single elements 
		for node in range(self.nodes): 
			parent.append(node) 
			rank.append(0) 

        # Number of graph to be taken is equal to V-1 
		while e < self.nodes -1 : 

            # Step 2: Pick the smallest edge and increment the index for next iteration 
			p, c, weight =  self.graph[i] 
			i = i + 1
			x = self.find(parent, p) 
			y = self.find(parent, c) 

            # If inclusion of this edge doesn't create the cycle, include it in the result
            # and increment the index of result for next edge 
			if x != y: 
				e = e + 1     
				result.append([p, c, weight]) 
				self.union(parent, rank, x, y)
				self.total = self.total + weight
				

            # Else discard the edge 

		print ("Minimal spanning tree from the graph: ")
		for p, c, weight in result: 
			print (str(p) + " -- " + str(c) + ", weight(" + str(weight) + ")")

def main():
	graph, no_nodes = input_graph()
	g = Graph(no_nodes)
	for i in range(len(graph)):
            g.add_edge(graph[i][0], graph[i][1], graph[i][2])
	g.kruskal() 
	print("Weight: ", g.total)
	print_split()


if __name__ == '__main__':
   main()