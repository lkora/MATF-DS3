decimal_space = 2

# Prints a bar
def print_split():
    print("--------------------------------------------------\n")

def print_variable(max_length, S, W, variable):
    if variable in S:
        ind = S.index(variable)
        length = max_length - len('s'+str(ind))
        left = length // 2
        right = length - left
        print(' '*(left) + 's'+str(ind) + ' '*right,end='')
    elif variable in W:
        ind = W.index(variable)
        length = max_length - len('w'+str(ind))
        left = length // 2
        right = length - left
        print(' '*(left) + 'w'+str(ind) + ' '*right,end='')
    else:
        length = max_length- len('x'+str(variable))
        left = length // 2 
        right = length - left
        print(' '*(left) + 'x'+str(variable) + ' '*right,end='')

    
def print_number(max_length,number):

    if number.is_integer():
        length = max_length - len(str(int(number)))
        left = length//2
        right = length - left
        s = ' '*left + str(int(number)) + ' '*right
        print(s,end='')
    else:
        length = max_length - len(str(round(number, decimal_space)))
        left = length//2
        right = length - left
        s = ' '*left + str(round(number, decimal_space)) + ' '*right
        print(s,end='')


def print_simplex_table(table, B, S, W):
        max_length = 0
        for row in table:
            for element in row:
                if element.is_integer():
                    max_length = max(max_length,len(str(int(element)))+3)
                else:
                    max_length = max(max_length,len(str(round(element,decimal_space)))+3)

        for i in range(len(table[0])-1):
            max_length = max(max_length,len('x'+str(i))+2)

        print(' '*(max_length+2),end='')
        for i in range(len(table[0])-1):
            print_variable(max_length, S, W, i)
        print()
        print('-'*max_length*(len(table[0])+1))

        for i in range(len(table)-1):
            print_variable(max_length, S, W, B[i])
            print('|',end='')
            for j in range(len(table[i])-1):
                print_number(max_length, table[i][j])
            print('|',end='')
            print_number(max_length, table[i][-1])
            print()
        
        print('-'*max_length*(len(table[0])+1))
        print(' '*(max_length+1),end='')
        for i in range(len(table[-1])-1):
            print_number(max_length, table[-1][i])
        print('|',end='')
        print_number(max_length,table[-1][-1])
        print()

