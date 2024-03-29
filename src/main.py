#!/bin/python3

from collections import Counter
import pygame, sys, random, time
running = True

def gridPos(mouseposx, mouseposy): # converts screen coordinates to game coordinates
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


def drawGrid(height, width, blockSize, screen, checkedPlaces, tiles):
    #drawing grid
    for x in range(0, width, blockSize):
        for y in range(0, height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (30,30,30), rect, 1)

    #drawing flag
    for i in flagLocations:
        screen.blit(tiles[0], i)

    #drawing numbers on grid
    for x, num in checkedPlaces.items():
        x,y = int(str(list(x)[0]-1)+'00'), int(str(list(x)[1]-1)+'00')
        if num == 0:
            screen.blit(tiles[9], (x,y))
        elif num == 1:
            screen.blit(tiles[1], (x,y))
        elif num == 2:
            screen.blit(tiles[2], (x,y))
        elif num == 3:
            screen.blit(tiles[3], (x,y))
        elif num == 4:
            screen.blit(tiles[4], (x,y))
        elif num == 5:
            screen.blit(tiles[5], (x,y))
        elif num == 6:
            screen.blit(tiles[6], (x,y))
        elif num == 7:
            screen.blit(tiles[7], (x,y))
        elif num == 8:
            screen.blit(tiles[8], (x,y))




def bombGenerator(maxBombs, xLimit, yLimit):
    bombPOS = []
    while len(bombPOS) < maxBombs:
        x = random.randint(1, xLimit)
        y = random.randint(1, yLimit)
        bombPOS.append([x,y])

    return bombPOS

def checkplaces(gridMousePos, gridBombs):
    placesToCheck=[]
    noOfBombs = 0
    for x in [gridMousePos[0]-1, gridMousePos[0], gridMousePos[0]+1]:
        for y in [gridMousePos[1]-1, gridMousePos[1], gridMousePos[1]+1]:
            placesToCheck.append((x,y))

    #checking for bombs
    for i in placesToCheck:
        try:
            if gridBombs[i] == 1:
                noOfBombs += 1
        except KeyError:
            pass
    return noOfBombs

def checkIfWon(flagLocations, gridBombs):
    gridbombers = {}
    flagLocationsGrid = {}
    checker = 0
    # making a only bombs dictionary
    for key, value in gridBombs.items():
        if value == 1:
            gridbombers[key] = 1

    #converting the key in flagLocations from world coordinates to game coordinates
    for key, value in flagLocations.items():
        flagLocationsGrid[tuple(gridPos(key[0], key[1]))] = 1

    #checking if the player has won
    if len(flagLocationsGrid)  != len(gridbombers):
        return False

    for key, value in gridbombers.items():
        if key not in flagLocationsGrid or flagLocationsGrid[key] != value:
            return False

    for key, value in flagLocationsGrid.items():
        if key not in gridbombers or gridbombers[key] != value:
            return False

    return True

option = input("easy[1], medium[2], hard[3]: ")

if __name__ == '__main__':
    #tiles
    zero = pygame.image.load('../assets/0.png')
    one = pygame.image.load('../assets/1.png')
    two = pygame.image.load('../assets/2.png')
    three = pygame.image.load('../assets/3.png')
    four = pygame.image.load('../assets/4.png')
    five = pygame.image.load('../assets/5.png')
    six = pygame.image.load('../assets/6.png')
    seven = pygame.image.load('../assets/7.png')
    eight = pygame.image.load('../assets/8.png')
    flag = pygame.image.load('../assets/flag.png')

    tiles=[flag, one, two, three, four, five, six, seven, eight, zero]

    #EASY MODE
    if option == '1':
        print("gamemode is set to easy")
        #screen variables
        screen_WIDTH = 800
        screen_HEIGHT = 800

        #grid variables
        gridBombs = {(x, y): 0 for x in range(1,9) for y in range(1,9)}
        checkedPlaces = {}

        #flag variables
        totalFlags = 10
        flagLocations = {}

        #pygame setup
        pygame.init()
        screen = pygame.display.set_mode((screen_HEIGHT, screen_WIDTH))
        pygame.display.set_caption("Minesweeper")
        clock = pygame.time.Clock()

        for i in tiles:
            i = i.convert()

        #generate bombs
        bombLocations = bombGenerator(10,8,8)
        for i in bombLocations:
            gridBombs[tuple(i)] = 1

        start_time = time.time()
        while running:#gameloop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos[0], event.pos[1]
                    gridMousePos = gridPos(x,y)

                    if event.button == 1:
                        if gridBombs[tuple(gridMousePos)] == 1:
                            running = False

                        elif gridBombs[tuple(gridMousePos)] == 0:
                                # getting number of bombs around
                                    checkedPlaces[tuple(gridMousePos)] = checkplaces(gridMousePos, gridBombs)


                    if event.button == 3:
                        x,y = int(str(gridMousePos[0]-1)+'00'), int(str(gridMousePos[1]-1)+'00')
                        if (x,y) in flagLocations:
                            del flagLocations[(x,y)]
                            totalFlags += 1
                        elif totalFlags > 0:
                            totalFlags -= 1
                            xytuple = (x,y)
                            flagLocations[xytuple] = 1
                            if checkIfWon(flagLocations, gridBombs):
                                end_time = time.time()
                                print("you won!")
                                elapsed_time = end_time-start_time
                                if elapsed_time > 60:
                                    elapsed_time_min = elapsed_time//60
                                    elapsed_time_sec = elapsed_time%60
                                    print(f"you took {elapsed_time_min} minutes and {round(elapsed_time_sec)} seconds")
                                else:
                                    print(f"you took {round(elapsed_time)} seconds")
                                running = False
                        else:
                            print("you used all flags")
                            pass

            #drawing to the screen
            screen.fill((200,200,200))
            drawGrid(screen_HEIGHT, screen_WIDTH, 100, screen, checkedPlaces, tiles)
            pygame.display.flip()
            pygame.display.update()

        pygame.quit()
        sys.exit()

