# When using don't forget:
# in exrex package \1 have to be written as \\1 
import exrex
import re
num_puzzles = 0
num_rows = list()
num_columns = list()
num_empty_cells = list()
rows = dict()
columns = dict()
solved_boards = dict()
limitting_num = 10000
    
def get_difference(l1, l2):
    return [x for x in l1 if x in l2]
    
def remove_outliers(list, k):
    for word in list[:]:        #note the [:]
        if len(word) != k:
            list.remove(word)
        
def get_letters(regex, limit, position, current_str):
    possible_strs = list()
    if limitting_num > 10000000:
        for i in range(limitting_num/100):
            #phase = 1
            #if float(i/10000) > 1:
            #    print i
            #    phase +=1
            possible_strs.append(exrex.getone(regex, limit = limit + 1))
                
    else:            
        gen = exrex.generate(regex, limit = limit + 1)
        i = 0
        for i in range(limitting_num):
            str = next(gen, None)
            if str != None:
                possible_strs.append(str)
            else:
                break

    #possible_strs = list(exrex.generate(regex, limit = limit + 1))
    #print 'possibilities: {}'.format(possible_strs)
    # removing all strings shorter than we need
    #print limit
    remove_outliers(possible_strs, limit)
    #print 'possibilities: {}'.format(possible_strs)
    # Cut all the strings that don't match current string
    is_bad = False
    chosen_strs = list()
    for string in possible_strs:
        for j in range(len(string)):
            if string[j] != current_str[j] and current_str[j] != '~':
                is_bad = True
        if is_bad: 
            is_bad = False
            continue
        else:
            chosen_strs.append(string)
            
    # Collect all possible variations of position' letter
    resulting_set = list()       
    for i in chosen_strs:
        if resulting_set.count(i[position]) == 0:#curr_l != i[position] or curr_l == '':
            resulting_set.append(i[position])
    return resulting_set
def get_row(row, board):
    return ''.join(board[row])
    
def get_column(curr_puzzle, column, board):
    global num_rows
    result = ''
    for row in range(num_rows[curr_puzzle]):
        result += board[row][column]
    return result
# Finds coordinate for the column vector
def get_coordinate(row,num_rows):
    return num_rows - row - 1
    
def solve_cell(curr_puzzle, row, column, board):
    global rows
    global columns
    
    print 'dealing with \'{}\' and \'{}\' regex'.format(rows[curr_puzzle][row], columns[curr_puzzle][column])
    # All the options for the row
    current_row = get_row(row, board)
    print 'current row is {}'.format(current_row)
    
    #letters_I = get_letters(rows[row],2,row,'~~')
    print 'at position {} for \'{}\' regex possible options are:'.format(column, rows[curr_puzzle][row])
    letters_I = get_letters(rows[curr_puzzle][row], len(current_row), column, current_row)
    print letters_I
    print '-'*70
    # All the options for the column
    current_column = get_column(curr_puzzle,column, board)
    print 'current column is {}'.format(current_column)  
    print 'at position {} for {} regex possible options are:'.format(row, columns[curr_puzzle][column])
    #letters_II = get_letters(columns[column],2,column,'~~')
    letters_II = get_letters(columns[curr_puzzle][column],len(current_column),row, current_column)
    print letters_II
    print '-'*70
    print 'Possible options are:'   
    # Get the difference between two sets
    print get_difference(letters_I, letters_II)
    # Return 
    return get_difference(letters_I, letters_II)

def get_cell(row, column, board):
    return board[row][column]

def read_file(file_name):
    global num_rows
    global num_columns
    global num_empty_cells
    global num_puzzles
    f = open(file_name, 'r')
    
    while True:
        testline = f.readline()
        if len(testline) ==0:
            break # EOF
        numbers = re.findall('\d+', testline)
        num_columns.append(int(numbers[0]))
        num_rows.append(int(numbers[1]))
        num_empty_cells.append(num_rows[num_puzzles]*num_columns[num_puzzles])
        print 'Board of size {}x{} with {} empty cells'.format(num_columns[num_puzzles], num_rows[num_puzzles], num_empty_cells[num_puzzles])
        rows[num_puzzles] = list()
        columns[num_puzzles] = list()
        for i in range(num_columns[num_puzzles]):
            columns[num_puzzles].append(f.readline().rstrip())
        for i in range(num_rows[num_puzzles]):
            rows[num_puzzles].append(f.readline().rstrip())
            
        print columns[num_puzzles]
        print rows[num_puzzles]
        num_puzzles += 1
    print 'total number of puzzles downloaded {}'.format(num_puzzles)

