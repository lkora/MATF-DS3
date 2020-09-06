import numpy as np
import os.path
from os import path
import math
import copy
from collections import deque


class NotFound(Exception): pass
np.set_printoptions(suppress=True, precision=3)


class Data:

    def __init__(self):
        self.n = 0
        self.m = 0
        self.rez_funkcije = 0
        self.costs = np.array([])
        self.demand = np.array([])
        self.supply = np.array([])


flag_flatten_row, flag_flatten_rcolumn = 0, 0
iter = 1
rows, columns = 0, 0


# Prints a bar
def print_split():
    print("--------------------------------------------------\n")


def input_vars():
    system = Data()
    option = 0
    while option != 1 or option != 2:
        if option == 1:
            print("---- NOTE ----\nThe input must be in the following format:\nN M\t\t\t\tWhere N - number of supply constraints and M - number of demand constraints\nA11 A12 ... A1M s1\nA21 A22 ... A2M system\n................\nAN1 AN2 ... ANM sN\nd1 d2 d3 ... dM")
            print_split()

            system.n = int(input("Input the number of supply constraints: "))
            system.m = int(input("Input the number of demand constraints: "))

            # Reserving and initializing space for demand
            system.demand = np.zeros(system.m, dtype=int)
            # Reserving and initializing space for costs
            system.costs = np.zeros((system.n, system.m), dtype=int)
            # Reserving and initializing space for supply
            system.supply = np.zeros(system.n, dtype=int)
            
            print("Input costs and supply row by row in the format stated above:")
            # Inputing the cost and supply
            for i in range(system.n):
                # Input a line to a tmp variable
                tmp = input(str(i) + ": ").split()
                for j in range(system.m):
                    system.costs[i, j] = int(tmp[j])
                system.supply[i] = int(tmp[system.m])
            # Inputing demand
            print("Input the demand:")
            tmp = input().split()
            system.demand = int(tmp)

            break


        elif option == 2:
            print("---- NOTE ----\nEnter the relative path to the file, from under \"/examples/\" \ne.g. For file 1.txt, write \"1.txt\", that will load \"/examples/1.txt\"")
            print_split()
            print("---- NOTE ----\nThe input must be in the following format:\nN M\t\t\t\tWhere N - number of supply constraints and M - number of demand constraints\nA11 A12 ... A1M s1\nA21 A22 ... A2M system\n................\nAN1 AN2 ... ANM sN\nd1 d2 d3 ... dM")
            print_split()
            print_split()
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
            
            system.n, system.m = [int(x) for x in next(f).split()] # Reads the dimensions

            # Reserving and initializing space for costs
            system.costs = np.zeros((system.n, system.m), dtype=int)
            # Reserving and initializing space for supply
            system.supply = np.zeros(system.n, dtype=int)
            # Reserving and initializing space for demand
            system.demand = np.zeros(system.m, dtype=int)
            
            for i in range(system.n):
                tmp_array = [int(x) for x in next(f).split()]
                for j in range(system.m+1):
                    if j < system.m:
                        system.costs[i, j] = int(tmp_array[j])
                    else:
                        system.supply[i] = int(tmp_array[j])
                tmp_array.clear()
            system.demand = np.array([int(x) for x in next(f).split()])
            
            f.close()
            break
                    
        else:
            option = int(input("Select the type of input:\n\t1: Manual input\n\t2: Input from file\nSelected: "))
            print_split()

    return system

def print_system(system):

    for i in range(len(system.costs)):
        for j in range(len(system.costs[0])):
            print('{: 6}'.format(system.costs[i][j]), end=" ")
        print('{: 6}'.format(system.supply[i]))

    for i in range(system.m):
        print('{: 6}'.format(system.demand[i]), end=" ")

    print()
    print_split()

def least_cost_method(problem_matrix, potential_matrix):
    tmp_matrix = copy.copy(problem_matrix.costs)
    erased_row = 0
    erased_column = 0

    # Choosing min from matrix C and updating value b and a in the row/column of that minumum
    while len(np.where(tmp_matrix != 10000)[0]) > 0:
        # Choosing the 1st minimum if there are more
        minimums = np.where(tmp_matrix == np.min(tmp_matrix))
        min_row = minimums[0][0]
        min_column = minimums[1][0]
        potential = min(problem_matrix.demand[min_column], problem_matrix.supply[min_row])

        potential_matrix.costs[min_row][min_column] = potential

        erase_column = 0
        if problem_matrix.demand[min_column] == problem_matrix.supply[min_row]:
            if erased_column <= erased_row:
                erase_column = 1

        if (potential == problem_matrix.demand[min_column] and potential != problem_matrix.supply[min_row]) or \
                (potential == problem_matrix.demand[min_column] and erase_column):

            problem_matrix.demand[min_column] = 0
            problem_matrix.supply[min_row] -= potential
            tmp_matrix[:, min_column] = 10000
            erased_column += 1
        else:
            problem_matrix.supply[min_row] = 0
            problem_matrix.demand[min_column] -= potential
            tmp_matrix[min_row, :] = 10000
            erased_row += 1


