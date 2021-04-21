import numpy as np

class System:
    def __init__(self, *args):
        self.m = 0
        self.problem = ""
        self.c = np.array([])
        self.A = np.array([])
        self.sign = ""
        self.b = np.array([])
        self.solution_set = ""
        self.direction = ""

        # c A b 
        if len(args[0]) == 3:              
            self.c = args[0][0]
            self.A = args[0][1]
            self.b = args[0][2]
        
        # m, otype, in_c, in_A, sign, in_b, solution_set
        elif len(args[0]) == 8:
            self.m = args[0][0]
            self.problem = args[0][1]
            self.c = args[0][2]
            self.A = args[0][3]
            self.sign = args[0][4]
            self.b = args[0][5]
            self.solution_set = args[0][6]
            self.direction = args[0][7]


