import queue
import os.path
from os import path
import numpy as np

# Item is defined with weight and value
class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

# Node in the tree
# level - level in the tree
# weight - gross weight going from the root 
# value - gross value going from the root
# bound - max value for sub-tree givin from the current node
class Node:
    def __init__(self, level, weight, value):
        self.level = level
        self.weight = weight
        self.value = value
        self.bound = 0.0


# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")

def input_problem():
    print("---- NOTE ----\nThe file must be in the following format:\nn MAX\t\t\tWhere n - number of items  MAX - Maximum allowed weight\nW0 W1 W2 W3 ... Wn\nP0 P1 P2 P3 ... Pn")
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
    
    tmp = [x for x in next(f).split()]    # Reads the dimensions and max weight
    n = int(tmp[0])
    max_weight = float(tmp[1])
    weights = []
    prices = []
    weights = next(f).split()
    for i in range(0, len(weights)): 
        weights[i] = float(weights[i]) 
    
    prices = next(f).split()
    for i in range(0, len(prices)): 
        prices[i] = float(prices[i]) 
    
    
    f.close()
    return n, weights, prices, max_weight

# Calculates the maximum value for the sub-tree with the root u
# The items are sorted by the value/weight ratio in the begining
# Going through the sub-tree and picking up items if we are under given weight
# This greedy algorothm gives us the upper bound of the optimal solution
def bound(u, knapsack_weight, items):
    if (u.weight >= knapsack_weight):
        return 0
    total_value = u.value 
    l = u.level + 1
    total_weight = u.weight
    while l < len(items) and total_weight + items[l].weight <= knapsack_weight:
        total_weight += items[l].weight
        total_value += items[l].value
        l += 1
    if l < len(items):
        total_value += (knapsack_weight - total_weight) / items[l].weight * items[l].value
    return total_value

# Calculates the maximum value of BnB algorithm
# Q - row with currently visited nodes
def bnb(knapsack_weight, items):
    Q = queue.Queue()
    # Initializing on a node coming from -1
    u = Node(-1, 0, 0)
    Q.put(u)
    max_value = 0
    while not Q.empty():
        # u - current node
        u = Q.get()
        if (u.level == len(items) - 1): 
            continue
        # v - child node, if we took v
        v = Node(u.level + 1, u.weight + items[u.level + 1].weight, u.value + items[u.level + 1].value)
        # Checks if the maximum value increases with the current item
        if v.weight <= knapsack_weight and v.value > max_value:
            max_value = v.value
        # v will be taken into consideration if the result is better than the current optimum 
        # If it's not, we don't check anything further
        v.bound = bound(v, knapsack_weight, items)
        if (v.bound > max_value):
            Q.put(v)
        # v - child node, if we didn't take v
        v = Node(u.level + 1, u.weight, u.value)
        v.bound = bound(v, knapsack_weight, items) 
        if (v.bound > max_value):
            Q.put(v)    
    return max_value


def main():
    n, weights, prices, max_weight = input_problem()
    items = []
    for i in range(n):
        items.append(Item(weights[i], prices[i]))
    print_split()
    print("Maximal basket value: ", bnb(max_weight, items))

if __name__ == '__main__':
   main()