def create_adjacency_list(A):
    adjacency_list = {}
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if A[i][j] != 0:
                # Looking only at neighbours in the column for even numbers
                if A[i][j] % 2 == 0:
                    column_neighbours = [(k * 10 + j) for k in range(A.shape[0]) if A[k, j] != 0 and k != i]
                    adjacency_list[i * 10 + j] = column_neighbours
                # Looking only at neighbours in the rpw for odd numbers
                else:
                    row_neighbours = [(i * 10 + k) for k in range(A.shape[1]) if A[i, k] != 0 and k != j]
                    adjacency_list[i * 10 + j] = row_neighbours

    return adjacency_list


def search(graph, start, finish):
    visited = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == finish:
            walk = []
            while node is not None:
                walk.append(node)
                node = visited[node]
            return walk[::-1]
        for adjacent in graph[node]:
            if adjacent not in visited:
                visited[adjacent] = node
                queue.append(adjacent)


def find_cycle(most_negative_row, most_negative_column, potential_matrix):
    A = np.zeros(potential_matrix.costs.shape)
    A[most_negative_row][most_negative_column] = 1
    potential_matrix.costs[most_negative_row][most_negative_column] = 0
    marked = 1

    while 1:
        # Odd, we are going through rows
        if marked % 2 != 0:
            basis_rows = np.where(A == marked)[0]
            if np.size(basis_rows) == 0:
                break

            for i in basis_rows:
                base = np.where(potential_matrix.costs[i] != float('-inf'))[0]
                for j in base:
                    if A[i, j] == 0:
                        A[i, j] = marked + 1

        # Even, we are going through columns
        else:
            basis_columns = np.where(A == marked)[1]
            if np.size(basis_columns) == 0:
                break
            for j in basis_columns:
                base = np.where(potential_matrix.costs[:, j] != float('-inf'))[0]
                for t in base:
                    if A[t, j] == 0:
                        A[t, j] = marked + 1

        marked += 1

    # Making adjacency list 
    adjacency_list = create_adjacency_list(A)
    start = most_negative_row * 10 + most_negative_column

    # Finding the ending node that has a child as a root node
    finish = 0
    for i in adjacency_list:
        for j in adjacency_list[i]:
            if j == start:
                finish = i

    positions = search(adjacency_list, start, finish)

    sign = -1
    theta = np.zeros((A.shape[0], A.shape[1]))

    for position in positions:
        sign *= -1
        i = int(position / 10)
        j = position % 10
        theta[i, j] = sign

    theta[most_negative_row, most_negative_column] = 1
    print("Theta, cycle:\n", theta)

    # Looking for min Theta
    potential_minimum = np.array([])
    potential_indices = np.array([])
    rows, columns = np.where(theta == -1)

    for i, j in zip(rows, columns):
        potential_minimum = np.append(potential_minimum, potential_matrix.costs[i][j])
        potential_indices = np.append(potential_indices, i * 10 + j)

    theta_row = min(potential_minimum)
    print("Theta min:", theta_row)
    index = np.where(potential_minimum == theta_row)[0][0]

    potential_matrix.costs = potential_matrix.costs + theta * theta_row
    v = int(potential_indices[index] / 10)
    k = int(potential_indices[index] % 10)
    potential_matrix.costs[v, k] = float('-inf')

    print("New matrix potential:\n", potential_matrix.costs)
    return potential_matrix.costs


