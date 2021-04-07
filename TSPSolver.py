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
		self.solution_found = 0
		self.total_pruned = 0
		self.states_created = 0
		self.max_queue = 0
		results = {}
		cities = self._scenario.getCities()
		self.queue = []
		heapq.heapify(self.queue)
		matrix = [[math.inf for x in range(len(cities))] for y in range(len(cities))]
		self.bssf = self.greedy()['soln']
		for i in range(len(cities)):
			for j in range(len(cities)):
				if i == j:
					continue
				else:
					cityi = cities[i]
					cityj = cities[j]
					matrix[i][j] = cityi.costTo(cityj)

		self.start_index = random.randint(0, len(cities) - 1)
		initial_state = State(matrix, None, self.start_index, cities)
		initial_state.reduce_first_state()

		heapq.heappush(self.queue, (0, initial_state))
		start_time = time.time()
		while len(self.queue) != 0 and time.time()-start_time < time_allowance:
			if len(self.queue) > self.max_queue:
				self.max_queue = len(self.queue)

			key, parent_state = heapq.heappop(self.queue)

			if parent_state.state_lower_bound < self.bssf.cost:
				self.create_states(cities, parent_state)

		end_time = time.time()

		results['cost'] = self.bssf.cost
		results['time'] = end_time - start_time
		results['count'] = self.solution_found
		results['soln'] = self.bssf
		results['max'] = self.max_queue
		results['total'] = self.states_created
		results['pruned'] = self.total_pruned
		return results

	def create_states(self, cities, parent_state):
		if len(parent_state.path_set) == len(cities):
			last_city = parent_state.path[-1]
			start_city = cities[self.start_index]
			if last_city.costTo(start_city) is not np.inf:
				solution = TSPSolution(parent_state.path)
				if solution.cost < self.bssf.cost:
					self.bssf = solution
			else:
				return
			self.prune()
		else:
			for city in cities:
				if not parent_state.path_set.__contains__(city._index):
					new_state = State(None, parent_state, city._index, cities)
					new_state.reduce_matrix()
					self.states_created += 1
					if new_state.state_lower_bound < self.bssf.cost:
						# put it on the queue
						#new_state.add_path_set(city._index)
						key = new_state.get_key()
						heapq.heappush(self.queue, (key, new_state))

	def prune(self):
		for tuple in self.queue:
			key, state = tuple
			if state.state_lower_bound <= self.bssf.cost:
				self.queue.remove(tuple)
				self.total_pruned += 1
		self.solution_found += 1



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
		



