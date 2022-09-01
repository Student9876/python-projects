import random  # for genarating random numbers
import sys  # we will use sys.exit to exit the game
import pygame
from pygame.locals import *
# Basic pygame imports

# Global variables for the game
FPS = 40
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PATH = '/home/enzeon/Documents/python-projects/Flappy_Bird/gallery'
PLAYER = f'{PATH}/sprites/bird.png'
BACKGROUND = f'{PATH}/sprites/background.png'
PIPE = f'{PATH}/sprites/pipe.png'


# This will be the main point from where out game will start
def welcomeScreen():
    """
    Shows Welcome images on the screen
    """

    # We want to show the player bird in the middle of the screen
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height()/2)
    messagex = int(SCREENWIDTH - GAME_SPRITES['message'].get_width()/0.8)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # If user clicks in cross button, close the game
            # for keyreference in pygame http://www.pygame.org/docs/ref/key.html
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                # If the user presses space or up key, start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # This return makes run the next function
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                # Screen will not change until this fucntion is not been run
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    # Here we are receiving two lists containing measurements about pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']}
    ]
    # List of lower pipes

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # Velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        # It will blit the images continuously while the game will be running
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # This function will return true if the player is crashed
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # Check score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first pipe is about to cross to the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width = + GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    # 25 is considered as player height 
    if playery > GROUNDY -25 or playery <0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()

        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if((playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """
    Generate positions of two pipes(One bottom straight and one top rotated) for blitting on the screen
    """

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},  # Upper Pipe
        {'x': pipex, 'y': y2}  # Lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()  # Initializing all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['numbers'] = (
        pygame.image.load(f'{PATH}/sprites/0.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/1.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/2.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/3.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/4.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/5.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/6.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/7.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/8.png').convert_alpha(),
        pygame.image.load(f'{PATH}/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load(
        f'{PATH}/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        f'{PATH}/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    # Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound(f'{PATH}/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound(f'{PATH}/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound(f'{PATH}/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(f'{PATH}/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound(f'{PATH}/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    while True:
        welcomeScreen()  # Shows welcome screen to user until a button is pressed
        mainGame()  # This is the main game function
