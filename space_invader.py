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
ship2_img = pygame.image.load("z_assets/ship2.png")
bullet1_img = pygame.image.load("z_assets/gullet1.png")
bullet2_img = pygame.image.load("z_assets/gullet2.png")
background_img = pygame.image.load("z_assets/gackground.jpg")
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)


mixer.music.load("z_assets/music.ogg")
bullet1_sound = mixer.Sound("z_assets/lazer1.ogg")
bullet2_sound = mixer.Sound("z_assets/lazer2.ogg")
ouch1 = mixer.Sound("z_assets/ouch1.ogg")
ouch2 = mixer.Sound("z_assets/ouch2.ogg")
boom = mixer.Sound("z_assets/goom.ogg")
gameover = mixer.Sound("z_assets/gameover.ogg")
mixer.music.play(-1)
over_sound_status = "on"


ship1 = {"x": 50, "y": INNER_HEIGHT - (50 + 64), "dx": 0, "dy": 0}
ship1_status = "fine"
ship2 = {"x": INNER_WIDTH - (50 + 64), "y": INNER_HEIGHT - (50 + 64), "dx": 0, "dy": 0}
ship2_status = "fine"
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
    enemy_img.append(pygame.image.load("z_assets/enemy1.png"))

bullet_speed = 10
bullet1 = {
    "x": -1000,
    "y": -1000,
    "dx": 0,
    "dy": bullet_speed,
}
bullet1_state = "ready"
bullet2 = {
    "x": -1000,
    "y": -1000,
    "dx": 0,
    "dy": bullet_speed,
}
bullet2_state = "ready"


def bullet1_fire(x, y):
    global bullet1_state
    bullet1_state = "fire"
    bullet1["x"] = x + 16
    bullet1["y"] = y
    screen.blit(bullet1_img, (bullet1["x"], bullet1["y"]))


def bullet2_fire(x, y):
    global bullet2_state
    bullet2_state = "fire"
    bullet2["x"] = x + 16
    bullet2["y"] = y
    screen.blit(bullet2_img, (bullet2["x"], bullet2["y"]))


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
player2_name = "Andy"

font_over = pygame.font.Font("z_assets/Politik Bold.otf", 50)
font_result = pygame.font.Font("z_assets/Politik Bold.otf", 30)
font1 = pygame.font.Font("z_assets/Politik.otf", 20)
font2 = pygame.font.Font("z_assets/Politik.otf", 18)
font3 = pygame.font.Font("z_assets/Politik Bold.otf", 25)
font4 = pygame.font.Font("z_assets/Politik Bold.otf", 18)
font_space = pygame.font.Font("z_assets/Politik Bold.otf", 70)
score1 = 0
score2 = 0
health2 = 3
health1 = 3
# for score and health
def show_score(score1, score2, health1, health2):
    score1_text = font1.render(player1_name + " : " + str(score1), True, COLOR["white"])
    score2_text = font1.render(player2_name + " : " + str(score2), True, COLOR["white"])
    health1_text = font2.render("health : " + str(health1), True, COLOR["green"])
    health2_text = font2.render("health : " + str(health2), True, COLOR["green"])
    screen.blit(score1_text, (20, 20))
    screen.blit(score2_text, ((INNER_WIDTH - 20) - 120, 20))
    screen.blit(health1_text, (20, 45))
    screen.blit(health2_text, ((INNER_WIDTH - 20) - 120, 45))


def show_over(score1, score2):
    over_text = font_over.render("GAME OVER", True, COLOR["red"])
    screen.blit(over_text, (265, 250))
    if score1 > score2:
        result_text = font_result.render(
            "winner : " + player1_name, True, COLOR["green"],
        )
        screen.blit(result_text, (290, 330))
    elif score1 < score2:
        result_text = font_result.render(
            "winner : " + player2_name, True, COLOR["green"],
        )
        screen.blit(result_text, (290, 330))
    else:
        result_text = font_result.render('Its "DRAW"', True, COLOR["white"])
        screen.blit(result_text, (325, 330))

    last_score_text1 = font4.render(
        player1_name + " score : " + str(score1), True, COLOR["white"],
    )
    last_score_text2 = font4.render(
        player2_name + " score : " + str(score2), True, COLOR["white"],
    )
    screen.blit(last_score_text1, (320, 380))
    screen.blit(last_score_text2, (320, 405))
    again_text = font3.render("press ENTER to PLAY AGAIN", True, COLOR["green"])
    quit_text = font4.render("To exit : press BACKSPACE", True, COLOR["red"])
    space_text = font_space.render("space invader", True, COLOR["blue"])

    screen.blit(again_text, (239, 450))
    screen.blit(quit_text, (285, 500))
    screen.blit(space_text, (190, 120))


max_score = 0