def save_solved_boards(file_name):
    f = open(file_name, 'w')
    for board_ind in range(len(solved_boards)):
        curr_board = solved_boards[board_ind]
        f.write('solution to problem ' + str(board_ind) + '\n')
        for row in range(len(curr_board)):
            for column in range(len(curr_board[row])):
                f.write(curr_board[row][column] + ' ')
            f.write('\n')
        f.write('\n')
    f.close()
    
# Intermediate level:
#rows = ['CAT|FOR|FAT', 'RY|TY\\-','[TOWEL]*']
#columns = ['.(.)\\1','.*[WAY]+','[RAM].[OH]']

#rows = ['[DEF][MNO]*', '[^DJNU]P[ABC]','[ICAN]*']
#columns = ['[JUNDT]*','APA|OPI|OLK','(NA|FE|HE)[CV]']

#rows = ['[RUNT]*', 'O.*[HAT]','(.)DO\\1']
#columns = ['[^NRU](NO|ON)','(D|FU|UF)+','(FO|A|R)*','(N|A)*']

#rows = ['[RUNT]*', 'O.*[HAT]','(.)DO\\1']
#columns = ['[^NRU](NO|ON)','(D|FU|UF)+','(FO|A|R)*','(N|A)*']

# Experienced level: 
#rows = ['[RUNT]*', 'O.*[HAT]','(.)DO\\1']
#columns = ['[^NRU](NO|ON)','(D|FU|UF)+','(FO|A|R)*','(N|A)*']

file_name = 'Experienced'
read_file(file_name + '.txt')

for curr_puzzle in range(num_puzzles):
    board = [['~' for x in xrange(num_columns[curr_puzzle])] for y in xrange(num_rows[curr_puzzle])]
    print board
    nrows = num_rows[curr_puzzle]
    ncolumns = num_columns[curr_puzzle]
    nempty_cells = num_empty_cells[curr_puzzle]
    limitting_num = 10000
    
    while nempty_cells:
        for row in range(nrows):
            for column in range(ncolumns):
                if get_cell(row, column, board) != '~':
                    print 'row {} and column {} = {}'.format(row, column, get_cell(row, column, board))
                    continue
                #print 'considering row {} and column {}'.format(row, column)
                options = solve_cell(curr_puzzle, row, column, board)
                if len(options) == 1:
                    board[row][column] = options[0]
                    nempty_cells -= 1
                    print 'empty cells left {}'.format(nempty_cells)
                    if not nempty_cells: break
                print board
            if not nempty_cells: break
        limitting_num = limitting_num * 2
        print 'limitting number was increased to {}'.format(limitting_num)
    print 'final board looks like this, verify this answer:'
    for row in range(nrows):
        print board[row]  
        
    # Recording the answer:    
    solved_boards[curr_puzzle] = board
save_solved_boards(file_name + '_solutions.txt')
    
    
'''
options = solve_cell(2, 0, board)
if len(options) == 1:
    board[2][0] = options[0]
print board

options = solve_cell(1, 1, board)
if len(options) == 1:
    board[1][1] = options[0]
print board

options = solve_cell(1, 0, board)
if len(options) == 1:
    board[1][0] = options[0]
print board

# Our first move is to discover that 0,1 = E
letters_I = get_letters('(.)* \\1',2,0,'~~')
print '-'*25 + 'first chunk' + '-'*25
print letters_I

letters_II = get_letters('AN|FE|BE',2,1,'~~')
print '-'*25 + 'second chunk' + '-'*25
print letters_II
print '-'*25 + 'intersection' + '-'*25
print get_difference(letters_I, letters_II)

# Our second move would be to discover 1,1
letters_I = get_letters('AN|FE|BE',2,0, '~E')
print '-'*25 + 'first chunk' + '-'*25
print letters_I
letters_II = get_letters('(A|B|C)\\1',2,1,'~~')
print '-'*25 + 'second chunk' + '-'*25
print letters_II
print '-'*25 + 'intersection' + '-'*25
print get_difference(letters_I, letters_II)  
print '-'*50

# Our third move would be to discover 0,0
letters_I = get_letters('.*M?O.*',2,0, '~~')
print '-'*25 + 'first chunk' + '-'*25
print letters_I
letters_II = get_letters('(A|B|C)\\1',2,0,'~B')
print '-'*25 + 'second chunk' + '-'*25
print letters_II
print '-'*25 + 'intersection' + '-'*25
print get_difference(letters_I, letters_II)  
print '-'*50

# Our last move would be to discover 1,0
letters_I = get_letters('.*M?O.*',2,1, 'B~')
print '-'*25 + 'first chunk' + '-'*25
print letters_I
letters_II = get_letters('AB|OE|SK',2,0,'~E')
print '-'*25 + 'second chunk' + '-'*25
print letters_II
print '-'*25 + 'intersection' + '-'*25
print get_difference(letters_I, letters_II)  
print '-'*50
'''
