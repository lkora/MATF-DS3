from collections import defaultdict 
import os.path
from os import path
import numpy as np

# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")


def input_problem():
    print("---- NOTE ----\nThe file must be in the following format:\nn MAX\t\t\tWhere n - number of items  MAX - Maximum allowed price\nW0 W1 W2 W3 ... Wn\nP0 P1 P2 P3 ... Pn")
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
    
    n, max_weight = [int(x) for x in next(f).split()]    # Reads the dimensions and max weight
    weights = []
    prices = []
    weights = next(f).split()
    for i in range(0, len(weights)): 
        weights[i] = int(weights[i]) 
    
    prices = next(f).split()
    for i in range(0, len(prices)): 
        prices[i] = int(prices[i]) 
    
    
    f.close()
    return n, weights, prices, max_weight

# Iterative solution for Knapsack
# Returns the maximum value that can 
# be put in a knapsack of a given capacity
def knapsack(max_weight, weights, prices, n): 
    F = [[0 for x in range(max_weight + 1)] for x in range(n + 1)] 

    # Building matrix F[][] from the bottom-up 
    for i in range(n + 1): 
        for max_weight in range(max_weight + 1): 
            if i == 0 or max_weight == 0: 
                F[i][max_weight] = 0
            elif weights[i-1] <= max_weight: 
                F[i][max_weight] = max(prices[i-1] + F[i-1][max_weight-weights[i-1]], F[i-1][max_weight]) 
            else: 
                F[i][max_weight] = F[i-1][max_weight] 

    
    return F, F[n][max_weight] 


def main():
    n, weights, prices, max_weight = input_problem()
    print()
    F, solution = knapsack(max_weight, weights, prices, n)
    F = np.array(F)
    print("F:\n", F)
    print_split()
    print("Maximal basket value: ", solution)

if __name__ == '__main__':
   main()