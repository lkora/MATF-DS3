import numpy as np

class System:
    def __init__(self, *args):
        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = 0     # rezultat funkcije!
        self.problem = ""
        self.koefs_problema = np.array([])
        self.niz_znakova = np.array([])
        self.matricaA = np.array([])
        self.matricaB = np.array([])
        self.P = np.array([])
        self.Q = np.array([])
        self.x = np.array([])
        
        # c A b 
        if len(args[0]) == 3:              
            self.koefs_problema = args[0][0]
            self.matricaA = args[0][1]
            self.matricaB = args[0][2]
        
        # n, m, otype, in_c, in_A, sign, in_b
        elif len(args[0]) == 7:
            self.br_vrsta = args[0][0]
            self.br_kolona = args[0][1]
            self.problem = args[0][2]
            self.koefs_problema = args[0][3]
            self.matricaA = args[0][4]
            self.niz_znakova = args[0][5]
            self.matricaB = args[0][6]


