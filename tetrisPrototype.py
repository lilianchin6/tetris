# hw6c.py
# Lilian Chin + lschin + section B
# partner: Sebastian Guerrero + sguerrer
# TETRIS!
######################################################################
# Place your autograded solutions below here
######################################################################

import math
import string
import random
import eventBasedAnimation

#initiates Tetris
def tetrisInitFn(data):
    data.aboutText = data.windowTitle = "Tetris"
    # make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in xrange(data.rows)]
    data.tetrisPieces = tetrisPieces()
    data.tetrisPieceColors = [ "red", "yellow", "magenta", 
                               "pink", "cyan", "green", "orange" ]
    newFallingPiece(data)
    data.isGameOver = False
    data.score = 0

#Seven "standard" pieces (tetrominoes)
def tetrisPieces():
    iPiece = [[ True,  True,  True,  True]]
    jPiece = [[ True, False, False ],[ True, True,  True]]
    lPiece = [[ False, False, True],[ True,  True,  True]]
    oPiece = [[ True, True],[ True, True]]
    sPiece = [[ False, True, True],[ True,  True, False ]]
    tPiece = [[ False, True, False ],[ True,  True, True]]
    zPiece = [[ True,  True, False ],[ False, True, True]]
    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    return tetrisPieces

# from course notes:
# http://www.cs.cmu.edu/~112/notes/notes-event-based-animations.html#2dGridDemo
def getCellBounds(row, col, data):
    # aka "modelToView"
    # data includes rows, cols, width, height, and margin
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

#moves the piece in whatever direction the player tells it to
def moveFallingPiece(data, drow, dcol):
    originalRow, originalCol = data.fallingPieceRow, data.fallingPieceCol
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    #change it back to original if not allowed
    if fallingPieceIsLegal(data) == False:
        data.fallingPieceRow, data.fallingPieceCol = originalRow, originalCol
        return False
    return True

#rotates the falling piece
def rotateFallingPiece(data):
    originalPiece, newPiece = data.fallingPiece, []
    originalRow, originalCol = data.fallingPieceRow, data.fallingPieceCol
    #oldPieceRows is height in number of rows
    #oldPieceCols is width in number of columns 
    oldPieceRows = len(data.fallingPiece)
    oldPieceCols = len(data.fallingPiece[0])
    #new row is old column
    #new column is old row 
    newPieceRows = len(data.fallingPiece[0])
    newPieceCols = len(data.fallingPiece)
    oldCenterRow = originalRow + oldPieceRows/2
    oldCenterCol = originalCol + oldPieceCols/2
    for row in range(newPieceRows-1, -1, -1):
        newPiece.append([])
        for col in range(newPieceCols):
            newPiece[-1].append(originalPiece[col][row])
    #making changes, then will check if legal after
    #changing the old center row to new center row
    data.fallingPieceRow = oldCenterRow - newPieceRows/2
    #changing the old center column to new center column
    data.fallingPieceCol = oldCenterCol - newPieceCols/2
    data.fallingPiece = newPiece
    #change it back to original if not allowed
    if fallingPieceIsLegal(data) == False:
        oldCenterRow = originalRow + oldPieceRows/2
        oldCenterCol = originalCol + oldPieceCols/2 
        data.fallingPieceRow, data.fallingPieceCol = originalRow, originalCol
        data.fallingPiece = originalPiece

#checks if falling piece is legal
def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                #checks if too far up or down
                if (data.fallingPieceRow < 0 or data.fallingPieceRow +
                    len(data.fallingPiece) > len(data.board)):
                    return False
                #checks if too far to the left or right
                elif (data.fallingPieceCol < 0 or data.fallingPieceCol + 
                    len(data.fallingPiece[0]) > len(data.board[0])):
                    return False  
                #checks if the new piece is still on blank
                elif (data.board[data.fallingPieceRow+row]
                      [data.fallingPieceCol+col] != data.emptyColor):
                    return False
    return True


