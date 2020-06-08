import math
import random
import pygame
import time
import sys

sys.setrecursionlimit(100000)

pygame.init()
width = 700
height = 600
row = 6
column = 7
pygame.display.set_caption("Connect 4")
win = pygame.display.set_mode((width, height))
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
c = red
z = 1
grid = [[0 for x in range(column)] for y in range(row)]


def drawGrid(color, row, column):
    for i in range(1, column):
        pygame.draw.line(win, color,
                         (i * width / column, 0), (i * width / column, height))
    for i in range(1, row):
        pygame.draw.line(win, color,
                         (0, i * height / row), (width, i * height / row))


def convert(x, y):
    return [y * row // height, x * column // width]


def colorIt(color, x, y):
    pygame.draw.circle(win, color, (round(y * width / column)+50, round(x *
                                                                        height / row)+50), 50)


def isWinner(turn, x, y):
    streak = 0
    for i in range(-3, 4):
        try:
            if grid[x+i][y] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                if i > 0:
                    break
                streak = 0
        except:
            pass
    streak = 0
    for i in range(-3, 4):
        try:
            if grid[x][y+i] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                if i > 0:
                    break
                streak = 0
        except:
            pass
    streak = 0
    for i in range(-3, 4):
        try:
            if grid[x+i][y+i] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                if i > 0:
                    break
                streak = 0
        except:
            pass
    streak = 0
    for i in range(-3, 4):
        try:
            if grid[x+i][y-i] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                if i > 0:
                    break
                streak = 0
        except:
            pass

    return False


def isTie():
    for i in range(column):
        for j in range(row):
            if grid[i][j] == 0:
                return False
    return True


def minimaxPro(x, y, alpha, beta, isMaximizing):
    global grid
    if isWinner(z, x, y):
        return 1
    if isWinner(3-z, x, y):
        return -1
    if isTie():
        return 0
    if isMaximizing:
        bestScore = -math.inf
        for i in range(column):
            if grid[row - 1 - i][i] == 0:
                grid[row - 1 - i][i] == z
                score = minimaxPro(row - 1 - i, i, alpha, beta, False)
                grid[row - 1 - i][i] == 0
                bestScore = max(score, bestScore)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return bestScore
    else:
        bestScore = math.inf
        for i in range(column):
            for j in range(row):
                if grid[row - 1 - i][i] == 0:
                    grid[row - 1 - i][i] == 3-z
                    score = minimaxPro(row - 1 - i, i, alpha, beta, False)
                    grid[row - 1 - i][i] == 0
                    bestScore = min(score, bestScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore


def bestMove():
    global c, z, grid
    bestScore = -math.inf
    for i in range(column):
        if grid[row - 1 - i][i] == 0:
            grid[row - 1 - i][i] = z
            score = minimaxPro(i, j, -math.inf, math.inf, False)
            grid[i][j] = 0
            if score > bestScore:
                bestScore = score
                p = [i, j]
    grid[row - 1 - i][p[1]] = z
    for j in range(row - 1 - i):
        colorIt(c, j, p[1])
        pygame.display.update()
        time.sleep(0.05)
        colorIt(black, j, p[1])
        drawGrid(white, row, column)
        pygame.display.update()
    colorIt(c, row - 1 - i, p[1])
    pygame.display.update()
    if isWinner(z, row - 1 - i, p[1]):
        msg = pygame.font.SysFont(None, 100).render(
            "GAME OVER", True, white)
        win.blit(msg, [width//2-210, height//2-35])
        pygame.display.update()
        time.sleep(3)
        exit()
    if isTie():
        msg = pygame.font.SysFont(None, 100).render(
            "MATCH TIE!", True, white)
        win.blit(msg, [width//2-210, height//2-35])
        pygame.display.update()
        time.sleep(3)
        exit()
    c = blue
    z = 3 - z


def play(l):
    global c, z
    for i in range(row):
        if grid[row - 1 - i][l[1]] == 0:
            grid[row - 1 - i][l[1]] = z
            for j in range(row - 1 - i):
                colorIt(c, j, l[1])
                pygame.display.update()
                time.sleep(0.05)
                colorIt(black, j, l[1])
                drawGrid(white, row, column)
                pygame.display.update()
            colorIt(c, row - 1 - i, l[1])
            pygame.display.update()
            if isWinner(z, row - 1 - i, l[1]):
                msg = pygame.font.SysFont(None, 100).render(
                    "GAME OVER", True, white)
                win.blit(msg, [width//2-210, height//2-35])
                pygame.display.update()
                time.sleep(3)
                exit()
            if isTie():
                msg = pygame.font.SysFont(None, 100).render(
                    "MATCH TIE!", True, white)
                win.blit(msg, [width//2-210, height//2-35])
                pygame.display.update()
                time.sleep(3)
                exit()
            if c == red:
                c = yellow
            else:
                c = red
            z = 3 - z
            # bestMove()
            break


def main(run):
    global c
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                play(convert(mx, my))
        drawGrid(c, row, column)
        pygame.display.update()


main(True)
