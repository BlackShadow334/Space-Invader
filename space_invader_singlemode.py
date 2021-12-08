import pygame
from pygame.locals import *
from pygame import mixer
import random
import math

pygame.init()

INNER_WIDTH = 800
INNER_HEIGHT = 600
SHIP_SPEED = 5
COLOR = {
    "black": (0, 0, 0),
    "green": (72, 217, 113),
    "red": (217, 81, 72),
    "white": (195, 214, 200),
    "blue": (89, 199, 227),
}
screen = pygame.display.set_mode((800, 600))

icon = pygame.image.load("z_assets/icon1.png")
ship1_img = pygame.image.load("z_assets/ship1.png")
bullet1_img = pygame.image.load("z_assets/gullet1.png")
background_img = pygame.image.load("z_assets/gackground.jpg")
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)


mixer.music.load("z_assets/music.ogg")
bullet1_sound = mixer.Sound("z_assets/lazer1.ogg")
ouch1 = mixer.Sound("z_assets/ouch1.ogg")
boom = mixer.Sound("z_assets/goom.ogg")
gameover = mixer.Sound("z_assets/gameover.ogg")
mixer.music.play(-1)
over_sound_status = "on"


ship1 = {"x": 50, "y": INNER_HEIGHT - (50 + 64), "dx": 0, "dy": 0}
ship1_status = "fine"
enemys = []
enemy_img = []
enemy_no = 100

for i in range(enemy_no):
    enemys.append(
        {
            "x": random.randint(10, (INNER_WIDTH - 64) - 10),
            "y": random.randint(10, (INNER_HEIGHT / 3)),
            "dx": random.choice((-3, 3)),
            "dy": 48,
        }
    )
    enemy_img.append(
        # pygame.image.load("z_assets\enemy1.png")
        pygame.image.load("z_assets/enemy1.png")
    )

bullet_speed = 10
bullet1_state = "ready"
bullet1 = {
    "x": -1000,
    "y": -1000,
    "dx": 0,
    "dy": bullet_speed,
}


def bullet1_fire(x, y):
    global bullet1_state
    bullet1_state = "fire"
    bullet1["x"] = x + 16
    bullet1["y"] = y
    screen.blit(bullet1_img, (bullet1["x"], bullet1["y"]))


def is_bullet_collision(x1, y1, x2, y2):
    dist = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    if dist - bullet_speed <= 32:
        return True
    else:
        return False


def is_enemy_collision(x1, y1, x2, y2):
    """enemy with ship colliosion cheak """
    dist = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    if dist <= 64:
        return True
    else:
        return False


player1_name = "Ben10"

font_over = pygame.font.Font("z_assets/Politik Bold.otf", 50)
font_result = pygame.font.Font("z_assets/Politik Bold.otf", 30)
font1 = pygame.font.Font("z_assets/Politik.otf", 20)
font2 = pygame.font.Font("z_assets/Politik.otf", 18)
font3 = pygame.font.Font("z_assets/Politik Bold.otf", 25)
font4 = pygame.font.Font("z_assets/Politik Bold.otf", 18)
font_space = pygame.font.Font("z_assets/Politik Bold.otf", 70)
score1 = 0
health1 = 3
# for score and health
def show_score(score1, health1):
    score1_text = font1.render(player1_name + " : " + str(score1), True, COLOR["white"])
    health1_text = font2.render("health : " + str(health1), True, COLOR["green"])
    screen.blit(score1_text, (20, 20))
    screen.blit(health1_text, (20, 45))


def show_over(score1):
    over_text = font_over.render("GAME OVER", True, COLOR["red"])
    screen.blit(over_text, (265, 250))

    last_score_text1 = font4.render(
        player1_name + " score : " + str(score1), True, COLOR["white"],
    )
    screen.blit(last_score_text1, (320, 380))
    again_text = font3.render("press ENTER to PLAY AGAIN", True, COLOR["green"])
    quit_text = font4.render("To exit : press BACKSPACE", True, COLOR["red"])
    space_text = font_space.render("space invader", True, COLOR["blue"])

    screen.blit(again_text, (239, 450))
    screen.blit(quit_text, (285, 500))
    screen.blit(space_text, (190, 120))


running = True
enemy_no = 5