def method_of_potentials(problem_matrix, potential_matrix):
    global iter
    print("Iteration:", iter)
    max_basis_row = 0
    max_basis_column = 0
    max_row = 0
    max_column = 0
    potential_matrix.demand = np.repeat(float('-inf'), potential_matrix.m)
    potential_matrix.supply = np.repeat(float('-inf'), potential_matrix.n)

    # Searching for a row with the most basis variables
    for i, row in enumerate(potential_matrix.costs):
        no_basis = np.size(np.where(row != float('-inf'))[0])
        if no_basis > max_basis_row:
            max_basis_row = no_basis
            max_row = i

    # Searching for a column with the most basis variables
    for j, column in enumerate(potential_matrix.costs.T):
        no_basis = np.size(np.where(column != float('-inf'))[0])
        if no_basis > max_basis_column:
            max_basis_column = no_basis
            max_column = j

    # We choose a row or a column with the most basis variables in the begining 
    if max_basis_row >= max_basis_column:
        potential_matrix.supply[max_row] = 0
    else:
        potential_matrix.demand[max_column] = 0

    print_system(potential_matrix)
    # Calculating for all untill we fill all A and B fields
    while np.size(np.where(potential_matrix.demand == float('-inf'))[0]) > 0 \
            or np.size(np.where(potential_matrix.supply == float('-inf'))[0]) > 0:

        # Going through rows and where the value is present in A, we are looking for the basis in the row
        # and for their columns, writing the result B - Ai in matrix
        for r, number in enumerate(potential_matrix.supply):
            if number != float('-inf'):

                bazisne = np.where(potential_matrix.costs[r] != float('-inf'))[0]
                for m in bazisne:
                    potential_matrix.demand[m] = problem_matrix.costs[r, m] - potential_matrix.supply[r]

        # Going through columns and doing the same thing, but now we are looking at B and
        # putting the result B - Bi in matrix A
        for r, number in enumerate(potential_matrix.demand):
            if number != float('-inf'):

                new_basis = np.where(potential_matrix.costs[:, r] != float('-inf'))[0]
                for m in new_basis:
                    potential_matrix.supply[m] = problem_matrix.costs[m, r] - potential_matrix.demand[r]

    print("Matrices after update:\n")
    print_system(problem_matrix)
    print_system(potential_matrix)

    flag = 0
    tmp_most_negative = float('+inf')
    most_negative = 0
    most_negative_row = 0
    most_negative_column = 0

    # Checking for the goal requrement: N - (Ai + Bj) >= 0
    for i, row in enumerate(potential_matrix.costs):
        for j, costs_value in enumerate(row):

            dif = problem_matrix.costs[i][j] - (potential_matrix.demand[j] + potential_matrix.supply[i])
            if costs_value == float('-inf') and dif < 0:

                flag = 1
                if dif < tmp_most_negative:
                    most_negative_row = i
                    most_negative_column = j
                    most_negative = problem_matrix.costs[i][j]
                    tmp_most_negative = dif

    # Calculating the optimal solution
    if flag == 0:
        # Deleting flattening row/column if we added it already
        if flag_flatten_row > 0:
            potential_matrix.costs = potential_matrix.costs[:-flag_flatten_row, :]
        elif flag_flatten_rcolumn > 0:
            potential_matrix.costs = potential_matrix.costs[:, :-flag_flatten_rcolumn]

        final_sum = 0
        for i, row in enumerate(potential_matrix.costs):
            for j, costs_value in enumerate(row):

                if costs_value != float('-inf'):
                    final_sum += costs_value * problem_matrix.costs[i][j]

        print("Optimal solution:", final_sum)
        exit()

    potential_matrix.costs = find_cycle(most_negative_row, most_negative_column, potential_matrix)

    iter += 1
    return method_of_potentials(problem_matrix, potential_matrix)


def main():
    global flag_flatten_rcolumn, flag_flatten_row
    problem_matrix = input_vars()

    # If sumaB != sumaA we add row/column and difference in demand/supply to make it equal
    dif = sum(problem_matrix.demand) - sum(problem_matrix.supply)
    num_ones_demand = len(np.where(problem_matrix.demand == 1)[0])
    num_ones_supply = len(np.where(problem_matrix.supply == 1)[0])

    if num_ones_demand == problem_matrix.m and num_ones_supply == problem_matrix.n:
        if dif > 0:
            flag_flatten_row = abs(dif)
            problem_matrix.n += abs(dif)
            for i in range(flag_flatten_row):
                problem_matrix.costs = np.append(problem_matrix.costs, [np.repeat(500, problem_matrix.m)], axis=0)
                problem_matrix.supply = np.append(problem_matrix.supply, 1)

        elif dif < 0:
            flag_flatten_rcolumn = abs(dif)
            problem_matrix.m += abs(dif)
            for i in range(flag_flatten_rcolumn):
                problem_matrix.costs = np.append(problem_matrix.costs, np.repeat(500, problem_matrix.n)
                                           .reshape(problem_matrix.n, 1), axis=1)
                problem_matrix.demand = np.append(problem_matrix.demand, 1)

    else:
        if dif > 0:
            flag_flatten_row = 1
            problem_matrix.n += 1
            problem_matrix.costs = np.append(problem_matrix.costs, [np.repeat(500, problem_matrix.m)], axis=0)
            problem_matrix.supply = np.append(problem_matrix.supply, [dif], axis=0)

        elif dif < 0:
            flag_flatten_rcolumn = 1
            problem_matrix.m += 1
            problem_matrix.costs = np.append(problem_matrix.costs, np.repeat(500, problem_matrix.n)
                                       .reshape(problem_matrix.n, 1), axis=1)
            problem_matrix.demand = np.append(problem_matrix.demand, -dif)

    # Creating a starting potential matrix
    potential_matrix = Data()
    potential_matrix.n = problem_matrix.n
    potential_matrix.m = problem_matrix.m

    potential_matrix.costs = np.repeat(float('-inf'), potential_matrix.n * potential_matrix.m)\
        .reshape((potential_matrix.n, potential_matrix.m))
    potential_matrix.demand = np.repeat(float('-inf'), potential_matrix.m)
    potential_matrix.supply = np.repeat(float('-inf'), potential_matrix.n)
    
    print("\n")
    print_system(problem_matrix)
    print_system(potential_matrix)

    least_cost_method(problem_matrix, potential_matrix)
    print("Matrices after Least Cost Method:\n")
    print_system(problem_matrix)
    print_system(potential_matrix)

    method_of_potentials(problem_matrix, potential_matrix)


if __name__ == '__main__':
    main()