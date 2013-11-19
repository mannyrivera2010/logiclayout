# -----------------------------------------------------------------------------
# grammar.py
# Created by Ingrid Avendano 11/17/13.
#
# Node classes for boolean algebra tokens with left and right children.
# -----------------------------------------------------------------------------

# token class template
class Token(object):
	""" Basic node class for tokens. """ 
	base = False

	def __init__(self, left=None, right=None):
		""" Lets a node set its children immediately when made. """
		self.left = left
		self.right = right

	def __repr__(self):
		""" What is displayed when a token is represented. """
		return "%s(%r)" % (self.kind, self.expr)

	def __contains__(self, other):
		""" Checks if other Node is a child 'in' this Node object. """
		return True if other in [self.left, self.right] else False

	def set_left(self, child):
		""" Set left child of node. """	
		self.left(child)

	def set_right(self, child):
		""" Set right child of node. """
		self.right(child)

# -----------------------------------------------------------------------------

class Equals(Token):
	""" Equals node.  """ 
	kind = 'EQUALS'
	expr = '='

class Not(Token):
	""" Not node. """ 
	kind = 'NOT'
	expr = '~'
	right = None

	def __init__(self, child=None):
		self.left = child

class And(Token):
	""" And node. """ 
	kind = 'AND'
	expr = '*'

class Or(Token):
	""" Or node. """ 
	kind = 'OR'
	expr = '+'

class Xor(Token):
	""" Xor node. """ 
	kind = 'XOR'
	expr = '^'

class Id(Token):
	""" Id node. """ 
	kind = 'ID'

	def __init__(self, expr, child=None):
		self.expr = expr
		self.left = child
		self.right = None

		if child == None:
			self.base = True


# -----------------------------------------------------------------------------

class Literal(Token):
	""" Literal node composed of integers, binary and boolean values. """ 
	kind = 'LITERAL'
	left = None
	right = None
	base = True

	def __init__(self, expr=None):
		self.expr = expr

	def __iter__(self):
		""" iter(self): returns the value/expression of the literal node. """
		return iter(self.expr)