from collections import defaultdict 
import os.path
from os import path

# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")


def input_graph():
    print("---- NOTE ----\nThe file must be in the following format:\nX u/d\t\t\tWhere p - Undirected graph or d - Directed graph, X - Starting node\nN0 N1\nN1 N3\nN0 N3\n....\n.... Where the direction is: \nfirst -> second (N0 -> N1 for directed)")
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
    no_nodes = int(option[0])
    option = str(option[1])
    directed = False
    if option != 'u' and option != 'd':
        print("Graph direction is invalid! Assuming directed graph")
        directed = True
    if option == 'd':
        directed = True   

    # Read the edges
    edges = [[int(x) for x in line.split()] for line in f]    
    f.close() # File not needed, all is in tmp_array
    
    return edges, directed, no_nodes


   
#This class represents an undirected graph using adjacency list representation 
class Graph: 
   
    def __init__(self, no_nodes): 
        self.no_nodes = no_nodes #No. of vertices 
        self.graph = defaultdict(list) # default dictionary to store graph 

    # Function to add an edge to graph 
    def add_edge(self, p, c): 
        self.graph[p].append(c) 

    # This function removes edge p-c from graph     
    def rmvEdge(self, p, c): 
        for index, key in enumerate(self.graph[p]): 
            if key == c: 
                self.graph[p].pop(index) 
        for index, key in enumerate(self.graph[c]): 
            if key == p: 
                self.graph[c].pop(index) 

    # A DFS based function to count reachable nodes from "node"
    def DFSCount(self, node, visited): 
        count = 1
        visited[node] = True
        for i in self.graph[node]: 
            if visited[i] == False: 
                count = count + self.DFSCount(i, visited)          
        return count 

    # A helper function used by isConnected 
    def DFSUtil(self, node, visited): 
        # Mark the current node as visited  
        visited[node] = True

        #Recur for all the vertices adjacent to this vertex 
        for i in self.graph[node]: 
            if visited[i] == False: 
                self.DFSUtil(i, visited) 


    # Method to check if all non-zero degree vertices are 
    # connected
    def isConnected(self): 

        # Mark all the vertices as not visited 
        visited = [False] * (self.no_nodes) 

        # Find a vertex with non-zero degree 
        for i in range(self.no_nodes): 
            if len(self.graph[i]) > 1: 
                break

        # If there are no edges in the graph, return true 
        if i == self.no_nodes - 1: 
            return True

        # Start DFS traversal from a vertex with non-zero degree 
        self.DFSUtil(i, visited) 

        # Check if all non-zero degree vertices are visited 
        for i in range(self.no_nodes): 
            if visited[i]==False and len(self.graph[i]) > 0: 
                return False
            
        return True


    # The function returns one of the following values 
    # 0 --> If grpah is not Eulerian 
    # 1 --> If graph has an Euler path (Semi-Eulerian) 
    # 2 --> If graph has an Euler Circuit (Eulerian)
    def isEulerian(self): 
        # Check if all non-zero degree vertices are connected 
        if self.isConnected() == False: 
            return 0
        else: 
            # Count vertices with odd degree 
            odd = 0
            for i in range(self.no_nodes): 
                if len(self.graph[i]) % 2 != 0: 
                    odd += 1

            # If odd count is 2, then semi-eulerian. 
            # If odd count is 0, then eulerian 
            # If count is more than 2, then graph is not Eulerian 
            # Note that odd count can never be 1 for undirected graph
            if odd == 0: 
                return 2
            elif odd == 2: 
                return 1
            elif odd > 2: 
                return 0


    # Function to run test cases 
    def test(self): 
        res = self.isEulerian() 
        if res == 0: 
            print ("Graph is not Eulerian", end = " ")
        elif res == 1 : 
            print ("Graph has Euler path", end = " ")
        else: 
            print ("Graph has Euler cycle", end = " ")


    # The function to check if edge p-c can be considered as next edge in 
    def isValidNextEdge(self, p, c): 
        # The edge p-c is valid in one of the following two cases: 
        
            # 1) If c is the only adjacent vertex of p 
        if len(self.graph[p]) == 1: 
            return True
        else: 
            # 2) If there are multiple adjacents, then p-c is not a bridge 
            #      Do following steps to check if p-c is a bridge 

            # 2.a) count of vertices reachable from p  
            visited =[False]*(self.no_nodes) 
            count1 = self.DFSCount(p, visited) 

            # 2.b) Remove edge (p, c) and after removing the edge, count 
            #      vertices reachable from p
            self.rmvEdge(p, c) 
            visited = [False] * (self.no_nodes) 
            count2 = self.DFSCount(p, visited) 

            # 2.c) Add the edge back to the graph 
            self.add_edge(p, c) 

            # 2.d) If count1 is greater, then edge (p, c) is a bridge 
            return False if count1 > count2 else True


    # Print Euler tour starting from vertex p 
    def printEulerUtil(self, p): 
        # Recur for all the vertices adjacent to this vertex 
        for c in self.graph[p]: 
            # If edge p-c is not removed and it's a a valid next edge 
            if self.isValidNextEdge(p, c): 
                print(str(p) + "-" + str(c), end=" "), 
                self.rmvEdge(p, c) 
                self.printEulerUtil(c) 


        
    # The main function that print Eulerian Trail. It first finds an odd 
    # degree vertex (if there is any) and then calls printEulerUtil() 
    # to print the path '''
    def printEulerTour(self): 
        # Find a vertex with odd degree 
        p = 0
        for i in range(self.no_nodes): 
            if len(self.graph[i]) %2 != 0 : 
                p = i 
                break
        # Print tour starting from odd vertex 
        print ("\n") 
        self.printEulerUtil(p) 


def main():
    edges, direction, no_nodes = input_graph()
    g = Graph(no_nodes)
    # Create graph, diracted/undirected
    if direction == True:
        for i in range(len(edges)):
            g.add_edge(edges[i][0], edges[i][1])
    else:
        for i in range(len(edges)):
            g.add_edge(edges[i][0], edges[i][1])
            g.add_edge(edges[i][1], edges[i][0])

    if direction == True:
        print("Directed graph.")
    else:
        print("Undirected graph.")

    print_split()
    g.test()
    g.printEulerTour() 
    print_split()

if __name__ == '__main__':
   main()