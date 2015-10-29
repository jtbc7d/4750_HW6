from __future__ import generators
import types
import pprint
import random

class CSP:

	def __init__(self, var, domain, neighbors):
		self.var = var
		self.domain = domain
		self.neighbors = neighbors
		self.curr_domains = {}

	def assign(self, var, val, assignment):
		assignment[var] = val
		if self.curr_domains:
			print("test")
			self.forward_check(var, val, assignment)

	def unassign(self, var, assignment):
		if var in assignment:
			if self.curr_domains:
				self.curr_domains[var] = self.domain[var][:]
			del assignment[var]

	def nconflicts(self, var, val, assignment):
		count = 0 
		for x in self.neighbors[var]:
			if assignment.has_key(x):
				if val == assignment.get(x):
					count +=1

	def forward_check(self, var, val, assignment):
		if self.curr_domains:
            # Restore prunings from previous value of var
			for (B, b) in self.pruned[var]:
				self.curr_domains[B].append(b)
			self.pruned[var] = []
	            # Prune any other B=b assignement that conflict with var=val
			for B in self.neighbors[var]:
				if B not in assignment:
					for b in self.curr_domains[B][:]:
						if not self.constraints(var, val, B, b):
							self.curr_domains[B].remove(b)
							self.pruned[var].append((B, b))

	def constraints(A, a, B, b):
		return A == a or B == b


def count_if(predicate, seq):
    """Count the number of elements of seq for which the predicate is true.
    >>> count_if(callable, [42, None, max, min])
    2
    """
    f = lambda count, x: count + (not not predicate(x))
    return reduce(f, seq, 0)


def argmin(seq, fn):
	best = seq[0]; best_score = fn(best)
	for x in seq:
		x_score = fn(x)
    	if x_score < best_score:
        	best, best_score = x, x_score
	return best


def backtracking(csp):
	csp.curr_domains, csp.pruned = {}, {}
	for v in csp.var:
		csp.curr_domains[v] = csp.domain[v][:]
        csp.pruned[v] = []
	return recur_backtrack({}, csp)

def recur_backtrack(assignment, csp):
	if len(assignment) == len(csp.var):
		return assignment

	var = unassigned_variable(assignment, csp)
	print("%d was selected" %var)

	for val in order_domain(var, assignment, csp):
		if csp.nconflicts(var, val, assignment) == 0:
			csp.assign(var, val, assignment)
			result = recur_backtrack(assignment, csp)
			if result is not None:
				return result
		csp.unassign(var, assignment)
	return assignment



def unassigned_variable(assignment, csp):
	mrv_val = 100
	smallest_domain = 0

	for v in csp.var:

		if v not in assignment:

			v_size = mrv_h(csp, v, assignment)
			print(v, v_size)
			if(v_size < mrv_val):
				mrv_val = v_size
				returnVal = v
			

			if(v_size == mrv_val):
				degree_new = degree_h(csp, v)
				print(v, degree_new)
				
				if(degree_new < smallest_domain):
					smallest_domain = degree_new
					returnVal = v
	print("---------------------")
	return returnVal

def order_domain(var, assignment, csp):
	if csp.curr_domains:
		domain = csp.curr_domains[var]
		#pprint.pprint(domain)
	else:
		domain = csp.domain[var][:]
		#pprint.pprint(domain)
	return domain

def legal_vals(csp, var, assignment):
	if csp.curr_domains:
		return len(csp.curr_domains[var])
	else:
		return count_if(lambda val: csp.nconflicts(var, val, assignment) == 0, 
			csp.domain[var])

def degree_h(csp, var):
	count = 0
	for l in csp.neighbors[var]:
		count +=1
	return count

def mrv_h(csp, var, assignment):
	mrv_size = len(csp.curr_domains[var])
	for x in csp.neighbors[var]:
		if assignment.has_key(x):
			for varVal in csp.curr_domains[var]:
				if varVal == assignment.get(x):
					mrv_size -= 1
	return mrv_size


def read_file(fname):
	constrData=[]
	constrFile = open(fname, 'r')
	constrData = [line.strip('\t\n\r') for line in constrFile]
	for i in constrData:
		print i
	return constrData

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
	f.close()
    return i + 1

def create_vars(length):
 	var_list = []
 	for i in range(1, length+1):
 		var_list.append(i)
 	return var_list


def create_domain(domain_set, length):
	csp_domain={}
	for key in range(1,length+1): 
		for domain in domain_set:
			csp_domain.setdefault(key, []).append(domain)
	return csp_domain

def find_neighbor(fname):
	csp_neighbors={}
	with open(fname) as f:
		for row, data in enumerate(f.readlines(),1):
			newData = data.replace('\t','').replace('\n','')
			for column, val in enumerate(newData, 1):
				if(val == '1'):
					csp_neighbors.setdefault(int(row), []).append(column)
	

	return csp_neighbors

length = file_len('constr.txt')


domain_one = ['a', 'b', 'c']
domain_two = ['a', 'b', 'c','d']

csp_vars = create_vars(length)
csp_domain = create_domain(domain_two, length)
csp_neighbors = find_neighbor('constr.txt')
#read_file('constr.txt')
result = {}
csp = CSP(csp_vars, csp_domain, csp_neighbors)
result = backtracking(csp)
pprint.pprint(result)
