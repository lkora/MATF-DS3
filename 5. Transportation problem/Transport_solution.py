import os.path
from os import path
from collections import deque
import numpy as np

# TODO: FIX POTENTIAL METHOD!!!

# Prints a bar
def print_split():
    print("--------------------------------------------------\n")

# Print the system
def print_table(costs, supply, demand):
    width = len(costs[0])
    height = len(costs)

    print("\t", end=" ")
    for j in range(width):
        print("D" + str(j) + "\t", end=" ")
    print("Supply")

    for i in range(height):
        for j in range(width + 1):
            if j == 0:
                print("S" + str(i) + "\t", end=" ")
            if j == width:
                print(str(supply[i]) + "\t", end=" ")
            else:
                print(str(costs[i, j, 0]) + "(" + str(costs[i, j, 1]) + ")\t", end=" ")
        print("")
    
    print("Demand\t", end=" ")
    for j in range(width):
        print(str(demand[j]) + "\t", end=" ")
    
    print("")
    print_split()


def input_vars():    
    option = 0
    while option != 1 or option != 2:
        if option == 1:
            print("---- NOTE ----\nThe input must be in the following format:\nN M\t\t\t\tWhere N - number of supply constraints and M - number of demand constraints\nA11 A12 ... A1M s1\nA21 A22 ... A2M s2\n................\nAN1 AN2 ... ANM sN\nd1 d2 d3 ... dM")
            print_split()

            n = int(input("Input the number of supply constraints: "))
            m = int(input("Input the number of demand constraints: "))

            # Reserving and initializing space for the Objective function
            demand = np.zeros(m, dtype=int)
            # Reserving and initializing space for the coeficients
            costs = np.zeros((n, m, 3), dtype=int)
            # Reserving and initializing space for the solution values
            supply = np.zeros(n, dtype=int)

            print("Input costs and supply row by row in the format stated above:")
            # Inputing the cost and supply
            for i in range(n):
                # Input a line to a tmp variable
                tmp = input(str(i) + ": ").split()
                for j in range(m):
                    costs[i, j, 0] = int(tmp[j])
                supply[i] = int(tmp[m])
            # Inputing demand
            print("Input the demand:")
            tmp = input().split()
            demand = int(tmp)

            break


        elif option == 2:
            print("---- NOTE ----\nEnter the relative path to the file, from under \"/examples/\" \ne.g. For file 1.txt, write \"1.txt\", that will load \"/examples/1.txt\"")
            print_split()
            print("---- NOTE ----\nThe input must be in the following format:\nN M\t\t\t\tWhere N - number of supply constraints and M - number of demand constraints\nA11 A12 ... A1M s1\nA21 A22 ... A2M s2\n................\nAN1 AN2 ... ANM sN\nd1 d2 d3 ... dM")
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
            
            n, m = [int(x) for x in next(f).split()] # Reads the dimensions

            # Reserving and initializing space for the Objective function
            demand = np.zeros(m, dtype=int)
            # Reserving and initializing space for the coeficients
            costs = np.zeros((n, m, 3), dtype=int)
            # Reserving and initializing space for the solution values
            supply = np.zeros(n, dtype=int)
            # Read the dimensions and A and b
            
            for i in range(n):
                tmp_array = [int(x) for x in next(f).split()]
                for j in range(m+1):
                    if j < m:
                        costs[i, j, 0] = int(tmp_array[j])
                    else:
                        supply[i] = int(tmp_array[j])
                tmp_array.clear()
            demand = [int(x) for x in next(f).split()]

            f.close()
            break
                    
        else:
            option = int(input("Select the type of input:\n\t1: Manual input\n\t2: Input from file\nSelected: "))
            print_split()

    return costs, supply, demand

def find_min_cell(A):
    width = len(A[0])
    height = len(A)
    min = np.Inf
    r = -1
    c = -1
    for i in range(height):
        for j in range(width):
            if A[i, j, 2] == 0 and min > A[i, j, 0]:
                min = A[i, j, 0]
                r = i
                c = j
    if r == -1 or c == -1:
        print("Error finding the minimum! How is this even possible??")
        return -1
    return r, c, min

