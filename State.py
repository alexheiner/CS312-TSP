import math


class State:
    set_rows = set()

    def __init__(self, mtx, plb, depth):
        self.state_lower_bound = None
        self.matrix = mtx
        self.parent_lower_bound = plb
        self.depth = depth

    def add_set_rows(self, index):
        self.set_rows.add(index)

    def reduce_matrix(self, row, col):


        nlb = None
        self.state_lower_bound = nlb

    def reduce_first_state(self):
        min_row = self.reduce_rows()
        min_col = self.reduce_cols()
        self.state_lower_bound = min_row + min_col

    def reduce_rows(self):
        # row reduce
        total_change = 0
        for row in range(len(self.matrix)):
            min = self.get_min_row(row)
            if min > 0 and min != math.inf:
                for col in range(len(self.matrix)):
                    cur_val = self.matrix[row][col]
                    self.matrix[row][col] = cur_val - min
            total_change += min
        return total_change

    def reduce_cols(self):
        # column reduce
        total_change = 0
        for row in range(len(self.matrix)):
            min = self.get_min_col(row)
            if min > 0 and min != math.inf:
                for col in range(len(self.matrix)):
                    cur_val = self.matrix[col][row]
                    self.matrix[col][row] = cur_val - min
            total_change += min
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
