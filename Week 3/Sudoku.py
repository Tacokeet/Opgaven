import time


# helper function
def cross(A, B):
    # cross product of chars in string A and chars in string B
    return [a + b for a in A for b in B]


#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I
arc = {}
digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
cells = cross(rows, cols)  # for 3x3 81 cells A1..9, B1..9, C1..9, ...

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +  # 9 rows
             [cross(rows, c) for c in cols] +  # 9 cols
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])  # 9 units
# peers is a dict {cell : list of peers}
# every cell c has 20 peers p (i.e. cells that share a row, col, box)
# units['A1'] is a list of lists, and sum(units['A1'],[]) flattens this list
units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in cells)


def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


def display(grid):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
            v = grid[r + c]
            # avoid the '123456789'
            if v == '123456789':
                v = '.'
            print(''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F':
            print('-------------------')
    print()


def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))


def no_conflict(grid, c, v):
    # check if assignment is possible: value v not a value of a peer
    for p in peers[c]:
        if grid[p] == v:
            return False  # conflict
    return True


def human_solve(grid):
    check = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    to_be_filled = {}
    missing = {}
    if '123456789' not in grid.values():
        display(grid)
        return grid
    for coord in grid:
        if grid[coord] != '123456789':
            continue
        to_be_filled[coord] = []
        missing[coord] = []
        for number in peers[coord]:
            to_be_filled[coord].append((number, grid[number]))
        for x in to_be_filled[coord]:
            if x[1] == '123456789':
                continue
            if x[1] in missing[coord]:
                continue
            missing[coord].append(x[1])
        if len((set(check).difference(missing[coord]))) == 1:
            print(next(iter(set(check).difference(missing[coord]))), 'is the number for', coord)
            grid[coord] = next(iter(set(check).difference(missing[coord])))
    human_solve(grid)


def dfs(grid, empty, next):
    if '123456789' not in grid.values():
        print('im done')
        return grid
    for i in range(1, 10):
        if no_conflict(grid, empty[next], str(i)):
            grid[empty[next]] = str(i)
            next += 1
            dfs(grid, empty, next)
            if '123456789' not in grid.values():
                break
            next -= 1
            grid[empty[next]] = str('123456789')
    return grid


def make_arc_consistent(grid, c, v):
    # print(v, c, peers[c])
    for p in peers[c]:
        if p in arc:
            # print(p, arc[p])
            if v in arc[p]:
                if len(arc[p]) <= 1:
                    return False
                else:
                    arc[p].remove(v)
    # find all one values
    # print(arc)
    for o in arc:
        # print(o, len(arc[o]))
        if len(arc[o]) == 1 and o != c:
            # print(o, c)
            # print(o, arc[o])
            if not make_arc_consistent(grid, o, arc[o]):
                return False
    return True


def get_smallest_set():
    smallest_len = 9
    for a in arc:
        if smallest_len > len(arc[a]) > 1:
            smallest = a
            smallest_len = len(arc[a])
    return smallest


def test():
    t = False
    for a in arc:
        if len(arc[a]) == 1:
            t = True
        else:
            t = False
    return t


def arc_dfs(grid):
    if '123456789' not in grid.values():
        print('im done')
        print(grid)
        display(grid)
        return True
    # if test():
    #     print(grid)
    #     display(grid)
    #     return True
    s = get_smallest_set()
    for v in arc[s]:
        if no_conflict(grid, s, v):
            new_grid = grid.copy()
            new_grid[s] = v
            if make_arc_consistent(new_grid, s, v):
                if arc_dfs(new_grid):
                    return True
    return False


def solve(grid):
    check = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    to_be_filled = {}
    missing = {}
    # Uncomment this for normal dfs and then call dfs
    # empty = []
    # for coord in grid:
    #     if grid[coord] != '123456789':
    #         continue
    #     empty.append(coord)
    #
    # display(dfs(grid, empty, 0))

    # making data set for arc_dfs
    for coord in grid:
        if grid[coord] != '123456789':
            continue
        to_be_filled[coord] = []
        missing[coord] = []
        for number in peers[coord]:
            to_be_filled[coord].append((number, grid[number]))
        for x in to_be_filled[coord]:
            if x[1] == '123456789':
                continue
            if x[1] in missing[coord]:
                continue
            missing[coord].append(x[1])
        arc[coord] = set(check).difference(missing[coord])
    print(arc)
    arc_dfs(grid)
    arc.clear()
    pass


# minimum nr of clues for a unique solution is 17
slist = [None for x in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10] = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11] = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12] = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14] = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15] = '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16] = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17] = '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18] = '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19] = '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'

for i, sudo in enumerate(slist):
    print('* sudoku {0} *'.format(i))
    d = parse_string_to_dict(sudo)
    display(d)
    start_time = time.time()
    solve(d)
    end_time = time.time()
    hours, rem = divmod(end_time - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(int(hours), int(minutes), seconds))
    print()
