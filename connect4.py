# this is a game called connect4
# you can play it with your friend or AI


import math
import random
import pygame


def drawGrid(color):
    s = 20
    e = 580
    d = 93
    w = 5
    for i in range(8):
        pygame.draw.line(win, color,
                         (s+d*i, s), (s+d*i, e), w)
    for i in range(7):
        pygame.draw.line(win, color,
                         (s, s+d*i), (e+d, s+d*i), w)


def nought(color, center):
    pygame.draw.circle(win, color, center, 43)


def isWinner(turn):
    streak = 0
    for i in range(6):
        for j in range(7):
            if grid[i][j] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
                if j > 2:
                    break

    for i in range(7):
        for j in range(6):
            if grid[j][i] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
                if j > 1:
                    break

    for i in range(3):
        for j in range(6-i):
            if grid[i+j][j] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
                if j+i > 1:
                    break

    for i in range(3):
        for j in range(6-i):
            if grid[j][i+j+1] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
                if i+j > 1:
                    break

    for i in range(3, 6):
        for j in range(1+i):
            if grid[i-j][j] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
    streak = 0

    for i in range(1, 4):
        for j in range(5, -2+i, -1):
            if grid[j][i+5-j] == turn:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
    return False


def isTie():
    for i in range(6):
        for j in range(7):
            if grid[i][j] == 0:
                return False
    return True


# def reset():
#     global grid, turn, undoaix, undoaiy, undox, undoy
#     undoaix, undoaiy, undox, undoy = -1, -1, -1, -1
#     for i in range(3):
#         for j in range(3):
#             grid[i][j] = " "
#     turn = random.choice([X, O])
#     play()


# def undo(x, y):
#     global grid, turn
#     grid[x][y] = " "
#     turn = opponent(turn)
#     xcord, ycord = coordinates(x, y)
#     win.blit(undopic, (xcord-10, ycord-10))
#     if turn == X:
#         drawGrid(red)
#     else:
#         drawGrid(green)
#     pygame.draw.rect(win, blue, (24+93*x, 24+93*y, 86, 86))


def endText(msg):
    global grid, turn
    for i in range(6):
        for j in range(7):
            grid[i][j] = 0

    text = pygame.font.SysFont(
        None, 100).render(msg, True, white)
    win.blit(text, [350 - 20*len(msg), 250])

    pygame.draw.rect(win, white, (680, 400, 110, 70))
    text = pygame.font.SysFont(
        None, 40).render("Play", True, black)
    win.blit(text, [700, 410])
    text = pygame.font.SysFont(
        None, 40).render("Again!", True, black)
    win.blit(text, [690, 440])

    pygame.draw.rect(win, white, (680, 500, 110, 70))
    text = pygame.font.SysFont(
        None, 40).render("Main", True, black)
    win.blit(text, [700, 510])
    text = pygame.font.SysFont(
        None, 40).render("Menu", True, black)
    win.blit(text, [700, 540])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 680 <= mx <= 790 and 400 <= my <= 470:
                    play()
                elif 680 <= mx <= 790 and 500 <= my <= 570:
                    main()
        pygame.display.update()
        Clock.tick(fps)


