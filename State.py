import math
import copy


class State:

    def __init__(self, mtx, parent_state, city_ind, cities):
        # properties for our initial state
        if parent_state is None:
            #
            self.parent_lower_bound = None
            self.matrix = mtx
            self.depth = 1
            self.state_lower_bound = 0
            self.set_rows = set()
            self.set_cols = set()
            self.path = [cities[city_ind]]
            self.path_set = {city_ind}
            self.to_city_ind = city_ind
        # properties for states other than initial
        else:
            self.parent_state = parent_state
            # copy the parent states matrix
            self.matrix = copy.deepcopy(parent_state.matrix)

            # increment depth
            self.depth = self.parent_state.depth + 1

            # initialize lower bound to zero, will be updated in reduce_matrix()
            self.state_lower_bound = 0

            # set states parent lower bound to the parent's state lower bound
            self.parent_lower_bound = self.parent_state.state_lower_bound

            # copy rows and columns visited, and also the path from the parent
            self.set_rows = copy.deepcopy(parent_state.set_rows)
            self.set_cols = copy.deepcopy(parent_state.set_cols)
            self.path = copy.deepcopy(parent_state.path)
            self.path_set = copy.deepcopy(parent_state.path_set)

            # add current city to path set and array
            self.path.append(cities[city_ind])
            self.path_set.add(city_ind)

            # set to and from city indexes
            self.from_city_ind = parent_state.to_city_ind
            self.to_city_ind = city_ind

    def reduce_matrix(self):
        # function to reduce states other than initial state

        # add cost of from city to city we want to go to
        self.state_lower_bound += self.matrix[self.from_city_ind][self.to_city_ind]

        # block off column of city you are potentially going to
        # block off row of city you are at
        # set inverse to infinity
        # set rows and columns to infinity
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                if row == self.from_city_ind or col == self.to_city_ind:
                    self.matrix[row][col] = math.inf
                elif col == self.from_city_ind and row == self.to_city_ind:
                    self.matrix[row][col] = math.inf

        # add from city to set rows and to city to set columns so we don't reduce on these values
        self.set_rows.add(self.from_city_ind)
        self.set_cols.add(self.to_city_ind)

        # get cost of reducing rows and columns
        cost_row = self.reduce_rows()
        cost_col = self.reduce_cols(self.to_city_ind)

        # add cost of row and col to state's lower bound
        self.state_lower_bound += cost_row + cost_col + self.parent_state.state_lower_bound

    def reduce_first_state(self):
        # function to reduce the initial state

        min_row = self.reduce_rows()
        min_col = self.reduce_cols()
        self.state_lower_bound = min_row + min_col

    def reduce_rows(self):
        # row reduce
        cost_reduce = 0
        for row in range(len(self.matrix)):
            # if row is not in our set of rows get min value
            if not self.set_rows.__contains__(row):
                # get min value for a row, if it's less than infinity subtract that value from rows
                min = self.get_min_row(row)
                if min > 0 and min != math.inf:
                    for col in range(len(self.matrix)):
                        cur_val = self.matrix[row][col]
                        self.matrix[row][col] = cur_val - min
                    cost_reduce += min
        return cost_reduce

    def reduce_cols(self, colTo=-1):
        # column reduce
        cost_reduce = 0
        can_get_min = True
        for row in range(len(self.matrix)):
            # if colTo = -1 we are reducing the initial state matrix
            if colTo == -1:
                can_get_min = True
            # if we have visited col before or our row if column of city we want to go to, don't get min
            elif self.set_cols.__contains__(row) or row is colTo:
                can_get_min = False
            if can_get_min:
                # get min value for a column, if it's less than infinity subtract that value from column
                min = self.get_min_col(row)
                if min > 0 and min != math.inf:
                    for col in range(len(self.matrix)):
                        cur_val = self.matrix[col][row]
                        self.matrix[col][row] = cur_val - min
                        # increment cost to reduce
                    cost_reduce += min
            # reset can get min to true
            can_get_min = True
        # return the cost to reduce
        return cost_reduce

    def get_min_row(self, row):
        row = self.matrix[row]
        min = math.inf
        # loop through rows
        for i in range(len(row)):
            # get num and update min if it is less
            num = row[i]
            if num == 0:
                return num
            elif num < min:
                min = num
        return min

    def get_min_col(self, col):
        min = math.inf
        # loop through columns
        for i in range(len(self.matrix)):
            # get num and update min if it is less
            num = self.matrix[i][col]
            if num == 0:
                return num
            elif num < min:
                min = num
        return min

    def get_key(self):
        # key for the queue is states lower bound * 2 / 2. This helps incorporate depth and lower bound to key
        return self.state_lower_bound * 2 / self.depth

    # when a state with same lower bound and depth as another state on the queue, heapq.heappush
    # will compare the state objects using this function
    # __lt__ will select one to be placed 'ahead' of the other in the queue
    def __lt__(self, other):
        return True
