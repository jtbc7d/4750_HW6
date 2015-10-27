from __future__ import generators
import types
import pprint

class CSP:

	def _init_(self, var, domain, neighbors):
		self.var = []
		self.domain = {}
		self.neighbors = {}
		curr_domains = {}

	def assign(self, var, val, assignment):
		assignment[var] = val

	def unsassign(self, var, assignment):
		if var in assignment:
			if self.curr_domains:
				self.curr_domains[var] = self.domain[var][:]

	def constraints(var, val, var2, val2):
		return var == var2 or val == val2

	def nconflicts(self, var, val, assignment):
		def conflit(var2):
			val2 = assignment.get(var2)
			return val2 != None and not self.constraints(var, val, var2, val2)
		return count_if(conflict, self.neighbors[var])

def argmin_random_tie(seq, fn):
    """Return an element with lowest fn(seq[i]) score; break ties at random.
    Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
    best_score = fn(seq[0]); n = 0
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score; n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0:
                    best = x
    return best

def backtracking(CSP):
	return recur_backtrack({}, CSP)

def recur_backtrack(assignment, csp):
	if len(assignment) == len(cps.vars):
		return assignment
	var = unassigned_variable(assignment, csp)
	for val in order_domain(var, assignment, csp):
		csp.nconflicts(var, val, assignment) == 0
		csp.assign(var, val, assignment)
		result = recur_backtrack(assignment, csp)
		if result is not None:
			return result
		csp.unassign(var, assignment)
	return None

def unassigned_variable(assignment, csp):
	unassigned = [v for v in csp.var if v not in assignment]
	return argmin_random_tie(unassigned, lambda var: -legal_vals(csp, var, assignment))

def order_domain(var, assignment, csp):
	if csp.curr_domains:
		domain = csp.curr_domains[var]
	else:
		domain = csp.domain[var][:]
	while domain:
		yield domain.pop()

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
			for column, val in enumerate(data,1):
				print(column, val)
				if(val == '1'):
					csp_neighbors.setdefault(row, []).append(column)
			print('--------------------------------')
	return csp_neighbors

length = file_len('constr.txt')


domain_one = ['a', 'b', 'c']
domain_two = ['a', 'b', 'c','d']

csp_vars = create_vars(length)
csp_domain = create_domain(domain_one, length)
csp_neighbors = find_neighbor('constr.txt')
#read_file('constr.txt')

pprint.pprint(csp_neighbors)