def minimaxPro(alpha, beta, isMaximizing):
    global grid
    if isWinner(turn):
        return 1
    if isWinner(3-turn):
        return -1
    if isTie():
        return 0
    if isMaximizing:
        bestScore = -math.inf
        for j in range(7):
            for i in range(5, -1, -1):
                if not grid[i][j]:
                    grid[i][j] = turn
                    score = minimaxPro(alpha, beta, False)
                    grid[i][j] = 0
                    bestScore = max(score, bestScore)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore = math.inf
        for j in range(7):
            for i in range(5, -1, -1):
                if not grid[i][j]:
                    grid[i][j] = 3-turn
                    score = minimaxPro(alpha, beta, True)
                    grid[i][j] = 0
                    bestScore = min(score, bestScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore


def AI():
    global grid, turn
    bestScore = -math.inf
    x = 0
    for j in range(7):
        for i in range(5, -1, -1):
            if not grid[i][j]:
                grid[i][j] = turn
                score = minimaxPro(-math.inf, math.inf, False)
                grid[i][j] = 0
                if score > bestScore:
                    bestScore = score
                    x = j
    for i in range(5, -1, -1):
        if not grid[i][x]:
            grid[i][x] = turn
            for j in range(6):
                if turn == 1:
                    nought(red, (67+93*x, 67+93*j))
                else:
                    nought(green, (67+93*x, 67+93*j))
                pygame.display.update()
                if i == j:
                    break
                pygame.time.delay(50)
                pygame.draw.rect(
                    win, blue, (24+93*x, 24+93*j, 86, 86))
            if isWinner(turn):
                endText("AI WIN!")
            elif isTie():
                endText("TIE")
            turn = 3-turn
            if turn == 1:
                drawGrid(red)
            else:
                drawGrid(green)
            break


def play():
    global turn, grid
    win.fill(blue)
    if turn == 1:
        drawGrid(red)
    else:
        drawGrid(green)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x = (mx-20)//93
                if 0 <= x <= 6:
                    for i in range(5, -1, -1):
                        if not grid[i][x]:
                            grid[i][x] = turn
                            for j in range(6):
                                if turn == 1:
                                    nought(red, (67+93*x, 67+93*j))
                                else:
                                    nought(green, (67+93*x, 67+93*j))
                                pygame.display.update()
                                if i == j:
                                    break
                                pygame.time.delay(50)
                                pygame.draw.rect(
                                    win, blue, (24+93*x, 24+93*j, 86, 86))
                            if isWinner(turn):
                                endText("YOU WIN!")
                            elif isTie():
                                endText("TIE")
                            turn = 3-turn
                            if turn == 1:
                                drawGrid(red)
                            else:
                                drawGrid(green)
                            if level != -1:
                                AI()
                            break
        pygame.display.update()
        Clock.tick(fps)


def difficulty():
    global level
    win.fill(blue)
    text = pygame.font.SysFont(
        None, 80).render("Select Difficulty!", True, white)
    win.blit(text, [200, 60])

    pygame.draw.rect(win, white, (260, 130, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Easy", True, black)
    win.blit(text, [300, 140])

    pygame.draw.rect(win, white, (260, 200, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Medium", True, black)
    win.blit(text, [300, 210])

    pygame.draw.rect(win, white, (260, 270, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Hard", True, black)
    win.blit(text, [300, 280])

    pygame.draw.rect(win, white, (260, 340, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Impossible", True, black)
    win.blit(text, [300, 350])

    pygame.draw.rect(win, white, (260, 410, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("Main Menu", True, black)
    win.blit(text, [300, 420])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 260 <= mx <= 560 and 130 <= my <= 190:
                    level = 0
                    play()
                elif 260 <= mx <= 560 and 200 <= my <= 260:
                    level = 1
                    play()
                elif 260 <= mx <= 560 and 270 <= my <= 330:
                    level = 2
                    play()
                elif 260 <= mx <= 560 and 340 <= my <= 400:
                    level = 3
                    play()
                elif 260 <= mx <= 560 and 410 <= my <= 460:
                    main()
        pygame.display.update()
        Clock.tick(fps)


def main():
    win.fill(blue)
    text = pygame.font.SysFont(
        None, 100).render("Connect 4", True, white)
    win.blit(text, [240, 100])

    pygame.draw.rect(win, white, (260, 200, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("YOU VS FRIEND", True, black)
    win.blit(text, [275, 210])

    pygame.draw.rect(win, white, (260, 300, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("YOU VS AI", True, black)
    win.blit(text, [300, 310])

    pygame.draw.rect(win, white, (260, 400, 300, 60))
    text = pygame.font.SysFont(
        None, 50).render("EXIT!", True, black)
    win.blit(text, [330, 410])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 260 <= mx <= 560 and 200 <= my <= 260:
                    level = -1
                    play()
                elif 260 <= mx <= 560 and 300 <= my <= 360:
                    difficulty()
                elif 260 <= mx <= 560 and 400 <= my <= 460:
                    exit()
        pygame.display.update()
        Clock.tick(fps)


pygame.init()
pygame.display.set_caption("Connect 4")
win = pygame.display.set_mode((800, 600))
Clock = pygame.time.Clock()
fps = 10
black = (0, 0, 0)
white = (255, 255, 255)
red = (250, 51, 51)
green = (51, 250, 89)
blue = (0, 0, 128)


grid = [[0 for x in range(7)] for y in range(6)]
level = -1
turn = random.randint(1, 2)
main()
