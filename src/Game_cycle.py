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


l=80
h=40
cave = Cave()
cave.save_cave(47,l,h,1,10,smooth_pixels=False)  # True для гладкой карты, False(Быстрее) для пиксельной

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
all_sprites.add(player)
all_sprites.add(cave)

mele_sprites = pygame.sprite.Group()
mele_sprites.add(weapon)

# Jump_flag = True

WIDTH = cave.rect.width
HEIGHT = cave.rect.height
WIDTH = 800
HEIGHT = 400
FPS = 30

background = pygame.Surface((WIDTH,HEIGHT))
background.fill(GRAY)

cave_camera_pos = np.array((-player.rect.x+WIDTH/2, -player.rect.y+HEIGHT/2))

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
onground = False
# Цикл игры
running = True
while running:
    all_sprites.update(cave)
    
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
    cave_camera_pos_prev = cave_camera_pos
    cave_camera_pos = np.array((-player.rect.x+WIDTH/2, -player.rect.y+HEIGHT/2))
    player_camera_pos = np.array((WIDTH/2-player.animate.x_offset, HEIGHT/2-player.animate.y_offset))
    
    camera_lag =0.3*(cave_camera_pos - cave_camera_pos_prev)
    
    screen.fill(BLACK)
    screen.blit(background,cave_camera_pos-camera_lag)
    screen.blit(player.image, player_camera_pos+camera_lag)
    screen.blit(cave.image, cave_camera_pos-camera_lag)

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
    onground_prev = onground
    onground = check_ground(player,cave)
    # Если кнопка зажата, то 
    # Триггеры анимации движения
    if LeftHeld == RightHeld:
        if onground:
            player.animate.Standing(player.animate)
        if player.Vx>0:
            player.Vx = max(0,player.Vx-player.Vx_deceliration)
        else:
            player.Vx = min(0,player.Vx+player.Vx_deceliration)
    else:
        if onground:
            if player.Vx>0:
                player.animate.Walking_right(player.animate)
            if player.Vx<0:
                player.animate.Walking_left(player.animate)

    if not onground:
        if player.Vy<0:
            player.animate.Jumping(player.animate)
        elif player.Vy>0:
            player.animate.Falling(player.animate)

    if onground == True and onground_prev == False:
        player.animate.Landed(player.animate)


    if RightHeld and not LeftHeld:
        player.walk_right()
    elif LeftHeld and not RightHeld:
        player.walk_left()
    if UpHeld:
        player.jump()

    if MiningRight:
        weapon.animate.Mining_hit_right(weapon.animate)
        
    if MiningLeft:
        weapon.animate.Mining_hit_left(weapon.animate)
    
    mele_sprites.update(player)


    if weapon.animate.mining_hit_right or weapon.animate.mining_hit_left:
    #    screen.blit(weapon.image,(weapon.rect.x-weapon.animate.x_offset,weapon.rect.y-weapon.animate.y_offset)) 
        weapon_camera_pos = player_camera_pos+camera_lag
        weapon_camera_pos[0] -= weapon.animate.x_offset
        weapon_camera_pos[1] -= weapon.rect.height - player.rect.height
        screen.blit(weapon.image,weapon_camera_pos) 
    
    ## Нужно перенести в character object
    # # Движение по X
    # player.rect.centerx += player.Vx
    # Vx_flag = check_mask_collision(player,cave,player.Vx,0)

    # # Движение по Y
    # player.rect.centery += player.Vy 
    # Vy_flag = check_mask_collision(player,cave,0,player.Vy)

    # # Если ударисля о пол или потолок
    # if Vy_flag == 1:
    #     player.Vy = 0
    # elif Vy_flag == 2:
    #     player.Vy = 0
    #     Jump_flag = True

    # # Гравитация
    # player.Vy +=player.g 

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
