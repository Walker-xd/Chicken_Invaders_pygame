import pygame
import sys
from random import randint

def music():
    pygame.mixer.music.load('sound/background.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


def main():
    pygame.init()

    game_font = pygame.font.SysFont("arial", 30)

    laser_sound = pygame.mixer.Sound('sound/laser.wav')                             #Sounds
    hit_sound = pygame.mixer.Sound('sound/hit.wav')
    game_over_sound = pygame.mixer.Sound('sound/game_over.wav')
    explode_sound = pygame.mixer.Sound('sound/explode.wav')
    explode_sound.set_volume(0.5)
    pygame.mixer.Sound('sound/start.wav').play()

    screen_wight, screen_height = 1280, 720  #1280, 720 1920, 1080
    screen = pygame.display.set_mode((screen_wight, screen_height))
    background = pygame.image.load('image/background1.png').convert()

    pygame.display.set_caption('Chicken Invaders')
    space_ship_image = pygame.image.load('image/space_ship.png')
    ship_width, ship_height = space_ship_image.get_size()
    ship_x, ship_y = screen_wight / 2 - ship_width / 2, screen_height - ship_height
    ship_move_left, ship_move_right = False, False
    ship_step = 10

    laser_image = pygame.image.load('image/laser.png')
    laser_width, laser_height = laser_image.get_size()
    launched_lasers = []
    laser_step = 10

    chicken_image = pygame.image.load('image/chicken.png')
    chicken_width, chicken_height = chicken_image.get_size()
    chicken_x, chicken_y = randint(0, screen_wight - chicken_width), 0
    chicken_step = 1.1

    game_score = 0
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT or (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE):
                sys.exit()

            if i.type == pygame.KEYDOWN:                                        # Pressing Key
                if i.key == pygame.K_a:
                    ship_move_left = True
                if i.key == pygame.K_d:
                    ship_move_right = True
                if i.key == pygame.K_SPACE:
                    laser_sound.play()
                    laser_x, laser_y = ship_x + ship_width / 2 - laser_width / 2, ship_y - ship_height / 2
                    launched_lasers.append([laser_x,laser_y])

            if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                laser_sound.play()
                laser_x, laser_y = ship_x + ship_width / 2 - laser_width / 2, ship_y - ship_height / 2
                launched_lasers.append([laser_x, laser_y])
            if i.type == pygame.KEYUP:                                              #Unpressing Key
                if i.key == pygame.K_a:
                    ship_move_left = False
                if i.key == pygame.K_d:
                    ship_move_right = False



        if ship_move_left and ship_x >= 0:                                          #Ship movement
            ship_x -= ship_step
        if ship_move_right and ship_x <= screen_wight - ship_width:
            ship_x += ship_step

        chicken_y += chicken_step                                                   #Chicken movement

        for laser in launched_lasers[:]:                                             #Laser movement
            laser[1] -= laser_step
            if laser[1] + laser_height < 0:
                launched_lasers.remove(laser)
            if laser[1] < chicken_y + chicken_height and chicken_x < laser[0] < chicken_x + chicken_width:
                launched_lasers.remove(laser)
                hit_sound.play()
                game_score += 1
                chicken_x, chicken_y = randint(0, screen_wight - chicken_width), 0
                if chicken_step < 3.5:
                    chicken_step += 0.2


        screen.blit(background, (0, 0))
        screen.blit(space_ship_image, (ship_x, ship_y))
        screen.blit(chicken_image, (chicken_x, chicken_y))
        for laser in launched_lasers:
            screen.blit(laser_image, (laser[0],laser[1]))
        score_text = game_font.render(f"SCORE: {game_score}", True, 'white')
        screen.blit(score_text, (screen_wight - 200, 10))
        pygame.display.update()

        pygame.time.Clock().tick(120)  #FPS_lock

        if chicken_y + chicken_height > ship_y:
            game_over_text = game_font.render(f"Game Over", True, 'white')
            game_over_rectangle = game_over_text.get_rect()
            game_over_rectangle.center = (screen_wight / 2, screen_height / 2)
            screen.blit(game_over_text, game_over_rectangle)
            screen.blit(score_text, (game_over_rectangle.centerx - score_text.get_width() // 2,game_over_rectangle.bottom +10))
            pygame.display.update()
            #explode_sound.play()
            game_over_sound.play()
            pygame.time.wait(3000)
            return

pygame.init()
music()
while True:
    main()