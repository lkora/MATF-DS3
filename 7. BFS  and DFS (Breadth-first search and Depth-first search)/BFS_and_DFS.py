from collections import defaultdict 
import os.path
from os import path

# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")


def input_graph():
    print("---- NOTE ----\nThe file must be in the following format:\nu/d X\t\t\tWhere u - Undirected graph or d - Directed graph, X - Starting node\nN0 N1\nN1 N3\nN0 N3\n....\n.... Where the direction is: \nfirst -> second (N0 -> N1 for directed)")
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
    option = next(f).split()
    start = int(option[1])
    option = str(option[0])
    directed = False
    if option != 'u' and option != 'd':
        print("Graph direction is invalid! Assuming directed graph")
        directed = True
    if option == 'd':
        directed = True   

    # Read the edges
    edges = [[int(x) for x in line.split()] for line in f]    
    f.close() # File not needed, all is in tmp_array

    
    return edges, directed, start

class Graph:    
    def __init__(self): 
        self.graph = defaultdict(list) 
  
    # Method to add an edge to graph
    def add_edge(self, p, c): 
        self.graph[p].append(c) 
  
    # BFS iterative implementation using queue
    def BFS(self, current): 
        # Mark all the vertices as not visited 
        visited = len(self.graph) * [False]
  
        # Create a queue for BFS 
        queue = [] 
  
        # Marking the beginning node as visited and putting it in the queue 
        queue.append(current) 
        visited[current] = True
  
        while queue: 
            # Visit a node and dequeue it
            current = queue.pop(0) 
            print(current, end = " ") 

            # Get all adjacent nodes of the dequeued current node. 
            # If an adjacent node has not been visited, mark it visited and enqueue it 
            for node in self.graph[current]: 
                if visited[node] == False: 
                    queue.append(node) 
                    visited[node] = True


    # DFS iterative implementation using stack
    def DFS(self, current):                   
        # Mark all the nodes as not visited 
        visited = len(self.graph) * [False] 
  
        # Create a stack for DFS  
        stack = [] 
  
        # Push the current node.  
        stack.append(current)  
  
        while(len(stack)):  
            # Pop a node from stack and print it  
            current = stack[-1]  
            stack.pop() 
  
            # Stack may contain the same node twice, so we need to print the popped item only if it is not visited.  
            if not visited[current]:  
                print(current, end = " ") 
                visited[current] = True 
  
            # Get all adjacent nodes of the popped current node. 
            # If an adjacent node has not been visited, then push it to the stack.  
            for node in self.graph[current]:  
                if not visited[node]:  
                    stack.append(node)  
  

def main():
    g = Graph()
    edges, direction, start = input_graph()
    # Create graph, diracted/undirected
    if direction == True:
        for i in range(len(edges)):
            g.add_edge(edges[i][0], edges[i][1])
    else:
        for i in range(len(edges)):
            g.add_edge(edges[i][0], edges[i][1])
            g.add_edge(edges[i][1], edges[i][0])
    
    print("Starting from the node: ", start)
    if direction == True:
        print("Directed graph.")
    else:
        print("Undirected graph.")
    print("BFS:", end = " ") 
    g.BFS(start)
    print()
    print("DFS:", end = " ")
    g.DFS(start)
    print_split()


if __name__ == '__main__':
   main()