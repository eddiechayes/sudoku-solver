from app import app
from flask import render_template, request, redirect, url_for
import sudoku

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/solved', methods=['POST'])
def solved():
	data = request.form
	puzzle, fixedCells = formatPuzzle(data)
	board, result = solvePuzzle(puzzle)
	if result:
		return render_template("solved.html", solution=board.cells, fixedCells=fixedCells)
	return render_template("unsolvable.html")

def formatPuzzle(puzzle):
	'''Changes the puzzle from an ImmutableMultiDict to a 2D array'''
	puzzleArray = [[0 for j in range(9)] for i in range(9)]
	index = 0
	for value in puzzle.values():
		if value != '':
			puzzleArray[index // 9][index % 9] = int(value)
		index += 1
	fixedCells = [[True if puzzleArray[i][j] != 0 else False for j in range(9)] for i in range(9)]
	return puzzleArray, fixedCells

def solvePuzzle(puzzle):
	'''Solves the puzzle. Returns true if successful and false otherwise.'''
	board = sudoku.Board(puzzle)
	result = board.solve()
	return board, result