while running:
    # screen.fill((32, 32, 32))
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        # for quitting
        if event.type == pygame.QUIT:
            running = False
        # (for keydown) CONTROLS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_END:
                running = False
            # for button control SHIP 1 (for keydown)
            if event.key == pygame.K_LEFT:
                ship1["dx"] = -SHIP_SPEED
            if event.key == pygame.K_RIGHT:
                ship1["dx"] = SHIP_SPEED
            if event.key == pygame.K_UP:
                ship1["dy"] = -SHIP_SPEED
            if event.key == pygame.K_DOWN:
                ship1["dy"] = SHIP_SPEED
            if event.key == pygame.K_SPACE:
                if bullet1_state == "ready":
                    bullet1_fire(ship1["x"], ship1["y"])
                    bullet1_sound.play()

        # (keyup) CONTROLS
        if event.type == pygame.KEYUP:
            # for button control SHIP 1 (for keyup)
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ship1["dx"] = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                ship1["dy"] = 0
            # controls after game over for restart
            if ship1_status == "out":
                if event.key == pygame.K_RETURN:
                    health1 = 3
                    ship1_status = "fine"
                    score1 = 0
                    enemy_no = 5
                    bullet_speed = 10
                    ship1["x"] = 50
                    ship1["y"] = INNER_HEIGHT - (50 + 64)
                    over_sound_status = "off"
                    for j in range(enemy_no):
                        enemys[j]["x"] = random.randint(10, (INNER_WIDTH - 64) - 10)
                        enemys[j]["y"] = random.randint(10, (INNER_HEIGHT / 3))
    # restricting from waall
    # ship1 wall restriction
    if ship1["x"] <= 0:
        ship1["x"] = 0
    if ship1["x"] >= INNER_WIDTH - 64:
        ship1["x"] = INNER_WIDTH - 64
    if ship1["y"] <= 0:
        ship1["y"] = 0
    if ship1["y"] >= INNER_HEIGHT - 64:
        ship1["y"] = INNER_HEIGHT - 64

    # boundry reaction for enemy1
    for i in range(enemy_no):
        enemys[i]["x"] += enemys[i]["dx"]
        if enemys[i]["x"] <= 0:
            enemys[i]["dx"] = -enemys[i]["dx"]
            enemys[i]["y"] += enemys[i]["dy"]
        if enemys[i]["x"] >= INNER_WIDTH - 64:
            enemys[i]["dx"] = -enemys[i]["dx"]
            enemys[i]["y"] += enemys[i]["dy"]
        # COLLISION
        # bullet1 collision   (with enemy)
        if is_bullet_collision(
            bullet1["x"], bullet1["y"], enemys[i]["x"], enemys[i]["y"]
        ):
            boom.play()
            bullet1_state = "ready"
            bullet1["x"] = -1000
            bullet1["y"] = -1000
            score1 += 1
            enemys[i]["x"] = random.randint(10, (INNER_WIDTH - 64) - 10)
            enemys[i]["y"] = random.randint(10, (INNER_HEIGHT / 3))
        # enemy and below wall (bottom) reaction
        if enemys[i]["y"] >= INNER_HEIGHT - 64 - 10:
            enemys[i]["x"] = random.randint(10, (INNER_WIDTH - 64) - 10)
            enemys[i]["y"] = random.randint(10, (INNER_HEIGHT / 3))
        # enemy and ship collision
        # enemy with ship1
        if is_enemy_collision(ship1["x"], ship1["y"], enemys[i]["x"], enemys[i]["y"]):
            enemys[i]["x"] = random.randint(10, (INNER_WIDTH - 64) - 10)
            enemys[i]["y"] = random.randint(10, (INNER_HEIGHT / 3))
            health1 += -1
            ouch1.play()
        # speeding enemy ...
        # if score1 != 0:
        # if int(score1 % 50) == 0:
        if enemys[i]["dx"] >= 0:
            enemys[i]["dx"] = int(score1 / 50) + 3
        if enemys[i]["dx"] <= 0:
            enemys[i]["dx"] = -(int(score1 / 50) + 3)

        screen.blit(enemy_img[i], (enemys[i]["x"], enemys[i]["y"]))

    # bullet1 movement
    if bullet1_state == "fire":
        bullet1["y"] += -bullet1["dy"]
        screen.blit(bullet1_img, (bullet1["x"], bullet1["y"]))
    if bullet1["y"] <= 0:
        bullet1_state = "ready"
        bullet1["y"] = 0
    # ship 1 dissappear
    if health1 <= 0:
        health1 = 0
        bullet1["x"] = -1000
        bullet1["y"] = -1000
        ship1["x"] = -1000
        ship1["y"] = -1000
        ship1_status = "out"
    # for game over
    if ship1_status == "out":
        show_over(score1)
        if over_sound_status == "on":
            gameover.play()
            over_sound_status = "off"
            # controls after game over is above (ONKEYUP)

    # level up
    if score1 != 0:
        if int(score1 % 10) == 0:
            enemy_no = int(score1 / 10 + 5)
        if enemy_no >= 100:
            enemy_no = 100
    # bullet speed up
    # bullet 1 speef up
    if int(score1 % 10) == 0:
        bullet1["dy"] = int(score1 / 10) + bullet_speed

    ship1["x"] += ship1["dx"]
    ship1["y"] += ship1["dy"]

    screen.blit(ship1_img, (ship1["x"], ship1["y"]))
    show_score(score1, health1)
    pygame.display.update()
pygame.quit()
