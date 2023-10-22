import pygame
import sys
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
MONSTER = True
GAME_BUFF = True
HIT = False
OUT = 0
hello = "ASdADWQAWDAWDAWDAWD"

BG_SURFACE_LOAD = pygame.image.load("assets/map1.jpg")
BG_SURFACE = pygame.transform.scale(BG_SURFACE_LOAD, (WIDTH, HEIGHT))

PLAYER_LOAD = pygame.image.load("assets/player1.png")
PLAYER_RESCALE = pygame.transform.scale(PLAYER_LOAD, (100, 150))
PLAYER = PLAYER_RESCALE.get_rect(center=(750, 400))

BUFF = pygame.Surface((50, 50))
BUFF.fill('Pink')
BUFF_RECT = BUFF.get_rect(center=(1000, 500))
BUFF_RESPAWN = 0

MONSTER_LOAD = pygame.image.load("assets/monster.png")
MONSTER_RES = pygame.transform.scale(MONSTER_LOAD, (100, 150))
MONSTER_RECT = MONSTER_RES.get_rect(center=(500, 100))


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
    global PLAYERHEALTH, STAMINA, HIT, PLAYER_STAMINA, GAME_BUFF, BUFF_RESPAWN, OUT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        key_input = pygame.key.get_pressed()
        print(key_input)
        SCREEN.blit(BG_SURFACE, (0, 0))
        if PLAYERHEALTH > 0:
            step = 5
            # if HIT:
            #     PLAYER_RESCALE.fill('Grey')
            # else:
            #     PLAYER_RESCALE.fill('Green')
            SCREEN.blit(PLAYER_RESCALE, PLAYER)

            if PLAYERHEALTH < 100:
                player_health = pygame.Surface((PLAYERHEALTH, 10))
                player_health.fill('Red')
                player_health_rect = player_health.get_rect(
                    center=(PLAYER.x+48, PLAYER.y-20))
                SCREEN.blit(player_health, player_health_rect)

            if PLAYER_STAMINA < 100:
                player_stamina = pygame.Surface((PLAYER_STAMINA, 10))
                player_stamina.fill('Blue')
                player_stamina_rect = player_stamina.get_rect(
                    center=(PLAYER.x+48, PLAYER.y-30))
                SCREEN.blit(player_stamina, player_stamina_rect)

            if key_input[pygame.K_LSHIFT] and stamina:
                step *= 2
                PLAYER_STAMINA -= 0.5
                if PLAYER_STAMINA <= 10:
                    stamina = False
            else:
                if PLAYER_STAMINA <= 100:
                    PLAYER_STAMINA += 0.5
                if PLAYER_STAMINA >= 40:
                    stamina = True

            if key_input[pygame.K_w] and key_input[pygame.K_a] and PLAYER.x >= 0 and PLAYER.y >= 0:
                PLAYER.y -= step*0.75
                PLAYER.x -= step*0.75
            elif key_input[pygame.K_w] and key_input[pygame.K_d] and PLAYER.y >= 0 and PLAYER.x <= WIDTH-50:
                PLAYER.y -= step*0.75
                PLAYER.x += step*0.75
            elif key_input[pygame.K_s] and key_input[pygame.K_a] and PLAYER.y <= HEIGHT-75 and PLAYER.x >= 0:
                PLAYER.y += step*0.75
                PLAYER.x -= step*0.75
            elif key_input[pygame.K_s] and key_input[pygame.K_d] and PLAYER.y <= HEIGHT-75 and PLAYER.x <= WIDTH-50:
                PLAYER.y += step*0.75
                PLAYER.x += step*0.75
            elif key_input[pygame.K_a] and PLAYER.x >= 0:
                PLAYER.x -= step
            elif key_input[pygame.K_w] and PLAYER.y >= 0:
                PLAYER.y -= step
            elif key_input[pygame.K_d] and PLAYER.x <= WIDTH-50:
                PLAYER.x += step
            elif key_input[pygame.K_s] and PLAYER.y <= HEIGHT-75:
                PLAYER.y += step

        if GAME_BUFF == True:
            SCREEN.blit(BUFF, BUFF_RECT)
        if PLAYER.colliderect(BUFF_RECT) and (GAME_BUFF == True) and (PLAYERHEALTH != 100):
            GAME_BUFF = False
            PLAYERHEALTH = 100
            BUFF_RESPAWN = pygame.time.get_ticks()+5000
        if not GAME_BUFF and (pygame.time.get_ticks() >= BUFF_RESPAWN):
            GAME_BUFF = True

        if not PLAYER.colliderect(MONSTER_RECT) and pygame.time.get_ticks() >= OUT and HIT:
            HIT = False
        if PLAYER.colliderect(MONSTER_RECT) and (MONSTER == True) and (HIT == False):
            PLAYERHEALTH -= DAMAGE
            HIT = True
            OUT = pygame.time.get_ticks()+1500

        if MONSTER == True:
            SCREEN.blit(MONSTER_RES, MONSTER_RECT)
            if MONSTER_RECT.x < PLAYER.x:
                MONSTER_RECT.x += 2.5
            elif MONSTER_RECT.x > PLAYER.x:
                MONSTER_RECT.x -= 2.5
            if MONSTER_RECT.y < PLAYER.y:
                MONSTER_RECT.y += 2.5
            elif MONSTER_RECT.y > PLAYER.y:
                MONSTER_RECT.y -= 2.5

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