def add_dummy(costs, supply, demand):
    demand_sum = sum(demand)
    supply_sum = sum(supply)
    
    # No dummy constraint needed
    if demand_sum == supply_sum:
        return costs, supply, demand
    # Adding dummy
    # We need to see if we need a column or a row dummy constraint
    if demand_sum < supply_sum:     # Adding demand constraint with 0 cost
        diff = supply_sum - demand_sum
        demand = np.append(demand, diff)
        costs = np.concatenate((costs, np.zeros((len(costs), 1, 3), dtype=int)), axis=1)

        print("Added a dummy demand constraint with 0 unit cost and with allocation " + str(diff))
        print_table(costs, supply, demand)
    else:                           # Adding supply constraint with 0 cost
        diff = demand_sum - supply_sum
        supply = np.append(supply, diff)
        costs = np.concatenate((costs, np.zeros((1, len(costs[0]), 3), dtype=int)), axis=0)

        print("Added a dummy supply constraint with 0 unit cost and with allocation " + str(diff))
        print_table(costs, supply, demand)
    
    return costs, supply, demand


# def create_a_graph(tmp):
#     graph = {}
#     for i in range(tmp.shape[0]):
#         for j in range(tmp.shape[1]):
#             if tmp[i][j] != 0:
#                 # For an even number just look at the neighbours in the column
#                 if tmp[i][j] % 2 == 0:
#                     col_neighbours = [(k * 10 + j) for k in range(tmp.shape[0]) if tmp[k][j] != 0 and k != i]
#                     graph[i * 10 + j] = col_neighbours

#                 # For an odd number just look at the neighbours in row
#                 else:
#                     row_neighbours = [(i * 10 + k) for k in range(tmp.shape[1]) if tmp[i][k] != 0 and k != j]
#                     graph[i * 10 + j] = row_neighbours

#     return graph


# def search(graph, start, finish):
#     visited = {start: None}
#     queue = deque([start])
#     while queue:
#         vertex = queue.popleft()
#         if vertex == finish:
#             walk = []
#             while vertex is not None:
#                 walk.append(vertex)
#                 vertex = visited[vertex]
#             return walk[::-1]
#         for neighbouring in graph[vertex]:
#             if neighbouring not in visited:
#                 visited[neighbouring] = vertex
#                 queue.append(neighbouring)

# def find_cycle(most_negative_row, most_negative_col, potential_matrix):
#     tmp = np.zeros(potential_matrix.mat_c.shape)
#     tmp[most_negative_row][most_negative_col] = 1
#     potential_matrix.mat_c[most_negative_row][most_negative_col] = 0
#     marked = 1

#     while 1:

#         # Neparan pa idemo po vrstama
#         if marked % 2 != 0:

#             base_row = np.where(tmp == marked)[0]
#             if np.size(base_row) == 0:
#                 break

#             for i in base_row:

#                 base = np.where(potential_matrix.mat_c[i] != float('-inf'))[0]
#                 for j in base:

#                     if tmp[i][j] == 0:
#                         tmp[i][j] = marked + 1

#         # Paran pa idemo po kolonama
#         else:

#             base_cols = np.where(tmp == marked)[1]
#             if np.size(base_cols) == 0:
#                 break

#             for j in base_cols:
#                 base = np.where(potential_matrix.mat_c[:, j] != float('-inf'))[0]

#                 for t in base:
#                     if tmp[t][j] == 0:
#                         tmp[t][j] = marked + 1

#         marked += 1

#     # Pravimo listu povezanosti
#     graph = create_a_graph(tmp)
#     start = most_negative_row * 10 + most_negative_col

#     # Pronalazimo krajnji cvor koji ima za potomka koreni cvor
#     finish = 0
#     for i in graph:
#         for j in graph[i]:
#             if j == start:
#                 finish = i

#     positions = search(graph, start, finish)

#     sign = -1
#     theta = np.zeros((tmp.shape[0], tmp.shape[1]))

#     for position in positions:
#         sign *= -1
#         i = int(position / 10)
#         j = position % 10
#         theta[i][j] = sign

#     theta[most_negative_row][most_negative_col] = 1
#     print("theta, cikl:\n", theta)

