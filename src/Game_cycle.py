import pygame
import random
import numpy as np

from lib.cave.main import Cave
from lib.objects.charecter import character
from lib.objects.weapons import mele
from lib.objects.map import map
from lib.objects.map import random_spawn
from lib.animation.spritesheet_to_sprites import sheet2frames
from lib.colisions.colisions import check_mask_collision
from lib.colisions.colisions import check_ground


l=160
h=80
scaling_coeff = 10
cave = Cave()
cave.save_cave(47,l,h,1,scaling_coeff,smooth_pixels=False)  # True для гладкой карты, False(Быстрее) для пиксельной

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127,127,127)

cave = map("src\Textures\cave.png")


player = character((0,0))
random_spawn(player,cave)
weapon = mele((player.rect.x,player.rect.y))
# Группировка спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(cave)

mele_sprites = pygame.sprite.Group()
mele_sprites.add(weapon)

# Jump_flag = True

WIDTH = cave.rect.width
HEIGHT = cave.rect.height
WIDTH = 800
HEIGHT = 400
FPS = 30

background = pygame.Surface((l*scaling_coeff,h*scaling_coeff))
background.fill(GRAY)

camera_scroll_true = np.array((player.rect.x-WIDTH/2, player.rect.y-HEIGHT/2))

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cave Game")
clock = pygame.time.Clock()


UpHeld = False
DownHeld = False
RightHeld = False
LeftHeld = False
MiningRight = False
MiningLeft = False 

# Цикл игры
running = True
while running:
    all_sprites.update()
    
    MiningRight = False
    MiningLeft = False 
    UpHeld = False
    Vx_flag = False
    Vy_flag = False
    # Отрисовка
    
    # Без камеры
    # screen.blit(player.image, (player.rect.x-player.animate.x_offset, player.rect.y-player.animate.y_offset))
    # screen.blit(cave.image, cave.rect.topleft)
    # С камерой
    camera_scroll_true += (np.array((player.rect.x-WIDTH/2, player.rect.y-HEIGHT/2)) - camera_scroll_true)/20
    camera_scroll = np.modf(camera_scroll_true)[1]
    cave_camera_pos = -camera_scroll
    player_camera_pos = np.array((player.rect.x-player.animate.x_offset, player.rect.y -player.animate.y_offset)) - camera_scroll
    
    
    screen.fill(GRAY)
    screen.blit(background,cave_camera_pos)
    screen.blit(player.image, player_camera_pos)
    screen.blit(cave.image, cave_camera_pos)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # Проверка тыков 
        elif event.type == pygame.KEYDOWN:
            
            if event.key ==pygame.K_a:  
                LeftHeld = True
            elif event.key == pygame.K_d:
                RightHeld = True
            elif event.key == pygame.K_SPACE:
                UpHeld = True
            elif event.key == pygame.K_w:
                MiningRight = True
            elif event.key == pygame.K_s:
                MiningLeft = True

        elif event.type == pygame.KEYUP:
            if event.key ==pygame.K_a:  
                LeftHeld = False
            elif event.key == pygame.K_d:
                RightHeld = False

    # проверка стоит ли на земле
    player.onground_prev = player.onground
    player.onground = check_ground(player,cave)
    # Если кнопка зажата, то 
    # Триггеры анимации движения
    if LeftHeld == RightHeld:
        if player.onground:
            player.animate.Standing(player.animate)
        player.decelerate()
    else:
        if player.onground:
            if player.Vx>0:
                player.animate.Walking_right(player.animate)
            if player.Vx<0:
                player.animate.Walking_left(player.animate)

    if not player.onground:
        if player.Vy<0:
            player.animate.Jumping(player.animate)
        elif player.Vy>0:
            player.animate.Falling(player.animate)

    if player.onground == True and player.onground_prev == False:
        player.animate.Landed(player.animate)


    if RightHeld and not LeftHeld:
        player.accelerate_right()
    elif LeftHeld and not RightHeld:
        player.accelerate_left()
    if UpHeld:
        player.jump()

    if MiningRight:
        weapon.animate.Mining_hit_right(weapon.animate)
        
    if MiningLeft:
        weapon.animate.Mining_hit_left(weapon.animate)
    
    mele_sprites.update(player)


    if weapon.animate.mining_hit_right or weapon.animate.mining_hit_left:
    #    screen.blit(weapon.image,(weapon.rect.x-weapon.animate.x_offset,weapon.rect.y-weapon.animate.y_offset)) 
        weapon_camera_pos = player_camera_pos
        weapon_camera_pos[0] -= weapon.animate.x_offset
        weapon_camera_pos[1] -= weapon.rect.height - player.rect.height
        screen.blit(weapon.image,weapon_camera_pos) 
    
    # Держим цикл на правильной скорости
    player.update(cave)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
