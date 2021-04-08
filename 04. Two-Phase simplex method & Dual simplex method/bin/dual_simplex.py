import math
import random

bland_rule = True
max_iter = math.inf

def dual_simplex(s):
    func = 0
    iter_no = 0
    while True:
        neg_b = [i for i in s.B if i < 0]

        if iter_no >= max_iter:
            print('Exceeded maximum number of iterations: {}'.format(iter_no))
            break

        if len(neg_b)==0:
            break
            # No negatives, we found an optimal solution
        else:
            # We go to a next step
            # If s.B < 0 exists we save that index
            nb = next(i for i, x in enumerate(s.B) if x<0)
            if not bland_rule:
                nb = random.choice([i for i, x in enumerate(s.B) if x<0])
            # If all are >0 then there is no feasible solution
            if all(i>0 for i in s.A[nb]):
                print('No feasible solution all elments are > 0 in the row.')
                quit()
            else:
                # Looking for a maximum element from all the negative values in the row  c[j] / s.A[red][j]
                ind = -1
                max = -math.inf

                for i in range(len(s.A[nb])):
                    if s.A[nb][i] < 0 and s.c[i] / s.A[nb][i] > max:
                        ind = i
                        max = s.c[i] / s.A[nb][i]

                if ind == -1:
                    print('Simplex error! Negative ')
                    quit()
                # Dividing the row with s.A[nb][ind]
                s.B[nb] /= s.A[nb][ind]
                s.A[nb] = [i/s.A[nb][ind] for i in s.A[nb]]

                # Pivoting, making zeroes above and bellow
                for i in range(len(s.A)):
                    if i!=nb:
                        mult = s.A[i][ind]
                        s.A[i] = [i-mult*j for i,j in zip(s.A[i],s.A[nb])]
                        s.B[i] -= mult*s.B[nb]
                zmult = s.c[ind]
                s.c = [z-zmult*j for z,j in zip(s.c,s.A[nb])]
                func += s.B[nb] * zmult
                # Creating the new base
                s.Q[nb] = ind
                iter_no +=1

    solution = [0] * len(s.A[0])
    for i in range(len(s.B)):
        solution[s.Q[i]] = s.B[i]
    print('Optimal solution found at: [',end='')
    for i in solution:
        print('{} '.format(round(i,2)),end='')
    print(']')
    print('Function maximum: {}'.format(round(func,2)))
