import math
import copy

class State:
    set_rows = set()
    set_cols = set()
    path = []
    path_set = set()

    def __init__(self, mtx, parent_state):
        if parent_state is None:
            self.parent_lower_bound = None
            self.matrix = mtx
            self.depth = 0
            self.state_lower_bound = 0
        else:
            self.parent_state = parent_state
            self.matrix = copy.deepcopy(parent_state.matrix)
            self.depth = self.parent_state.depth + 1
            self.parent_lower_bound = self.parent_state.state_lower_bound

    def reduce_matrix(self, to_city_ind):
        # block off column of city you are potentially going to
        # block off row of city you are at
        # set inverse to infinity

        # set rows and columns to infinity
        parent_city_ind = self.path[len(self.path) - 1]
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                if row == parent_city_ind or col == to_city_ind:
                    self.matrix[row][col] = math.inf
                elif col == parent_city_ind and row == to_city_ind:
                    self.matrix[row][col] = math.inf

        min_row = self.reduce_rows()
        min_col = self.reduce_cols(to_city_ind)
        self.state_lower_bound = min_row + min_col

    def reduce_first_state(self):
        min_row = self.reduce_rows()
        min_col = self.reduce_cols()
        self.state_lower_bound = min_row + min_col

    def reduce_rows(self):
        # row reduce
        total_change = 0
        for row in range(len(self.matrix)):
            if not self.set_rows.__contains__(row):
                min = self.get_min_row(row)
                if min > 0 and min != math.inf:
                    for col in range(len(self.matrix)):
                        cur_val = self.matrix[row][col]
                        self.matrix[row][col] = cur_val - min
                total_change += min
        return total_change

    def reduce_cols(self, colTo = -1):
        # column reduce
        total_change = 0
        can_get_min = True
        for row in range(len(self.matrix)):
            if colTo == -1:
                can_get_min = True
            elif self.set_cols.__contains__(row) or row is colTo:
                can_get_min = False
            if can_get_min:
                min = self.get_min_col(row)
                if min > 0 and min != math.inf:
                    for col in range(len(self.matrix)):
                        cur_val = self.matrix[col][row]
                        self.matrix[col][row] = cur_val - min
                total_change += min
            can_get_min = True
        return total_change

    def get_min_row(self, row):
        row = self.matrix[row]
        min = math.inf
        for i in range(len(row)):
            num = row[i]
            if num == 0:
                return num
            elif num < min:
                min = num
        return min

    def get_min_col(self, col):
        min = math.inf
        for i in range(len(self.matrix)):
            num = self.matrix[i][col]
            if num == 0:
                return num
            elif num < min:
                min = num
        return min

    def add_set_rows(self, index):
        self.set_rows.add(index)

    def get_path_set(self):
        return self.path_set

    def add_path_set(self, city_ind):
        self.path_set.add(city_ind)

    def add_path_arr(self, city_ind):
        self.path.append(city_ind)