def get_max_score(score1, score2):
    global max_score
    if score1 > score2:
        max_score = score1
    else:
        max_score = score2
    return max_score


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
            if event.key == pygame.K_a:
                ship1["dx"] = -SHIP_SPEED
            if event.key == pygame.K_d:
                ship1["dx"] = SHIP_SPEED
            if event.key == pygame.K_w:
                ship1["dy"] = -SHIP_SPEED
            if event.key == pygame.K_s:
                ship1["dy"] = SHIP_SPEED
            if event.key == pygame.K_e:
                if bullet1_state == "ready":
                    bullet1_fire(ship1["x"], ship1["y"])
                    bullet1_sound.play()
            # for button control SHIP 2 (for keydown)
            if event.key == pygame.K_LEFT:
                ship2["dx"] = -SHIP_SPEED
            if event.key == pygame.K_RIGHT:
                ship2["dx"] = SHIP_SPEED
            if event.key == pygame.K_UP:
                ship2["dy"] = -SHIP_SPEED
            if event.key == pygame.K_DOWN:
                ship2["dy"] = SHIP_SPEED
            if event.key == pygame.K_RCTRL:
                if bullet2_state == "ready":
                    bullet2_fire(ship2["x"], ship2["y"])
                    bullet2_sound.play()
        # (keyup) CONTROLS
        if event.type == pygame.KEYUP:
            # for button control SHIP 1 (for keyup)
            if event.key == pygame.K_a or event.key == pygame.K_d:
                ship1["dx"] = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                ship1["dy"] = 0
            # for button control SHIP 2 (for keyup)
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ship2["dx"] = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                ship2["dy"] = 0
            # controls after game over for restart
            if ship1_status == "out" and ship2_status == "out":
                if event.key == pygame.K_RETURN:
                    health1 = 3
                    health2 = 3
                    ship1_status = "fine"
                    ship2_status = "fine"
                    score1 = 0
                    score2 = 0
                    enemy_no = 5
                    bullet_speed = 10
                    ship1["x"] = 50
                    ship1["y"] = INNER_HEIGHT - (50 + 64)
                    ship2["x"] = INNER_WIDTH - (50 + 64)
                    ship2["y"] = INNER_HEIGHT - (50 + 64)
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
    # ship2 wall restriction
    if ship2["x"] <= 0:
        ship2["x"] = 0
    if ship2["x"] >= INNER_WIDTH - 64:
        ship2["x"] = INNER_WIDTH - 64
    if ship2["y"] <= 0:
        ship2["y"] = 0
    if ship2["y"] >= INNER_HEIGHT - 64:
        ship2["y"] = INNER_HEIGHT - 64

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
        # bullet2 collision
        if is_bullet_collision(
            bullet2["x"], bullet2["y"], enemys[i]["x"], enemys[i]["y"]
        ):
            boom.play()
            bullet2_state = "ready"
            bullet2["x"] = -1000
            bullet2["y"] = -1000
            score2 += 1
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
        # enemy with ship2
        if is_enemy_collision(ship2["x"], ship2["y"], enemys[i]["x"], enemys[i]["y"]):
            enemys[i]["x"] = random.randint(10, (INNER_WIDTH - 64) - 10)
            enemys[i]["y"] = random.randint(10, (INNER_HEIGHT / 3))
            health2 += -1
            ouch2.play()
        # speeding enemy ...
        get_max_score(score1, score2)
        # if max_score != 0:
        if int(max_score % 50) == 0:
            if enemys[i]["dx"] >= 0:
                enemys[i]["dx"] = int(max_score / 50) + 3
            if enemys[i]["dx"] <= 0:
                enemys[i]["dx"] = -(int(max_score / 50) + 3)

        screen.blit(enemy_img[i], (enemys[i]["x"], enemys[i]["y"]))

    # bullet1 movement
    if bullet1_state == "fire":
        bullet1["y"] += -bullet1["dy"]
        screen.blit(bullet1_img, (bullet1["x"], bullet1["y"]))
    if bullet1["y"] <= 0:
        bullet1_state = "ready"
        bullet1["y"] = 0
    # bullet2 movement
    if bullet2_state == "fire":
        bullet2["y"] += -bullet2["dy"]
        screen.blit(bullet2_img, (bullet2["x"], bullet2["y"]))
    if bullet2["y"] <= 0:
        bullet2_state = "ready"
        bullet2["y"] = 0
    # ship 1 dissappear
    if health1 <= 0:
        health1 = 0
        bullet1["x"] = -1000
        bullet1["y"] = -1000
        ship1["x"] = -1000
        ship1["y"] = -1000
        ship1_status = "out"
    # ship 2 dissappear
    if health2 <= 0:
        bullet2["x"] = -1000
        bullet2["y"] = -1000
        ship2["x"] = -1000
        ship2["y"] = -1000
        ship2_status = "out"
        health2 = 0
    # for game over
    if ship1_status == "out" and ship2_status == "out":
        show_over(score1, score2)
        if over_sound_status == "on":
            gameover.play()
            over_sound_status = "off"
            # controls after game over is above (ONKEYUP)

    # level up
    get_max_score(score1, score2)
    if max_score != 0:
        if int(max_score % 10) == 0:
            enemy_no = int(max_score / 10 + 5)
        if enemy_no >= 100:
            enemy_no = 100
    # bullet speed up
    # bullet 1 speef up
    if int(score1 % 10) == 0:
        bullet1["dy"] = int(score1 / 10) + bullet_speed
    if int(score2 % 10) == 0:
        bullet2["dy"] = int(score2 / 10) + bullet_speed

    ship1["x"] += ship1["dx"]
    ship1["y"] += ship1["dy"]
    ship2["x"] += ship2["dx"]
    ship2["y"] += ship2["dy"]

    screen.blit(ship1_img, (ship1["x"], ship1["y"]))
    screen.blit(ship2_img, (ship2["x"], ship2["y"]))
    show_score(score1, score2, health1, health2)
    pygame.display.update()
pygame.quit()
