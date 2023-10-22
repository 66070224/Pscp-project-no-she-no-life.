import pygame
import sys
import random
from button import Button

pygame.init()

WIDTH = 1500
HEIGHT = 800

pygame.display.set_caption('Mygame')
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FRAME = pygame.time.Clock()

"""PLAY"""
PLAYERHEALTH = 100
PLAYER_STAMINA = 100
DAMAGE = 25

STAMINA = True
HIT = False
OUT = 0
hello = "ASdADWQAWDAWDAWDAWD"

BG_SURFACE_LOAD = pygame.image.load("assets/map1.jpg")
BG_SURFACE = pygame.transform.scale(BG_SURFACE_LOAD, (WIDTH, HEIGHT))

PLAYER_LOAD = pygame.image.load("assets/player1.png")
PLAYER_RESCALE = pygame.transform.scale(PLAYER_LOAD, (50, 75))
PLAYER = PLAYER_RESCALE.get_rect(center=(750, 400))
DIRACTION = 'd'

PLAYER_BULLET = pygame.Surface((10, 10))
PLAYER_BULLET.fill('Red')
BULLET = False

GAME_BUFF = True
BUFF = pygame.Surface((25, 25))
BUFF.fill('Pink')
BUFF_RECT = BUFF.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))
print(BUFF_RECT)
BUFF_RESPAWN = 0
BUFFSPEED = False
BUFFSPEED_TIME = 0

MONSTER = True
MONSTER_LOAD = pygame.image.load("assets/monster.png")
MONSTER_RES = pygame.transform.scale(MONSTER_LOAD, (50, 75))
MONSTER_RECT = MONSTER_RES.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))
MONSTER_RESPAWN = 0


"""MENU"""
LOAD_PLAY_BUTTON = pygame.image.load("assets/play_button.png")
PLAY = pygame.transform.scale(LOAD_PLAY_BUTTON, (250, 100))

LOAD_MENU_BG = pygame.image.load("assets/menu_bg.png")
MENU_BG = pygame.transform.scale(LOAD_MENU_BG, (WIDTH, HEIGHT))


