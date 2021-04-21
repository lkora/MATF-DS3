# Prints a bar
def print_split():
    print("\n--------------------------------------------------\n")


def write_element(el, max_length, tmp = ''):
    length = max_length - len(el)
    padding_left = length//2
    padding_right = length - padding_left

    new_element = ' '*padding_left + el + ' '*padding_right
    print(new_element, end=tmp)

def write_table(table):
    # Adding padding left and right so that the output looks nice
    max_length = 0
    for row in table:
        for el in row:
            max_length = max(max_length, len(str(el))+4)

    underscore = '-'*( (len(table[0])) * (max_length+1) )

    for i in range(len(table)):
        for j in range(len(table[i])):
            write_element( str(table[i][j]), max_length, tmp='|')
        print()
        print(underscore)

def print_initial(Z_set):
    # Writing the initial problem for the given set
    if Z_set:
        print(' for xi in set Z')
    else:
        print(' for xi in set [0-1]')
    print()
