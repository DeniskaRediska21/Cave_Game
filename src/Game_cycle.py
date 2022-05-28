import pygame
import random
import numpy as np
import math

from lib.cave.main import Cave
from lib.objects.charecter import character
from lib.objects.weapons import mele
from lib.objects.weapons import shooting
from lib.objects.map import map
from lib.objects.map import random_spawn
from lib.animation.spritesheet_to_sprites import sheet2frames
from lib.colisions.colisions import check_mask_collision
from lib.colisions.colisions import check_ground

WIDTH = 800
HEIGHT = 400
FPS = 30

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cave Game")
clock = pygame.time.Clock()

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
fist = mele((player.rect.x,player.rect.y))
pistol = shooting()
# Группировка спрайтов
all_sprites = pygame.sprite.Group()
all_sprites.add(cave)

mele_sprites = pygame.sprite.Group()
mele_sprites.add(fist)

# Jump_flag = True



background = pygame.Surface((l*scaling_coeff,h*scaling_coeff))
background.fill(GRAY)

camera_scroll_true = np.array((player.rect.x-WIDTH/2, player.rect.y-HEIGHT/2))




UpHeld = False
DownHeld = False
RightHeld = False
LeftHeld = False
MiningRight = False
MiningLeft = False 

# Цикл игры
running = True
while running:
    
    all_sprites.update(fist)
    mele_sprites.update(player,cave)
    player.update(cave)
    pistol.update(cave)
    
    
    
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
    
    
    screen.fill(BLACK)
    screen.blit(background,cave_camera_pos)
    screen.blit(player.image, player_camera_pos)
    screen.blit(cave.image, cave_camera_pos)
    for number,bullet in enumerate(pistol.bullets):
        screen.blit(bullet.image, np.array(bullet.rect.topleft) - camera_scroll)
    
    

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
                    

    # Если зажата кнопка, то стрелять
    mouse = pygame.mouse.get_pressed(num_buttons=3)
    if mouse[0]:
        pistol.shoot(camera_scroll,player)

    # Проверка стоит ли на земле и запоминание прошлого состояния для анимации
    player.onground_prev = player.onground
    player.onground = check_ground(player,cave)
    
    # Если кнопка зажата, то 
    # Триггеры анимации движения вправо и влево
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

    # Если игрок не на земле и летит вверх, то играть анимацию прыжка,если падает, то падения
    if not player.onground:
        if player.Vy<0:
            player.animate.Jumping(player.animate)
        elif player.Vy>0:
            player.animate.Falling(player.animate)

    # Если игрок на земле, а до этого на земле не был проиграть анимацию приземления
    if player.onground == True and player.onground_prev == False:
        player.animate.Landed(player.animate)
        

    # Если идет анимация удара, нарисовать кадр удара
    if fist.animate.mining_hit_right or fist.animate.mining_hit_left:
        fist_camera_pos = np.array((fist.rect.x,fist.rect.y))-camera_scroll
        screen.blit(fist.image,fist_camera_pos) 



    # Если зажата кнопка то ускоряемся
    if RightHeld and not LeftHeld:
        player.accelerate_right()
    elif LeftHeld and not RightHeld:
        player.accelerate_left()
    if UpHeld:
        player.jump()

    # В конце анимации запускается действие, поэтому вызывается анимация
    if MiningRight:
        fist.animate.Mining_hit_right(fist.animate)
        
    if MiningLeft:
        fist.animate.Mining_hit_left(fist.animate)
    
    
    


    
    
    
    
    # Держим цикл на правильной скорости

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