#     # Finding minimal theta
#     pot_min = np.array([])
#     possible_indexes = np.array([])
#     vrste, kolone = np.where(theta == -1)

#     for i, j in zip(vrste, kolone):
#         pot_min = np.append(pot_min, potential_matrix.mat_c[i][j])
#         possible_indexes = np.append(possible_indexes, i * 10 + j)

#     theta_row = min(pot_min)
#     print("Theta min:" + str(theta_row))
#     index = np.where(pot_min == theta_row)[0][0]

#     potential_matrix.mat_c = potential_matrix.mat_c + theta * theta_row
#     v = int(possible_indexes[index] / 10)
#     k = int(possible_indexes[index] % 10)
#     potential_matrix.mat_c[v][k] = float('-inf')

#     print("Nova matrica potencijala:\n", potential_matrix.mat_c)
#     return potential_matrix.mat_c



# LCM - Least Cost Method
# STEP1:    Select the cell having minimum unit cost Cij and allocate as much as possible, i.e. min(Si,Dj)
# STEP2a:   Subtract this min value from supply si and demand Dj.
# STEP2b:   If the supply Si is 0, then cross that row and if the demand Dj is 0 then cross that column.
# STEP2c:   If min unit cost cell is not unique, then select the cell where maximum allocation can be possible
# STEP3:    Repeact this steps for all uncrossed rows and columns until all supply and demand values are equal to 0.
def least_cost_method(costs, supply, demand):
    costs, supply, demand = add_dummy(costs, supply, demand)
    width = len(demand)
    height = len(supply)
    it = 1
    while any(demand) and any(supply):
        print("Iteration " + str(it) + ":\n")
        it += 1
        r, c, min_c = find_min_cell(costs)
        print("The smallest transportation cost is: " + str(min_c) + " in cell S" + str(r) + "D" + str(c))
        min_sd = min(supply[r], demand[c])
        print("The allocation to this cell is: min(" + str(supply[r]) + ", " + str(demand[c]) + ") = " + str(min_sd) + ".")
        if supply[r] < demand[c]:
            print("This exhausts the supply of S" + str(r) + " and leaves " + str(demand[c]) + " - " + str(supply[r]) + " = " + str(demand[c] - supply[r]) + " units with D" + str(c))
            demand[c] -= supply[r]
            supply[r] = 0
            costs[r, c, 1] = min_sd
            for j in range(width):
                costs[r, j, 2] = 1
        elif supply[r] > demand[c]:
            print("This satisfies the entire demand of D" + str(c) + " and leaves " + str(supply[r]) + " - " + str(demand[c]) + " = " + str(supply[r] - demand[c]) + " units with S" + str(r))
            supply[r] -= demand[c]
            demand[c] = 0
            costs[r, c, 1] = min_sd
            for i in range(height):
                costs[i, c, 2] = 1
        else:
            costs[r, c, 1] = min_sd
            supply[r] = 0
            demand[c] = 0
            # for i in range(height):
            #     for j in range(width):
            #         costs[i, j, 2] = 1
            costs[:, c, 2] = 1
            costs[r, :, 2] = 1

        print("")
        print_table(costs, supply, demand)

    print("The minimum transportation cost =", end="")
    number_of_allocated_cells = 0
    total_cost = 0
    for i in range(height):
        for j in range(width):
            if costs[i, j, 1] != 0:
                number_of_allocated_cells += 1
                print(" (" + str(costs[i, j, 0]) + " * " + str(costs[i, j, 1]) + ")", end=" ")
                total_cost += costs[i, j, 0] * costs[i, j, 1]
    print(" = " + str(total_cost))

    if (width+height-1) == number_of_allocated_cells:
        print("The number of allocated cells is: " + str(number_of_allocated_cells) + " and is equal to (n + m - 1)")
        print("The solution is non-degenerate")
    else:
        print("The number of allocated cells " + str(number_of_allocated_cells) + " doesn't equal to (n + m -1)")
        print("The solution is degenerate")
    print_split()


def main():
    print("Transportation problem")
    print_split()
    costs, supply, demand = input_vars()
    print("Entered problem:\n")
    print_table(costs, supply, demand)
    print("Least cost method:\n")
    least_cost_method(costs, supply, demand)


if __name__ == '__main__':
   main()