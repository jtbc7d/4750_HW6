from __future__ import generators
from utils import *
import search
import types

class CSP:

	def _init_(self, var, domain, neighbors):
		self.var = []
		self.domain = {}
		self.neighbors = {}
		curr_domains[] = None

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

def backtracking(CSP):
	return recur_backtrack({}, CSP)

def recur_backtrack(assignment, csp):
	if len(assignment) == len(cps.vars):
		return assignment
	var = unassigned_variable(assignment, csp)
	for val in order_domain(var, assignment, csp)
		csp.nconflicts(var, val, assignment) == 0
		csp.assign(var, val, assignment)
		result = recur_backtrack(assignment, csp)
		if result is not None:
			return result
		csp.unassign(var, assignment)
	return None

def unassigned_variable(assignment, csp):
	unassigned = [v for v in csp.var if v not in assignment]