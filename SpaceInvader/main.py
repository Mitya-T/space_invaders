import pygame
import random
import math

from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# -------------------------PLAYER-----------------------------------------------------


# Player
playerImg = pygame.image.load('player.png')

# starting position of player
playerX = 370
playerY = 480
playerX_change = 0

# -------------------------ENEMY-----------------------------------------------------

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 60

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))

    # starting position of ENEMY
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    # Start speed of enemy
    enemyX_change.append(3)
    enemyY_change.append(40)
# -------------------------BULLET-----------------------------------------------------

# Bullet
bulletImg = pygame.image.load('bullet.png')

# Ready - you can't see the bullet
# Fire - bullet is moving


# starting position of ENEMY
bulletX = 0
bulletY = 480
# Start speed of enemy
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('No Virus.ttf',32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('No Virus.ttf',64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (0,255,0))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER!!!", True, (0, 255, 0))

    explosion_Sound = mixer.Sound('explosion.wav')
    explosion_Sound.play()
    screen.blit(over_text, (200, 250))

# Drawing the player spaceship
def player(x, y):
    screen.blit(playerImg, (x, y))


# Drawing the enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Drawing the BULLET
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,
                (x + 16, y + 10))  # 16 and 10 are to appear at the right position of a spaceship (NOT IN THE CENTER!)


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance <= 27:
        return True
    else:
        return False


# GAME LOOP
running = True

while running:

    # Filling the screen with RGB color:
    screen.fill((255, 0, 0))
    # background image
    screen.blit(background, (0, 0))  # 0,0 - means we want to load it from top left corner of a screen

    for event in pygame.event.get():

        # To STOP the game:
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed left / right ?
        if event.type == pygame.KEYDOWN:
            print("KEYSTROKE")
            if event.key == pygame.K_LEFT:
                playerX_change = -5

                print("Left arrow pressed")
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
                print("RIGHT arrow pressed")
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    print("SPACEBAR pressed")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("Keystroke has been released")

    # Checking for bondaries of SPACESHIP
    playerX += playerX_change

    # Setting the borders for the spaceship:
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:  # 800 - 'size of spaceship'
        playerX = 768

    # ENEMY movement
    for i in range(num_of_enemies):

        # GAME OVER
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        # Setting the borders for the ENEMY:
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:  # 800 - 'size of spaceship'
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()

            bulletY = 480
            bullet_state = "ready"

            score_value += 1
            # Enemy dies and respawn!
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # A MOMENT OF DRAWING OF THE ENEMY

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement

    # If bullet reaches the end of the screen - shoot another one
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    # A MOMENT OF DRAWING OF THE SPACESHIP
    player(playerX, playerY)

    show_score(textX, textY)

    pygame.display.update()
