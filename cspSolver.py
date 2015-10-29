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

	def unassign(self, var, assignment):
		if var in assignment:
			if self.curr_domains:
				self.curr_domains[var] = self.domain[var][:]
			del assignment[var]

	def nconflicts(self, var, val, assignment):
		count = 0 
		for x in self.neighbors[var]:
			#print("This is the var %d" %var)
			if assignment.has_key(x):
				if val == assignment.get(x):
					count +=1
		#print(count)
		return count
			


	def display(self, assignment):
		print 'CSP:', self, 'with assignment:', assignment

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best

def count_if(predicate, seq):
    """Count the number of elements of seq for which the predicate is true.
    >>> count_if(callable, [42, None, max, min])
    2
    """
    f = lambda count, x: count + (not not predicate(x))
    return reduce(f, seq, 0)

def backtracking(csp):
	csp.curr_domains, csp.pruned = {}, {}
	for v in csp.var:
		csp.curr_domains[v] = csp.domain[v][:]
        csp.pruned[v] = []
	csp = csp
	return recur_backtrack({}, csp)

def recur_backtrack(assignment, csp):
	if len(assignment) == len(csp.var):
		return assignment

	var = unassigned_variable(assignment, csp)

	for val in order_domain(var, assignment, csp):
		if csp.nconflicts(var, val, assignment) == 0:
			csp.assign(var, val, assignment)
			result = recur_backtrack(assignment, csp)
			if result is not None:
				return result
		csp.unassign(var, assignment)
	return assignment

def unassigned_variable(assignment, csp):
	"Select the variable to work on next.  Find"
	unassigned = [v for v in csp.var if v not in assignment]
	pprint.pprint(unassigned)
	return argmin(unassigned,
                     lambda var: -legal_vals(csp, var, assignment))
    

	"""def unassigned_variable(assignment, csp):
	mrv_val = 100
	
	for v in csp.var:
		if v not in assignment:
			if csp.curr_domains:
				if(len(csp.domain[v] < mrv_val)):
					mrv_val = len(csp.curr_domains[v])
					returnVal = v

				if(len(csp.domain[v] == mrv_val)):
					v = nconflicts(v, assignment.get(n), assignment)
					returnVal = nconflicts(v, assignment.get(n), assignment)
					if(returnVal < v):
						returnVal = v
			else:
				returnVal = v

	return returnVal"""

def order_domain(var, assignment, csp):
	if csp.curr_domains:
		domain = csp.curr_domains[var]
		#pprint.pprint(domain)
	else:
		domain = csp.domain[var][:]
		#pprint.pprint(domain)
	return domain

def legal_vals(cs, var, assignment):
	if csp.curr_domains:
		return len(csp.curr_domains[var])
	else:
		return count_if(lambda val: csp.nconflicts(var, val, assignment) == 0, 
			csp.domain[var])

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
csp_domain = create_domain(domain_one, length)
csp_neighbors = find_neighbor('constr.txt')
#read_file('constr.txt')
result = {}
csp = CSP(csp_vars, csp_domain, csp_neighbors)
result = backtracking(csp)
pprint.pprint(result)