posX = 350
posY = 400


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():  # Playing game...
    global PLAYERHEALTH, STAMINA, HIT, PLAYER_STAMINA, DIRACTION, PLAYER_BULLET, BULLET, GAME_BUFF, BUFF_RECT, BUFF_RESPAWN, BUFFSPEED, BUFFSPEED_TIME, OUT, MONSTER, MONSTER_RECT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        key_input = pygame.key.get_pressed()
        SCREEN.blit(BG_SURFACE, (0, 0))
        if PLAYERHEALTH > 0:
            playerstep = 4
            monsterstep = 2
            bulletspeed = 20
            # if HIT:
            #     PLAYER_RESCALE.fill('Grey')
            if BUFFSPEED == True:
                playerstep *= 2
            SCREEN.blit(PLAYER_RESCALE, PLAYER)

            if PLAYERHEALTH < 100:
                player_health = pygame.Surface((PLAYERHEALTH/2, 5))
                player_health.fill('Red')
                player_health_rect = player_health.get_rect(
                    center=(PLAYER.x+24, PLAYER.y-5))
                SCREEN.blit(player_health, player_health_rect)

            if PLAYER_STAMINA < 100:
                player_stamina = pygame.Surface((PLAYER_STAMINA/2, 5))
                player_stamina.fill('Blue')
                player_stamina_rect = player_stamina.get_rect(
                    center=(PLAYER.x+24, PLAYER.y-10))
                SCREEN.blit(player_stamina, player_stamina_rect)

            if key_input[pygame.K_LSHIFT] and stamina:
                playerstep += 2
                PLAYER_STAMINA -= 0.5
                if PLAYER_STAMINA <= 10:
                    stamina = False
            else:
                if PLAYER_STAMINA <= 100:
                    PLAYER_STAMINA += 0.5
                if PLAYER_STAMINA >= 40:
                    stamina = True

            if key_input[pygame.K_w] and key_input[pygame.K_a] and PLAYER.x >= 0 and PLAYER.y >= 0:
                PLAYER.y -= playerstep*0.75
                PLAYER.x -= playerstep*0.75
                DIRACTION = 'wa'
            elif key_input[pygame.K_w] and key_input[pygame.K_d] and PLAYER.y >= 0 and PLAYER.x <= WIDTH-50:
                PLAYER.y -= playerstep*0.75
                PLAYER.x += playerstep*0.75
                DIRACTION = 'wd'
            elif key_input[pygame.K_s] and key_input[pygame.K_a] and PLAYER.y <= HEIGHT-75 and PLAYER.x >= 0:
                PLAYER.y += playerstep*0.75
                PLAYER.x -= playerstep*0.75
                DIRACTION = 'sa'
            elif key_input[pygame.K_s] and key_input[pygame.K_d] and PLAYER.y <= HEIGHT-75 and PLAYER.x <= WIDTH-50:
                PLAYER.y += playerstep*0.75
                PLAYER.x += playerstep*0.75
                DIRACTION = 'sd'
            elif key_input[pygame.K_a] and PLAYER.x >= 0:
                PLAYER.x -= playerstep
                DIRACTION = 'a'
            elif key_input[pygame.K_w] and PLAYER.y >= 0:
                PLAYER.y -= playerstep
                DIRACTION = 'w'
            elif key_input[pygame.K_d] and PLAYER.x <= WIDTH-50:
                PLAYER.x += playerstep
                DIRACTION = 'd'
            elif key_input[pygame.K_s] and PLAYER.y <= HEIGHT-75:
                PLAYER.y += playerstep
                DIRACTION = 's'
            
            if key_input[pygame.K_f] and not BULLET:
                BULLET = True
                firstdiraction = DIRACTION
                bullet_rect = PLAYER_BULLET.get_rect(center=(PLAYER.x+24, PLAYER.y+35))
                bullet_time = pygame.time.get_ticks()+1000
            if BULLET:
                if MONSTER_RECT.colliderect(bullet_rect):
                    MONSTER = False
                    MONSTER_RESPAWN = pygame.time.get_ticks()+2000
                    BULLET = False
                if pygame.time.get_ticks() >= bullet_time:
                    BULLET = False
                if firstdiraction == 'wa':
                    bullet_rect.y -= bulletspeed*0.75
                    bullet_rect.x -= bulletspeed*0.75
                elif firstdiraction == 'wd':
                    bullet_rect.y -= bulletspeed*0.75
                    bullet_rect.x += bulletspeed*0.75
                elif firstdiraction == 'sa':
                    bullet_rect.y += bulletspeed*0.75
                    bullet_rect.x -= bulletspeed*0.75
                elif firstdiraction == 'sd':
                    bullet_rect.y += bulletspeed*0.75
                    bullet_rect.x += bulletspeed*0.75
                elif firstdiraction == 'a':
                    bullet_rect.x -= bulletspeed
                elif firstdiraction == 'w':
                    bullet_rect.y -= bulletspeed
                elif firstdiraction == 'd':
                    bullet_rect.x += bulletspeed
                elif firstdiraction == 's':
                    bullet_rect.y += bulletspeed
                SCREEN.blit(PLAYER_BULLET, bullet_rect)


        if GAME_BUFF == True:
            SCREEN.blit(BUFF, BUFF_RECT)
        if pygame.time.get_ticks() >= BUFFSPEED_TIME:
            BUFFSPEED = False
        if PLAYER.colliderect(BUFF_RECT) and (GAME_BUFF == True):
            GAME_BUFF = False
            BUFFSPEED = True
            BUFFSPEED_TIME = pygame.time.get_ticks()+1500
            PLAYERHEALTH = 100
            BUFF_RESPAWN = pygame.time.get_ticks()+5000
        if not GAME_BUFF and (pygame.time.get_ticks() >= BUFF_RESPAWN):
            GAME_BUFF = True
            BUFF_RECT = BUFF.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))

        if pygame.time.get_ticks() >= OUT and HIT:
            HIT = False
        if PLAYER.colliderect(MONSTER_RECT) and (MONSTER == True) and (HIT == False):
            PLAYERHEALTH -= DAMAGE
            HIT = True
            OUT = pygame.time.get_ticks()+1500

        if MONSTER == True:
            SCREEN.blit(MONSTER_RES, MONSTER_RECT)
            if MONSTER_RECT.y > PLAYER.y and MONSTER_RECT.x > PLAYER.x:
                MONSTER_RECT.y -= monsterstep*0.75
                MONSTER_RECT.x -= monsterstep*0.75
            elif MONSTER_RECT.x < PLAYER.x and MONSTER_RECT.y > PLAYER.y:
                MONSTER_RECT.y -= monsterstep*0.75
                MONSTER_RECT.x += monsterstep*0.75
            elif MONSTER_RECT.y < PLAYER.y and MONSTER_RECT.x > PLAYER.x:
                MONSTER_RECT.y += monsterstep*0.75
                MONSTER_RECT.x -= monsterstep*0.75
            elif MONSTER_RECT.x < PLAYER.x and MONSTER_RECT.y < PLAYER.y:
                MONSTER_RECT.y += monsterstep*0.75
                MONSTER_RECT.x += monsterstep*0.75
            elif MONSTER_RECT.x < PLAYER.x:
                MONSTER_RECT.x += monsterstep
            elif MONSTER_RECT.x > PLAYER.x:
                MONSTER_RECT.x -= monsterstep
            elif MONSTER_RECT.y < PLAYER.y:
                MONSTER_RECT.y += monsterstep
            elif MONSTER_RECT.y > PLAYER.y:
                MONSTER_RECT.y -= monsterstep
        if not MONSTER and (pygame.time.get_ticks() >= MONSTER_RESPAWN):
            MONSTER = True
            MONSTER_RECT = MONSTER_RES.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))

        pygame.display.update()
        FRAME.tick(75)


def main_menu():  # Menu page
    while True:
        SCREEN.blit(MENU_BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, 120))

        PLAY_BUTTON = Button(image=PLAY, pos=(WIDTH//2, 320),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()

        pygame.display.update()


main_menu()