#sets a new piece at the top center
def newFallingPiece(data):
    numOfPieces = (len(data.tetrisPieces)-1)
    fallingPieceIndex = random.randint(0, numOfPieces)
    data.fallingPiece = data.tetrisPieces[fallingPieceIndex]
    data.fallingPieceColor = data.tetrisPieceColors[fallingPieceIndex]
    #height and width of falling piece
    fallingPieceRows = len(data.fallingPiece)
    fallingPieceCols = len(data.fallingPiece[0])
    #row and column of falling piece
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols/2 - fallingPieceCols/2

#implements the piece to the board once it's finished falling
def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True: 
                newRow = row+data.fallingPieceRow    
                newCol = col+data.fallingPieceCol
                data.board[newRow][newCol] = data.fallingPieceColor



#drops piece with a space bar
def dropPiece(data):
    while moveFallingPiece(data, 1, 0) and fallingPieceIsLegal(data):
        continue
    placeFallingPiece(data)

#remove rows if a line is full
def removeFullRows(data):
    newBoard = [([data.emptyColor] * data.cols) for row in xrange(data.rows)]
    count = 0
    newIndex = len(data.board)-1
    for oldRow in range(len(data.board)-1, -1, -1):  
        #print "old", oldRow
        #if blue is in the row, that means it's NOT full  
        #if blue is NOT in board, that means it's full
        if data.emptyColor not in data.board[oldRow]:
            count += 1 
    for newRow in range(len(data.board)-1, -1, -1):
        if data.emptyColor in data.board[newRow]:
            newBoard[newIndex] = data.board[newRow]
            newIndex -= 1
    if count != 0:
        data.board = newBoard
        data.score += (count ** 2)

#stops the game if this function is called
def gameOver(data):
    data.isGameOver = True

#draws Tetris
def tetrisDrawFn(canvas, data):
    drawGame(canvas, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    if data.isGameOver == True:
        drawGameOver(canvas, data)

#draws the orange canvas
def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)

#draws the board on top of the canvas
def drawBoard(canvas, data):
    # draw grid of cells
    for row in xrange(data.rows):
        for col in xrange(data.cols):
            drawCell(canvas, data, row, col)

#draws the score in top left corner
def drawScore(canvas, data):
    scoreX = 26
    scoreY = 12
    sFontSize = 10
    canvas.create_text(scoreX, scoreY, text = "Score: "+ str(data.score), 
                                       font = "Arial "+str(sFontSize)+ " bold",
                                       fill = data.emptyColor)
#draws the Game Over text
def drawGameOver(canvas, data):
    if data.isGameOver == True:
        fontSize = 34
        canvas.create_text(data.width/2, data.height/2, 
                           text = "Game Over!", 
                           font = "Arial " + str(fontSize)+ " bold",
                           fill = "white")

#draws the falling piece at the top
def drawFallingPiece(canvas, data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                drawFallingCell(canvas, data, 
                                row + data.fallingPieceRow, 
                                col + data.fallingPieceCol, 
                                data.fallingPieceColor)

#draws each individual cell
def drawCell(canvas, data, row, col):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=data.board[row][col])

#draws falling cell
def drawFallingCell(canvas, data, row, col, color):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)

def tetrisStepFn(data):
    if data.isGameOver == False:
        if moveFallingPiece(data, 1, 0) == False:
            if fallingPieceIsLegal(data) == True:
                placeFallingPiece(data)
                removeFullRows(data)
                newFallingPiece(data)
            if fallingPieceIsLegal(data) == False:
                print "bye"
                gameOver(data)
  
def tetrisKeyFn(event, data):
    if data.isGameOver == False:
        if event.keysym == "Up":
            rotateFallingPiece(data)
        elif event.keysym == "Down":
            moveFallingPiece(data, 1, 0) 
        elif event.keysym == "Left":
            moveFallingPiece(data, 0, -1) 
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, 1)
        elif event.keysym == "space":
            print "hello"
            dropPiece(data)
    if event.keysym == "r":
        tetrisInitFn(data) 

def playTetris():
    rows = 15
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    eventBasedAnimation.run(
        initFn=tetrisInitFn,
        keyFn = tetrisKeyFn,
        drawFn=tetrisDrawFn,
        stepFn = tetrisStepFn,
        width=width, height=height,
        rows=rows, cols=cols, margin=margin, timerDelay = 500
        )

if __name__ == '__main__':
	playTetris()

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################
from Tkinter import *
import tkSimpleDialog
import sys


