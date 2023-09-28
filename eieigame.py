import pygame
pygame.init()

width = 1500
height = 800

pygame.display.set_caption('Mygame')
screen_diplay = pygame.display.set_mode((width, height))
frame = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

playerhealth = 100
playerstamina = 100
stamina = True
monster = True
game_buff = True
hit = False
out = 0
damage = 25

background_surface = pygame.Surface((width, height))
background_surface.fill('White')

player_character = pygame.Surface((50, 75))
player_rect = player_character.get_rect(center = (750, 400))

buff = pygame.Surface((50, 50))
buff.fill('Pink')
buff_rect = buff.get_rect(center = (1000, 500))

monster_character = pygame.Surface((50, 75))
monster_character.fill('Red')
monster_rect = monster_character.get_rect(center = (500, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    key_input = pygame.key.get_pressed()
    screen_diplay.blit(background_surface, (0,0))
    if playerhealth > 0:
        step = 5
        if hit:
            player_character.fill('Grey')
        else:
            player_character.fill('Green')
        screen_diplay.blit(player_character, player_rect)

        if playerhealth < 100:
            player_health = pygame.Surface((playerhealth, 10))
            player_health.fill('Red')
            player_health_rect = player_health.get_rect(center = (player_rect.x+25, player_rect.y-20))
            screen_diplay.blit(player_health, player_health_rect)

        if playerstamina < 100:
            player_stamina = pygame.Surface((playerstamina, 10))
            player_stamina.fill('Blue')
            player_stamina_rect = player_stamina.get_rect(center = (player_rect.x+25, player_rect.y-30))
            screen_diplay.blit(player_stamina, player_stamina_rect)

        if key_input[pygame.K_LSHIFT] and stamina:
            step *= 2
            playerstamina -= 0.5
            if playerstamina <= 10:
                stamina = False
        else:
            if playerstamina <= 100:
                playerstamina += 0.5
            if playerstamina >= 40:
                stamina = True

        if key_input[pygame.K_a] and player_rect.x >= 0:
            player_rect.x -= step
        if key_input[pygame.K_w] and player_rect.y >= 0:
            player_rect.y -= step
        if key_input[pygame.K_d] and player_rect.x <= width-50:
            player_rect.x += step
        if key_input[pygame.K_s] and player_rect.y <= height-75:
            player_rect.y += step

    if player_rect.colliderect(buff_rect) and (game_buff == True) and (playerhealth != 100):
        game_buff = False
        playerhealth = 100
    if game_buff == True:
        screen_diplay.blit(buff, buff_rect)

    if not player_rect.colliderect(monster_rect) and pygame.time.get_ticks() >= out and hit:
        hit = False
    if player_rect.colliderect(monster_rect) and (monster == True) and (hit == False):
        playerhealth -= damage
        hit = True
        out = pygame.time.get_ticks()+1500
    if monster == True:
        screen_diplay.blit(monster_character, monster_rect)

    pygame.display.update()
    frame.tick(75)
