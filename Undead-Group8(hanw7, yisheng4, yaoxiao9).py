import copy

# Han Wang, NetID: hanw7
# Yisheng Sun, NetID:yisheng4
# Yao Xiao, NetID: yaoxiao9

# compare two list of same length,
# if any element of list a is bigger than that of list b in same idx return true
def lcmp(a, b):
    for i in range(len(a)):
        if a[i] > b[i]:
            return True
    return False


class Board():
    # init an empty board
    # f_pos: '/' positon: [[int]]
    # b_pos: '\' positon: [[int]]
    def __init__(self, f_pos, b_pos, n):
        self.f_pos = f_pos
        self.b_pos = b_pos
        self.n = n
        self.data_ = [[' ' for i in range(n)] for i in range(n)]
        for i, j in f_pos:
            self.data_[i][j] = '/'
        for i, j in b_pos:
            self.data_[i][j] = '\\'
        self.fill_order = self.init_fill_order()
        self.paths = self.find_paths()
        self.push_idx = 0

    def clean(self):
        for i, j in self.fill_order:
            self.data_[i][j] = ' '

    # push a monster 'm' of 'gvz', acrroding to the fill_order
    def push(self, m):
        i, j = self.fill_order[self.push_idx]
        self.data_[i][j] = m
        self.push_idx += 1

    # pop a monster, acrroding to the fill_order
    def pop(self):
        i, j = self.fill_order[self.push_idx]
        self.data_[i][j] = ' '
        self.push_idx -= 1

    def init_fill_order(self):
        fill_order = []
        for i in range(self.n):
            for j in range(self.n):
                if [i, j] not in self.f_pos and [i, j] not in self.b_pos:
                    fill_order.append([i, j])
        return fill_order

    def find_paths(self):
        paths = []
        for j in range(self.n):
            paths.append(self.find_path([0, j], 1))  # U
        for j in range(self.n):
            paths.append(self.find_path([3, j], 2))  # D
        for i in range(self.n):
            paths.append(self.find_path([i, 0], 3))  # L
        for i in range(self.n):
            paths.append(self.find_path([i, 3], 4))  # R
        return paths

    def copy(self):
        return copy.deepcopy(self)

    # number of monsters seens on each paths
    def see(self):
        cnts = []
        for path in self.paths:
            cnt = 0
            seen_mirror = False
            weights = {'ghost': [0, 1], 'vampire': [1, 0], 'zombie': [1, 1], ' ': [0, 0]}
            for i, j in path:
                thing = self.data_[i][j]
                if thing == '\\' or thing == '/':
                    seen_mirror = True
                else:
                    cnt += weights[thing][seen_mirror]
            cnts.append(cnt)
        return cnts

    # fill the board with a (in)complete configuration
    def fill(self, comb):
        assert (len(comb) <= len(self.fill_order))
        idx = 0
        for i, j in self.fill_order:
            self.data_[i][j] = comb[idx]
            idx += 1
            if idx >= len(comb):
                break
        return self

    def print(self):
        print('-' * self.n)
        for row in self.data_:
            print(row)

    # direction: 1 : U, 2: D, 3: L, 4: R
    # pos: starting cordinate
    def find_path(self, pos, direction):
        path = [pos.copy()]
        b_map = [0, 3, 4, 1, 2]
        f_map = [0, 4, 3, 2, 1]
        while (0 <= pos[0] <= self.n - 1) and (0 <= pos[1] <= self.n - 1):
            seen = self.data_[pos[0]][pos[1]]
            if seen == '\\':
                direction = b_map[direction]
            elif seen == '/':
                direction = f_map[direction]
            if direction == 1:
                pos[0] += 1
            elif direction == 2:
                pos[0] -= 1
            elif direction == 3:
                pos[1] += 1
            elif direction == 4:
                pos[1] -= 1
            path.append(pos.copy())
        return path[0:len(path) - 1]


class Puzzle:
    # board, the empty board with mirrors
    # monsters : {str:int}, {n_ghost, n_vampire, n_zombie}
    # clues : [int] number of monsters seen from each window
    #    len(clues) == 4 * board.n
    def __init__(self, board: Board, monsters, clues):
        self.board = board
        self.n = board.n
        self.monsters = monsters
        self.clues = clues
        self.solutions = []

    # solve the puzzle
    def solve(self):
        num_ans_found = 0
        combs = self.all_combs()
        for comb in combs:
            board = self.board.fill(comb)
            # board.print()
            if board.see() == self.clues:
                num_ans_found += 1
                if num_ans_found <= 4:
                    board.print()
        print("This puzzle has " + str(num_ans_found) + " distinct solutions.")


    def invalid(self):
        return lcmp(self.board.see(), self.clues)

    # optimized ver. partial fill and check
    # not finished. Still has bug
    def backtrack(self):
        def backtrack_(i, monsters, total):
            self.board.print()
            if i == total:
                if self.board.see() == self.clues:
                    self.board.print()
            else:
                for m in 'gvz':
                    if monsters[m] == 0:
                        continue
                    monsters[m] -= 1
                    self.board.push(m)
                    if not self.invalid():
                        backtrack_(i + 1, monsters, total)
                    monsters[m] += 1
                    self.board.pop()

        backtrack_(0, self.monsters, sum(self.monsters.values()))

    def solve2(self):
        self.backtrack()

    def all_combs(self):
        def backtrack(combs, tmp, monsters, total):
            if len(tmp) == total:
                combs.append(tmp[:])
            else:
                for m in ['ghost', 'vampire', 'zombie']:
                    if monsters[m] == 0:
                        continue
                    monsters[m] -= 1
                    tmp.append(m)
                    backtrack(combs, tmp, monsters, total)
                    monsters[m] += 1
                    tmp.pop()

        combs = []
        backtrack(combs, [], self.monsters, sum(self.monsters.values()))
        return combs


def test1():
    dimension = 4
    f_position = [[3, 1]]
    b_position = [[0, 0], [0, 1], [2, 0], [3, 3]]
    clues = [2, 2, 4, 3, 0, 0, 4, 0, 2, 3, 1, 1, 2, 3, 3, 3]
    b = Board(f_position, b_position, dimension)

    p = Puzzle(b, {'ghost': 2, 'vampire': 4, 'zombie': 5}, clues)
    p.solve()


def test2():
    dimension = 4
    f_position = [[2, 1], [3, 1]]
    b_position = [[0, 2], [1, 0], [1, 1], [1, 3], [2, 2]]
    clues = [2, 2, 0, 1, 1, 1, 2, 3, 3, 2, 1, 1, 1, 0, 2, 2]
    b = Board(f_position, b_position, dimension)

    p = Puzzle(b, {'ghost': 2, 'vampire': 5, 'zombie': 2}, clues)
    p.solve()


if __name__ == '__main__':
    test1()
    test2()