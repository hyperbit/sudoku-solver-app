#!/usr/bin/python

# Copyright 2014 Justin Cano
#
# This is a simple Python program of the game Sudoku
# (http://www.sudoku.name/rules/en), developed for
# a coding challenge from the Insight Data Engineering
# Fellows Program application for the January 2015
# session.
#
# Licensed under the GNU General Public License, version 2.0
# (the "License"), this program is free software; you can
# redistribute it and/or modify it under the terms of the
# License.
#
# You should have received a copy of the License along with this
# program in the file "LICENSE". If not, you may obtain a copy of
# the License at
#	http://www.gnu.org/licenses/gpl-2.0.html
#
import csv
import copy
import sys

filename = 'bad_input.csv'#'sample_input.csv'

def loadBoard(filename):
    '''
    Loads the game board with the values contained
    in the csv file designated by filename
    Params: filename - the filename of the corresponding
            csv file to be read
    Return: board - a game board loaded with the elements
            from the csv file
    '''
    board = []
    try:
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                board.append(map(int, row))
    except ValueError:
        print "ValueError: invalid literal for int()"
        print "Make sure csv file is comma separated and"
        print "contains integers between 0-9!"
    except IOError:
        print "IOError: no such file '%s'" % filename

    return board

def isValidSudokuBoard(board):
    '''
    Checks for validity of the game board loaded from the input
    csv file. Game board must be a 9x9 element array with each
    element value between 0-9
    Params: board - the game board to be validated
    Return: True if board is valid (9x9 with elements between 0-9)
            False if board is invalid
    '''
    if board == None:
        return False
    if len(board) != 9:
        return False
    for i in range(9):
        if len(board[i]) != 9:
            return False
        for j in range(9):
            if board[i][j] < 0 or board[i][j] > 9:
                return False


    return True


def printBoard(board):
    '''
    Prints the contents of the game board in a human readable
    format
    Params: board - the game board to be printed
    '''
    if not isValidSudokuBoard(board):
        print "Board is not a Sudoku board!"
        return

    print '_' * (len(board)-1) * 3
    for i in range(len(board)):
        print '|',
        for j in range(len(board)):
            print board[i][j],
            if (j+1) % 3 == 0:
                print '|',
        print
        if (i+1) % 3 == 0:
            print '_' * (len(board)-1) * 3

def boardRow(board, rowIndex):
    '''
    Returns an array of board elements at row rowIndex
    '''
    return board[rowIndex]

def boardCol(board, colIndex):
    '''
    Returns an array of board elements at column colIndex
    '''
    return [row[colIndex] for row in board]

def boardRegion(board, i, j):
    '''
    Returns an array of board elements in the same region
    as board[i][j]
    '''
    region = []
    region += board[i/3*3][j/3*3:j/3*3+3]
    region += board[i/3*3+1][j/3*3:j/3*3+3]
    region += board[i/3*3+2][j/3*3:j/3*3+3]
    return region

def isSafeToAssign(board, row, col, num):
    '''
    Returns True if it is safe to assign board[row][col] to num
    e.g. returns True if there is no other num in the same board
    row, column, or region
    '''
    return not (num in boardRow(board, row) or num in boardCol(board, col) or num in boardRegion(board, row, col))

def findNextUnassignedCell(board):
    '''
    Returns the row and column indices of the block that has the value of 0 (unassigned)
    '''
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                return row, col

    # Return (-1, -1) if board is full
    return -1, -1


def isSolution(board):
    '''
    Checks to see if board is a valid sudoku solution
    '''
    solution = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if len(board) != 9:
        return False

    # Check rows:
    for row in board:
        if sorted(row) != solution:
            return False

    # Check cols:
    for j in range(9):
        col = boardCol(board, j)
        if sorted(col) != solution:
            return False

    # Check regions:
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            region = boardRegion(board, i, j)
            if sorted(region) != solution:
                return False

    # Board is solved!
    return True

def solveSudoku(board):
    '''
    Solves the given sudoku board using the backtrack method
    Params: board - the sudoku game board to be solved
    Return: solution - the solved game board as a board
    '''
    row, col = findNextUnassignedCell(board)

    if row < 0 or col < 0:
        return board

    for num in range(1,10):
        if isSafeToAssign(board, row, col, num):
            board[row][col] = num

            solution = solveSudoku(board)
            if solution != None:
                return solution

            board[row][col] = 0

    return None

def outputToCSV(board):
    '''
    Outputs the game board to a csv file
    Params: board - the game board to output to csv
    Return: returns nothing, but creates a csv file
            of the board to the current directory
    '''
    with open('solution.csv', 'w') as solution:
        for row in board:
            solution.write(','.join(map(str,row))+'\n')

def printNoInputMessage():
    print "Invalid input!"
    print "Usage: python sudoku.py <filename.csv>"

def printBadInputMessage():
    print
    print "Invalid input!"
    print """CSV file should be a 9x9 comma separated integer grid,
with each integer between 0-9 (0 represents blanks), e.g.,

0,3,5,2,9,0,8,6,4
0,8,2,4,1,0,7,0,3
7,6,4,3,8,0,0,9,0
2,1,8,7,3,9,0,4,0
0,0,0,8,0,4,2,3,0
0,4,3,0,5,2,9,7,0
4,0,6,5,7,1,0,0,9
3,5,9,0,2,8,4,1,7
8,0,0,9,0,0,5,2,6
"""

def main():
    board = []

    if len(sys.argv) != 2:
        printNoInputMessage()
        return

    filename = sys.argv[1]
    board = loadBoard(filename)

    if not isValidSudokuBoard(board):
        printBadInputMessage()
        return

    printBoard(board)

    solution = solveSudoku(board)

    print

    if isSolution(solution):
        print "Sudoku!"
        printBoard(solution)
        outputToCSV(solution)
    else:
        print "Could not find a solution!"


if __name__ == "__main__":
    main()
