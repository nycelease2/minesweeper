#!/bin/python3

import pygame, sys, random
running = True

def gridPos(mouseposx, mouseposy):
    #convert the mouse position to list
    mouseposxLIST = [int(x) for x in str(mouseposx)]
    mouseposyLIST = [int(x) for x in str(mouseposy)]
    
    gridposition = []

    #append x grid value
    if len(mouseposxLIST) < 3:
        gridposition.append(1)
    else:
        gridposition.append(mouseposxLIST[0]+1)
    
    #append y grid value
    if len(mouseposyLIST) < 3:
        gridposition.append(1)
    else:
        gridposition.append(mouseposyLIST[0]+1)

    return gridposition


def drawGrid(height, width, blockSize, screen):
    for x in range(0, width, blockSize):
        for y in range(0, height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (30,30,30), rect, 1)

def bombGenerator(maxBombs, xLimit, yLimit):
    bombPOS = []
    while len(bombPOS) < maxBombs:
        x = random.randint(1, xLimit)
        y = random.randint(1, yLimit)
        bombPOS.append([x,y])
                
    return bombPOS

option = input("easy[1], medium[2], hard[3]: ")

if __name__ == '__main__':
    #EASY MODE
    if option == '1':
        print("gamemode is set to easy")
        #variables
        screen_WIDTH = 800
        screen_HEIGHT = 800
        
        #pygame setup
        pygame.init()
        screen = pygame.display.set_mode((screen_HEIGHT, screen_WIDTH))
        pygame.display.set_caption("Minesweeper")
        clock = pygame.time.Clock()

        bombLocations = bombGenerator(10,8,8)
        print(bombLocations)
        print(len(bombLocations))
        while running:#gameloop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos[0], event.pos[1]
                    print(f"MOUSEPOS = x: {x}, y: {y}")
                    print(gridPos(x,y))

                #drawing to the screen
                screen.fill((200,200,200))
                drawGrid(screen_HEIGHT, screen_WIDTH, 100, screen)
                pygame.display.update()

        pygame.quit()
        sys.exit()



