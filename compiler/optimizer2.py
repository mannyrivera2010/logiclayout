# -----------------------------------------------------------------------------
# optimizer.py
# Created by Ingrid Avendano 11/17/13.
# -----------------------------------------------------------------------------
# Node class and Tree made from Tokens defined in grammar module.
# -----------------------------------------------------------------------------

class Node(object):
	def __init__(self, token, pin=False, gate=False, root=False):
		self.parents = []
		self.children = []
		self.gate = gate
		self.pin = pin
		self.root = root
		self.level = 0
		self.x = 0
		self.y = 0

		if token.kind == 'LITERAL':
			if token.expr == None:
				self.expr = '0'
			else:
				self.expr = '1'
			self.weight = 1
		elif token.kind == 'ID':
			self.expr = token.expr
			self.weight = 1
		else:
			self.gate = True
			self.expr = token.kind
			self.weight = 0

	def __repr__(self):
		""" What is displayed when a node is represented. """
		return "%r" % self.expr

	def __str__(self):
		""" What is displayed when a node is represented. """
		return "%s" % str(self.expr)

	def add(self, *children):
		self.children += children

		print children
		for child in children:
			print self, child
			self.weight += child.weight
			if self not in child.parents:
				child.parents.append(self)
		print " ", self, "--->", self.weight

# -----------------------------------------------------------------------------
# Cluster and Level hold Nodes that are at the same level in AST.
# -----------------------------------------------------------------------------

class Cell(object):
	""" Cluster is a group of children of a Node. """

	def __init__(self, depth, *nodes):
		self.depth = depth
		self.nodes = list(nodes)

		# this is for determining y-axis positions
		self.y_min = 0
		self.y_max = 0

	def print_nodes(self):
		print "y depth", self.depth
		print self.nodes


class Level(object):
	""" Level to hold Nodes. """

	def __init__(self, depth):
		self.depth = depth
		self.cells = []

	def add(self, cell):
		cell.depth = len(self.cells)
		self.cells.append(cell)

	def print_level(self):
		print "x depth", self.depth
		for cell in self.cells:
			cell.print_nodes()


# -----------------------------------------------------------------------------
# Tree that holds all Nodes and has extra attributes listed about the tree.
# -----------------------------------------------------------------------------

class Tree(object):
	""" Tree of Nodes. """

	def __init__(self, root_token, expression=""):
		""" Takes a root Token from parser and converts it to Node tree. """

		self.nodes = []
		self.depth = 0
		
		# ---------------------------------------------------------------------
		# Go through Tokens and converts them to Nodes, find depth of tree.
		# ---------------------------------------------------------------------

		def convert(token, depth=1): 
			""" Organize tree of Nodes out of tokens and gives depth. """

			if token.kind == 'EQUALS':

				# asssign left Token as output pin
				new_node = Node(token.left, pin=True, root=True)
				self.nodes.append(new_node)

				# recursively go through new_node to find children
				new_child_node = convert(token.right, depth + 1)
				new_node.add(new_child_node)

			elif token.kind == 'ID' or token.kind == 'LITERAL':

				# must be an input pin
				new_node = Node(token, pin=True)
				# self.nodes.append(new_node)

				# determines depth of tree
				self.depth = depth if depth > self.depth else self.depth

			else: 
				new_node = Node(token, gate=True)

				# recursively checks for right Tokens
				if token.right:
					new_child_node = convert(token.right, depth + 1)
					new_node.add(new_child_node)
				
				# recursively checks for left Tokens
				if token.left:
					
					# OPTIMIZE PART
					# left child Token might be the same kind as root Token
					# if so, don't add the child Token, just add its children
					if token.left.kind == token.kind:
						print "@#$%^&*()*&^%$#@$%^&*()(_*&^%$#$%^&*()*&^%$#"
						new_child_node = convert(token.left, depth)
						new_node.children += new_child_node.children
					else: 
						new_child_node = convert(token.left, depth + 1)
						new_node.add(new_child_node)


				
			return new_node

		# def find_depth(node, depth=0):
		# 	""" Determines the depth of a tree based on its nodes. """
		# 	deepest_depth = depth 

		# 	# determine a cell of children nodes
		# 	if len(node.children) > 0:

		# 		for child in node.children:
		# 			new_depth = find_depth(child, depth + 1)

		# 			if new_depth > deepest_depth:
		# 				deepest_depth = new_depth

		# 		cell_num = len(self.levels[depth+1])
		# 		new_cell = Cell(cell_num, node.children)

		# 		self.levels[depth+1].add(new_cell)

		# 	# this function also sets the depth level of a node
		# 	node.level = depth

		# 	return deepest_depth

		# def find_cells(node):
		# 	""" Determine which cells each node belongs in. """

		# 	if len(node.children) > 0:

		# 		for child in node.children:
		# 		find_cells(child)

		# 	else:



			# sets the weight for node based on children
			node.weight = weight

			return list_of_nodes

		def find_base_nodes(nodes, base):
			base_nodes = []

			for node in nodes:
				if node.pin == base:
					base_nodes.append(node)




		# def find_levels(nodes, depth):
		# 	""" Determines how many nodes go into each level. """
		# 	levels = [Level(i) for i in range(depth)]

		# 	for node in nodes:
		# 		levels[node.level].append(node)

		# 	return levels

		# def find_clusters_by_level(node, levels):
		# 	""" Determines the depth of a tree based on its nodes. """
			
		# 	for child in node.children:
		# 		levels = find_clusters_by_level(child, levels)

		# 	# this should not be an okay way to do this
		# 	if node.level == 0:
		# 		levels[0] = [[node],]
		# 		levels[1].append(node.children)
		# 	else:
		# 		if not node.pin:
		# 			levels[node.level+1].append(node.children)
		# 	return levels

		# ---------------------------------------------------------------------

		self.expr 			= expression
		self.root 			= convert(root_token)
		self.levels 		= [[] for i in range(self.depth)]

		# find_cells()

		# self.nodes 			= find_nodes(self.root)
		# self.nonterminals 	= find_base_nodes(self.nodes, True)
		# self.terminals 		= find_base_nodes(self.nodes, False)
		# self.levels 		= find_levels(self.nodes, self.depth)
		# layers				= [[] for i in range(self.depth)]
		# self.clusters 		= find_clusters_by_level(self.root, layers)
		# self.weight 		= self.root.weight

		# self.find_node_positions()
	# -------------------------------------------------------------------------

	# def find_node_positions(self):

	# 	for level in self.levels:
	# 		print len(level)
	# 		for cell in level:
		
	# 	# def x_y_positions(node):

	# 	# 	for child in node.children:



	def print_tree(self):
		""" Prints each Node in tree in tree like structure to console. """ 

		def print_node(node, indent=0):
			""" Print a node that has children. """
			print '\t'*indent, node
			indent += 1
			for child in node.children:
				print_node(child, indent)

		print_node(self.root)
		print "depth:", self.depth

	def print_nodes(self):
		""" Prints a life of each Node to console. """ 
		print "Number of nodes:", len(self.nodes)
		for node in self.nodes:
			print node, node.gate, node.weight

	def print_levels(self):
		for level in self.levels:
			print level.print_level()
		# for i in range(self.depth):
			# print i, self.levels[i]