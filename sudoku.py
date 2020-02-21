from app import app

class Cell(object):
	'''Represents one cell in the sudoku board'''

	def __init__(self, row, col):
		'''Create an empty cell'''
		self.domain = list(range(1,10))
		self.number = 0
		self.row = row
		self.col = col

	@staticmethod
	def fixedCell(num, row, col):
		'''Create a cell with a fixed number.'''
		cell = Cell(row, col)
		cell.domain = [num]
		cell.number = num
		return cell

	def __repr__(self):
		return str(self.number)

class Board(object):
	'''Represents a 9x9 sudoku board'''

	def __init__(self, numbers):
		'''
		Create a new board.
		arguments:
		numbers -- a 9x9 2D list of ints. A zero refers to an empty cell.
		'''

		# A 2D (9x9) list of all cells on the board
		self.cells = [[0 for j in range(9)] for i in range(9)]

		# A map from square number (0-8) to all the cells in that square
		self.squares = {i:[] for i in range(9)}

		# The number of unassigned cells
		self.numUnassigned = 0

		# Populate self.cells and self.squares
		for i in range(9):
			for j in range(9):

				# Add to self.cells
				if numbers[i][j] > 0:
					self.cells[i][j] = Cell.fixedCell(numbers[i][j], i, j)
				else:
					self.numUnassigned += 1
					self.cells[i][j] = Cell(i, j)

				# Add to self.squares
				square = self.getSquare(i, j)
				self.squares[square].append(self.cells[i][j])


	def getSquare(self, row, col):
		'''Returns the square that the cell at (row, column) resides at.'''
		return ((row // 3) * 3) + (col // 3)


	def solve(self):
		'''
		Solves the sodoku board using backtracking search.
		returns -- True if successful, False otherwise
		'''

		if not self.initialFilter():
			return False
		return self.backtrackingSearch()


	def backtrackingSearch(self):
		'''
		Performs backtracking search on the sudoku board.
		returns -- True if successful, False otherwise
		'''

		# Base case: the board is solved
		if self.numUnassigned == 0:
			return True

		# Get the cell with the fewest remaining values in its domain
		cell = self.minimumRemainingValue()

		# Loop over possible values in its domain
		for num in cell.domain:

			# Assign a valid number to the cell
			cell.number = num

			# Filter based on the assignment
			filteredCells, result = self.filter(cell)

			# If that assignment violates a contraint, 
			# undo the effects of the filter and skip it
			if not result:
				self.unfilter(num, filteredCells)
				cell.number = 0
				continue

			# Recursively search
			self.numUnassigned -= 1
			result = self.backtrackingSearch()
			if result: return True

			# Remove assignment
			cell.number = 0
			self.numUnassigned += 1

			# Undo the filtering
			self.unfilter(num, filteredCells)

		# The board in its current state is unsolvable. Backtrack!
		return False
			

	def initialFilter(self):
		'''
		Prunes the values of all cells' domains based on the fixed cells in the starting board.
		returns: -- True if successful, False if not (ie, unsolvable puzzle)
		'''

		# Loop through every cell
		for i in range(9):
			for j in range(9):
				cell = self.cells[i][j]
				# If the cell has a fixed value, filter based on that cell 
				if cell.number != 0:
					if not self.filter(cell)[1]:
						# If that filtering violates a constraint, then the puzzle is unsolvable
						return False

		# Successfully filtered based on the starting board
		return True

	def filter(self, cell):
		'''
		Prunes the values of all cell's domains based on a number assignment to the argument cell.
		returns -- (filteredCells, result)
			filteredCells -- a list of all cells that had values removed from their domains
			result -- a boolean indicating whether the filter was successful or not (violates constraints)
		'''

		# A list of cells whose domains have been filtered
		filteredCells = []

		# Loop through the cell's row
		for currentCell in self.cells[cell.row]:
			# If the cell is unassigned, remove cell.number from its domain
			if currentCell.number == 0 and cell.number in currentCell.domain:
				currentCell.domain.remove(cell.number)
				filteredCells.append(currentCell)
			# If we encounter another cell with the same number, then this assignment isn't correct
			elif currentCell != cell and currentCell.number == cell.number:
				return filteredCells, False

		# Loop through the cell's column
		for i in range(9):
			currentCell = self.cells[i][cell.col]
			# If the cell is unassigned, remove cell.number from its domain
			if currentCell.number == 0 and cell.number in currentCell.domain:
				currentCell.domain.remove(cell.number)
				filteredCells.append(currentCell)
			# If we encounter another cell with the same number, then this assignment isn't correct
			elif currentCell != cell and currentCell.number == cell.number:
				return filteredCells, False

		# Loop through the cell's square
		square = self.getSquare(cell.row, cell.col)
		for currentCell in self.squares[square]:
			# If the cell is unassigned, remove cell.number from its domain
			if currentCell.number == 0 and cell.number in currentCell.domain:
				currentCell.domain.remove(cell.number)
				filteredCells.append(currentCell)
			# If we encounter another cell with the same number, then this assignment isn't correct
			elif currentCell != cell and currentCell.number == cell.number:
				return filteredCells, False

		return filteredCells, True


	def unfilter(self, num, cells):
		'''
		Undoes the effects of filtering num from the domain of cells.
		Called after backtracking to reset domains to their original state.
		'''

		# Loop through the filtered cells and add back the pruned number to their domain
		for cell in cells:
			cell.domain.append(num)


	def minimumRemainingValue(self):
		'''Returns the cell with the smallest domain.'''

		# The cell with the smallest domain so far
		smallestDomainCell = None

		# The size of that domain
		smallestDomain = 10

		# Iterate through every cell
		for i in range(9):
			for j in range(9):
				currentCell = self.cells[i][j]	
				lenDomain = len(currentCell.domain)

				# Check that it is unassigned and its domain is smaller
				if currentCell.number == 0 and lenDomain < smallestDomain:

					# Return early because this is the best we can do
					if lenDomain == 0:
						return currentCell

					# Overwrite with the new smallest cell
					smallestDomainCell = currentCell
					smallestDomain = lenDomain

		return smallestDomainCell