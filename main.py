import pygame
import random
import math
from pygame import mixer

# initializing the pygame
pygame.init()

# initializing the screen for our game
screen = pygame.display.set_mode((800, 800))
''' screen being a variable here 
    also setting the screen such that it has 800px height
    and 600px width '''

'''Till this step, a screen is formed but just for a fraction of second
   hence, to display it properly, we are gonna use an infinte while loop '''

# Background
background = pygame.image.load('2352.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title/Caption and Icon
'''Program for caption'''
pygame.display.set_caption("Space Invaders")
'''To import the image as icon'''
icon = pygame.image.load('PyCharm CE.png')
'''To display the set icon'''
pygame.display.set_icon(icon)

# Player1
playerImg = pygame.image.load('player1 (1).png')
playerX = 370
playerY = 600
playerX_change = 0

# Enemy

'''There are 2 states of the bullet:
   1) Ready - You can't see the bullet on the screen
   2) Fire - The bullet is currently moving'''

enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
enemyX_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien (1).png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyY_change.append(40)
    enemyX_change.append(0.5)

# Bullet
bulletImg = pygame.image.load('bullet (2).png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bulletX_change = 0
bullet_state = "ready"

# Score Text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
'''Extra fonts - dafont.com'''
textX = 10
textY = 10

# Game Over Text
game_over = pygame.font.Font('freesansbold.ttf', 256)


def show_score(x,y):
    score = font.render("Score: "+ str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def gameover_text():
    gameover = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameover, (300, 300))

def player(x, y):
    screen.blit(playerImg, (x, y))
    '''blit is for dropping the image in our game'''

def enemy(x, y, i):
    screen.blit(enemyImg[i] , (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+5, y+5))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop-Creating a screen for your game!

'''while True:
    pass'''

'''Above written function is somewhat cool,
   but the problem occuring here is that the black screen 
   just appears and it doesn't quit by its own, rather just hangs '''

running = True
while running:

    # R, G, B Background Color
    '''In it, we can update our background screen in our desired color
       combination of Primary(Red, Green, Blue) colors
       .update is quite necessary to update the changes'''
    screen.fill((0, 0, 0))

    # applying background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed, check whether right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    '''Gets the x coordinate of the bullet'''
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    #enemyX += enemyX_change

    '''Creating boundaries for player '''
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    '''Creating boundaries for enemy '''
    # Enemy Movement
    for i in range(num_of_enemies):

        if enemyY[i] > 600 :
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            gameover_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    enemyX += enemyX_change

    player(playerX, playerY)
    show_score(textX, textY)


    pygame.display.update()
