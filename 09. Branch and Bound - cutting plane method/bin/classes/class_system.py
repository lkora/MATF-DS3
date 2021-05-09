import numpy as np

class System:
    def __init__(self, *args):
        self.n = 0
        self.m = 0
        self.problem = ""
        self.c = np.array([])
        self.A = np.array([])
        self.sign = ""
        self.b = np.array([])
        self.solution_set = ""
        self.direction = ""
        self.lb = 0
        self.ub = 1

        # c A b 
        if len(args[0]) == 3:              
            self.c = args[0][0]
            self.A = args[0][1]
            self.b = args[0][2]
        
        # n, m, otype, in_c, in_A, sign, in_b, solution_set, lb, ub
        elif len(args[0]) == 10:
            self.n = args[0][0]
            self.m = args[0][1]
            self.problem = args[0][2]
            self.c = args[0][3]
            self.A = args[0][4]
            self.sign = args[0][5]
            self.b = args[0][6]
            self.solution_set = args[0][7]
            self.lb = args[0][8]
            self.ub = args[0][9]


