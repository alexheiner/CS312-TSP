import math
import copy


class State:

    def __init__(self, mtx, parent_state, city_ind, cities):
        if parent_state is None:
            self.parent_lower_bound = None
            self.matrix = mtx
            self.depth = 0
            self.state_lower_bound = 0
            self.set_rows = set()
            self.set_cols = set()
            self.path = [cities[city_ind]]
            self.path_set = {city_ind}
            self.to_city_ind = city_ind
        else:
            self.parent_state = parent_state
            self.matrix = copy.deepcopy(parent_state.matrix)
            self.depth = self.parent_state.depth + 1
            self.state_lower_bound = 0
            self.parent_lower_bound = self.parent_state.state_lower_bound
            self.set_rows = copy.deepcopy(parent_state.set_rows)
            self.set_cols = copy.deepcopy(parent_state.set_cols)
            self.path = copy.deepcopy(parent_state.path)
            self.path.append(cities[city_ind])
            self.path_set = copy.deepcopy(parent_state.path_set)
            self.path_set.add(city_ind)
            self.from_city_ind = parent_state.to_city_ind
            self.to_city_ind = city_ind

    def reduce_matrix(self):
        # block off column of city you are potentially going to
        # block off row of city you are at
        # set inverse to infinity
        self.state_lower_bound += self.matrix[self.from_city_ind][self.to_city_ind]
        # set rows and columns to infinity
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                if row == self.from_city_ind or col == self.to_city_ind:
                    self.matrix[row][col] = math.inf
                elif col == self.from_city_ind and row == self.to_city_ind:
                    self.matrix[row][col] = math.inf

        min_row = self.reduce_rows()
        min_col = self.reduce_cols(self.to_city_ind)
        self.state_lower_bound += min_row + min_col + self.parent_state.state_lower_bound


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

    def reduce_cols(self, colTo=-1):
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

    def get_key(self):
        return self.state_lower_bound * 2 / self.depth

    # when a state with same lower bound and depth as another state on the queue, heapq.heappush
    # will compare the state objects using this function
    # __lt__ will select one to be placed 'ahead' of the other in the queue
    def __lt__(self, other):
        return True
