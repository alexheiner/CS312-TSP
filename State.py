import math

class State:
    def __init__(self, mtx, plb, depth, set_cols, set_rows):
        self.state_lower_bound = None
        self.matrix = mtx
        self.parent_lower_bound = plb
        self.depth = depth
        self.set_cols = set_cols
        self.set_rows = set_rows

    def reduce_matrix(self):
        nlb = None

        self.state_lower_bound = nlb

    def reduce_first_state(self):
        min_row = self.reduce_rows()
        min_col = self.reduce_cols()
        self.state_lower_bound = min_row + min_col

    def reduce_rows(self):
        # row reduce
        for row in range(len(self.matrix)):
            min = self.get_min_row(row)
            if min > 0 and not math.inf:
                for col in range(len(self.matrix)):
                    cur_val = self.matrix[row][col]
                    self.matrix[row][col] = cur_val - min
        return min

    def reduce_cols(self):
        # column reduce
        for row in range(len(self.matrix)):
            min = self.get_min_row(row)
            if min > 0 and not math.inf:
                for col in range(len(self.matrix)):
                    cur_val = self.matrix[col][row]
                    self.matrix[col][row] = cur_val - min
        return min



    def get_min_row(self, row):
        row = self.matrix[row]
        min = math.inf
        for i in range(len(row)):
            if i < min:
                min = i
        return min

    def get_min_col(self, col):
        min = math.inf
        for i in range(len(self.matrix)):
            if self.matrix[i][col] < min:
                min = i
        return min
