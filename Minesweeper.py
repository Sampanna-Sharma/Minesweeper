import pygame as py
from pygame.locals import *
import random


BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BOX_WIDTH = 30
NO_OF_BOMB = 10

WIDTH = 500
HEIGHT = 500
GRID_HEIGHT = 100
GRID_WIDTH = 100


class Box:
    def __init__(self, x, y, bomb=False, reveal=False):
        self.x = x
        self.y = y
        self.bomb = bomb
        self.reveal = reveal
        self.noofbomb = 0


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = []
        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append(Box(j*BOX_WIDTH+100, i*BOX_WIDTH+100))

        for i in range(NO_OF_BOMB):
            l = random.randint(0, height-1)
            k = random.randint(0, width-1)
            if self.grid[l][k].bomb:
                i -= 1
            self.grid[l][k].bomb = True

        for i in range(self.height):
            for j in range(self.width):
                for yoff in range(-1, 2):
                    for xoff in range(-1, 2):
                        k = yoff + i
                        l = xoff + j
                        if k > -1 and k < self.height and l > -1 and l < self.width:
                                    if self.grid[k][l].bomb:
                                        self.grid[i][j].noofbomb += 1

    def show(self):
        for i in range(self.height):
            for j in range(self.width):
                py.draw.rect(window, BLACK, (self.grid[i][j].x, self.grid[i][j].y, BOX_WIDTH, BOX_WIDTH), 2)

                if self.grid[i][j].reveal:
                    if self.grid[i][j].bomb:
                        py.draw.rect(window, RED, (self.grid[i][j].x, self.grid[i][j].y, BOX_WIDTH, BOX_WIDTH), 2)
                        py.draw.ellipse(window, RED, (self.grid[i][j].x, self.grid[i][j].y, BOX_WIDTH, BOX_WIDTH))
                        for o in range(self.height):
                            for p in range(self.width):
                                self.grid[o][p].reveal = True

                    else:
                        score_surf = score_font.render(str(self.grid[i][j].noofbomb), 1, (0, 0, 0))
                        score_pos = [j*BOX_WIDTH+105, i*BOX_WIDTH+100]
                        window.blit(score_surf, score_pos)
                        py.draw.rect(window, GREEN, (self.grid[i][j].x, self.grid[i][j].y, BOX_WIDTH, BOX_WIDTH), 4)

    def mouse_react(self, cordinate):
        mouse_x = cordinate[0]
        mouse_y = cordinate[1]
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j].x <= mouse_x <= self.grid[i][j].x+BOX_WIDTH and self.grid[i][j].y <= mouse_y <= self.grid[i][j].y+BOX_WIDTH:
                    self.grid[i][j].reveal = True
                    a = i
                    b = j
                    while True:
                        if self.grid[a][b].noofbomb == 0:
                            for yoff in range(-1, 2):
                                for xoff in range(-1, 2):
                                    k = yoff + a
                                    l = xoff + b
                                    if k > -1 and k < self.height and l > -1 and l < self.width:
                                        self.grid[k][l].reveal = True

                            if random.random() > 0.5:
                                a += 1
                            else:
                                b += 1

                            if a >= self.height or b >= self.width:
                                break
                        else:
                            break


if __name__ == '__main__':
    game = Grid(10, 10)

    py.init()
    window = py.display.set_mode((HEIGHT, WIDTH))

    score_font = py.font.Font(None, 50)

    while True:
        window.fill((255, 255, 255))
        for event in py.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                game.mouse_react(py.mouse.get_pos())
        game.show()
        py.display.update()
        py.display.flip()

