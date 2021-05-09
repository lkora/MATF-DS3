from .print_ import print_split
from ortools.linear_solver import pywraplp


def branch_and_bound(s):
    print("Starting Branch and Bound with cutting planes!")
    print_split()

    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()
    if s.solution_set == 'inf':
        s.ub = infinity

    # Check if valid bounds have been entered
    if s.lb < 0 or s.ub < 0 or s.ub <= s.lb:
        print("Illegal bounds!")
        return


    # Define the variables
    x = {}
    for j in range(s.m):
        x[j] = solver.IntVar(s.lb, s.ub, 'x[%i]' % j)
    print('Number of variables =', solver.NumVariables())

    # Define the constraints
    for i in range(s.n):
        constraint_expr = [s.A[i][j] * x[j] for j in range(s.m)]
        solver.Add(sum(constraint_expr) <= s.b[i])
    print('Number of constraints =', solver.NumConstraints())

    # for i in range(s.n):
    #     constraint = solver.RowConstraint(0, s.b[i], '')
    #     for j in range(s.m):
    #         constraint.SetCoefficient(x[j], s.A[i, j])

    # Define the objective function
    objective = solver.Objective()
    for j in range(s.m):
        objective.SetCoefficient(x[j], s.c[j])
    
    # Set mode
    if s.problem == 'min':
        objective.SetMinimization()
    elif s.problem == 'max':
        objective.SetMaximization()
    else:
        raise Exception("Invalid mode operation!")

    # Solve
    status = solver.Solve()
    
    # Print results
    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        for j in range(s.m):
            print(x[j].name(), ' = ', x[j].solution_value())   
        print()

        print('Problem solved in %f milliseconds' % solver.wall_time())
        # print('Problem solved in %d iterations' % solver.iterations())
        # print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    else:
        print('The problem does not have an optimal solution.')
    print_split()
