#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
from State import *
import heapq
import itertools



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation(ncities)
			route = []
			# Now build the route using the random permutation
			for i in range(ncities):
				route.append(cities[perm[i]])
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

# size 15 diff hard seed 20 path: D, H, J, E, I, M, N, G, K, C, F, B, A, L, O

# check size 40 starting index of 8 and random sead of 918, no outgoing edges??

	def greedy(self,time_allowance=60.0):
		results = {}
		path = []
		cities = self._scenario.getCities()

		visited = set()
		start_index = random.randint(0, len(cities) - 1)
		#start_index = 2

		index = start_index
		# path.append(cities[index])
		# visited.add(cities[index])
		start_time = time.time()
		found_path = False
		valid_path = False
		shortest_edge = 0
		while not found_path:# and time.time()-start_time < time_allowance:
			if shortest_edge is not np.inf:
				curr_city = cities[index]
				path.append(cities[index])
				visited.add(cities[index])
			else:
				found_path = True
				break
			shortest_edge = np.inf
			if len(cities) == len(visited):
				city = cities[start_index]
				final_edge = curr_city.costTo(city)
				if final_edge is not np.inf:
					valid_path = True
				found_path = True
				break
			for city in cities:
				if city._name is not curr_city._name and not visited.__contains__(city):
					edge = curr_city.costTo(city)
					if edge is not np.inf:
						if shortest_edge == np.inf:
							shortest_edge = edge
							index = city._index

						elif edge < shortest_edge:
							shortest_edge = edge
							index = city._index

		end_time = time.time()
		if not found_path:
			results['cost'] = math.inf
			results['time'] = end_time - start_time
			results['count'] = 0
			results['soln'] = None
			results['max'] = None
			results['total'] = None
			results['pruned'] = None
			return results
		elif found_path and valid_path:
			bssf = TSPSolution(path)
			cost = bssf.cost
			results['cost'] = bssf.cost
			results['time'] = end_time - start_time
			results['count'] = 1
			results['soln'] = bssf
			results['max'] = None
			results['total'] = None
			results['pruned'] = None
			return results
		elif not valid_path and found_path:
			return self.greedy()


	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
		
	def branchAndBound( self, time_allowance=60.0 ):
		cities = self._scenario.getCities()
		matrix = [[math.inf for x in range(len(cities))] for y in range(len(cities))]
		bssf = self.greedy()['cost']
		for i in range(len(cities)):
			for j in range(len(cities)):
				if i == j:
					continue
				else:
					cityi = cities[i]
					cityj = cities[j]
					matrix[i][j] = cityi.costTo(cityj)

		initial_state = State(matrix, None)
		initial_state.reduce_first_state()

		start_city = cities[random.randint(0, len(cities) - 1)]

		initial_state.add_set_rows(start_city._index)
		initial_state.add_path_set(start_city._index)
		initial_state.add_path_arr(start_city._index)
		temp_set = initial_state.get_path_set()
		self.create_states(cities, initial_state, temp_set)

		print('hello')

	def create_states(self, cities, parent_state, city_set):
		for city in cities:
			if not city_set.__contains__(city._index):
				new_state = State(None, parent_state)
				new_state.reduce_matrix(city._index)


	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
		
	def fancy( self,time_allowance=60.0 ):
		pass
		



