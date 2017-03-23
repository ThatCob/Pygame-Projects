import pygame,sys, random
from pygame.locals import *

pygame.init()

WINDOWWIDTH = 600
WINDOWHEIGHT = 400

WORLDWIDTH = 1800
WORLDHEIGHT = 400

FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)

windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
windowRect= windowSurface.get_rect()

playerWidth = 20
playerHeight = 50
jumpHeight = 10

def turnOnGravity(player,gravity):
    player.bottom += gravity

player = pygame.Rect(windowRect.centerx,windowRect.bottom - playerHeight,playerWidth,playerHeight)

def shiftWorld(shiftX):

    for plat in platforms:
        plat.left += shiftX

# variables for the platform class

platformWidth = 50
platformHeight = 10
platformCount = 0
platforms = []

# the below should contain the x,y coordinates of platforms as tuples for the first level
LEVEL1 = [(310,330), (350,280),(370,220),(450,210),(550,200),(700,220)]

class platform():
    
    def __init__(self,x,y,width,height,player,gravity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.player = player
        self.gravity = gravity
    
    def makePlat(x,y,width,height):
        plat = pygame.Rect(x,y,width,height)

        return plat

platLimit = 10
    

mainClock = pygame.time.Clock()

jumpLoopsPassed = 0
playerTimeOnPlat = 0
gravity = 9.8
gravityOn = False
playerJumping = False
moveLeft = False
moveRight = False

while True:
    gravityOn = True
        
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_j:
                playerJumping = True

            if event.key == K_a:
                moveLeft = True
                moveRight = False

            if event.key == K_d:
                moveRight = True
                moveLeft = False

        if event.type == KEYUP:
            if event.key == K_j:
                playerJumping = False

            if event.key == K_a:
                moveLeft = False

            if event.key == K_d:
                moveRight = False

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if playerJumping == True:
        pygame.time.delay(10)
        player.bottom -= 20
        jumpLoopsPassed += 1

    # this tests whether any platform collides with any point on the bottom of the player's Rect
    # if so, turns gravity off, thus preventing the call to turnOnGravity below
    for plat in platforms[:]:
        if plat.collidepoint(player.midbottom) or plat.collidepoint(player.bottomleft) or plat.collidepoint(player.bottomright):
            gravityOn = False
            playerTimeOnPlat += 1

            platPlayerIsOn = platforms.index(plat)
                       
    if player.bottom < windowRect.bottom and gravityOn == True:
        turnOnGravity(player,gravity)

    if moveLeft == True and player.left > 0:
        player.left -= 10

    if moveRight == True and player.right < WINDOWWIDTH and player.right < WORLDWIDTH:
        player.right += 10

    # this is how we implement sidescrolling
    # if player reaches a certain point on the scren, start moving EVERY OTHER OBJECT BUT THE PLAYER
    # this is what shiftWorld does
    if moveRight == True and player.right >= (WINDOWWIDTH - 200):
        diff = player.width
        shiftWorld(-diff)

    '''not sure if I want the player to be able to move back'''
    #if moveLeft == True and player.left <= (0 + 200) :
        #diff = player.width 
        #shiftWorld(diff)

        
    ''' this will prevent holding jump down indefinitely if the player is holding down the jump key, playerJumping becomes True
    BUT it also increments the jumpLoopsPassed - as soon as that hits jumpHeight, playerJumping becomes False and we can't jump any
    further'''

    # means we can regulate the height of the player's jumps through jumpLoopsPassed
    # and jumpHeight
    if playerJumping == True and jumpLoopsPassed >= jumpHeight:
        playerJumping = False
        jumpLoopsPassed = 0

    windowSurface.fill(BLACK)

    # place platforms from level 1 list
    if len(platforms) < 6:
        for i in range(len(LEVEL1)):
        #xcoordinate = random.randint(0,WORLDWIDTH - platformWidth)
        #ycoordinate = random.randint(0,WORLDHEIGHT - platformHeight)

            xcoordinate = LEVEL1[i][0]
            ycoordinate = LEVEL1[i][1]
            platforms.append(platform.makePlat(xcoordinate,ycoordinate,platformWidth,platformHeight))


    # draw all the platforms in the list to the screen
    for plat in platforms:
        pygame.draw.rect(windowSurface,BLUE,plat)

    # this turns the current platform red if the player has sat on it too long as a warning it will be removed
    # note current issue: playerTimeOnPlat increments regardless of the platform you're on
    # should only increment if I'm on one too long
    '''if playerTimeOnPlat >= 60:
        pygame.draw.rect(windowSurface,RED,platforms[platPlayerIsOn])'''

    '''if playerTimeOnPlat == 100:
        platforms.pop(platPlayerIsOn)
        playerTimeOnPlat = 0'''
        
    platformCount += 1
        
    pygame.draw.rect(windowSurface,WHITE,player)
    pygame.display.update()

    mainClock.tick(FPS)
