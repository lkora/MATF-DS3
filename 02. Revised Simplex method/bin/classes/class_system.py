import numpy as np

class System:
    def __init__(self, *args):
        self.n = 0
        self.m = 0
        self.function_result = 0
        self.problem = ""
        self.c = np.array([])
        self.sign_array = np.array([])
        self.A = np.array([])
        self.B = np.array([])
        self.P = np.array([])
        self.Q = np.array([])
        self.x = np.array([])
        
        # c A b 
        if len(args[0]) == 3:              
            self.c = args[0][0]
            self.A = args[0][1]
            self.B = args[0][2]
        
        # n, m, otype, in_c, in_A, sign, in_b
        elif len(args[0]) == 7:
            self.n = args[0][0]
            self.m = args[0][1]
            self.problem = args[0][2]
            self.c = args[0][3]
            self.A = args[0][4]
            self.sign_array = args[0][5]
            self.B = args[0][6]


