import pygame
import numpy as np
import math
from lib.animation.spritesheet_to_sprites import sheet2frames
from lib.colisions.colisions import check_mask_collision, check_mask_collision_simple

class mele(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.sprites.__init__(self.sprites)
        self.animate.__init__(self.animate)
        self.image = self.sprites.mining_hit_right[-1]
        self.rect = self.image.get_rect() # size and position
        
        self.w = self.rect.width
        self.h = self.rect.height
        self.block_damage = 0.5
        
    
    def update(self,character,cave):
        if self.animate.mining_hit_right:
            self.rect.bottomleft = character.rect.bottomleft
        elif self.animate.mining_hit_left:
            self.rect.bottomright = character.rect.bottomright

        if self.animate.mining_hit_right == True:
            self.animate.current_frame += 0.4
            if self.animate.current_frame >= len(self.sprites.mining_hit_right):
                self.animate.current_frame = 0
                cave.damage_blocks(self)
                self.animate.mining_hit_right = False
                
            self.image = self.sprites.mining_hit_right[int(self.animate.current_frame)]
            self.mask = pygame.mask.from_surface(self.image)
            # self.rect = self.image.get_rect()
            self.animate.Set_offsets(self,character)
            self.animate.y_offset = 0

        if self.animate.mining_hit_left == True:
            self.animate.current_frame += 0.4
            if self.animate.current_frame >= len(self.sprites.mining_hit_left):
                self.animate.current_frame = 0
                cave.damage_blocks(self)
                self.animate.mining_hit_left = False
                
            self.image = self.sprites.mining_hit_left[int(self.animate.current_frame)]
            self.mask = pygame.mask.from_surface(self.image)
            # self.rect = self.image.get_rect()
            self.animate.Set_offsets(self,character)
            self.animate.y_offset = 0

    class animate():
        def __init__(self):
            self.current_frame = 0
            self.x_offset = 0
            self.y_offset = 0
            
            self.mining_hit_right = False
            self.mining_hit_left = False

        def Set_offsets(self,character):
            if self.animate.mining_hit_right:
                self.rect.left = character.rect.left
            if self.animate.mining_hit_left:
                self.rect.right = character.rect.right
            # self.animate.x_offset = (self.image.get_rect().width - self.w)/2
            # self.animate.y_offset = (self.image.get_rect().height - self.h)

        def setup(self):
                self.current_frame = 0
                self.mining_hit_right = False
                self.mining_hit_left = False
                
        def Mining_hit_right(self):
            if not self.mining_hit_right:
                self.setup(self)
                self.mining_hit_right = True

        def Mining_hit_left(self):
            if not self.mining_hit_left:
                self.setup(self)
                self.mining_hit_left = True

    class sprites():
        def __init__(self):
            self.mining_hit_right = []
            self.mining_hit_left = []
            
            self.mining_hit_right = sheet2frames('src\Textures\Mining_hit.png')
            
            # Движение налево обратно движению направо
            for frame in self.mining_hit_right:
                self.mining_hit_left.append(pygame.transform.flip(frame, True, False))

class bullet(pygame.sprite.Sprite):
    def __init__(self,angle,pos,velocity = 10, gravity = 0, image = 'src\Textures\Pistol_bullet.png'):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = velocity
        self.gravity = gravity
        self.image = pygame.image.load(image).convert_alpha()
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.Vx = self.velocity*math.sin(self.angle)
        self.Vy = self.velocity*math.cos(self.angle) 
        self.block_damage = 0.5
    
    def update(self,cave):
        self.rect.centerx += self.Vx
        Flag_X = check_mask_collision_simple(self,cave,self.Vx,0)
        
        self.rect.centery += self.Vy 
        Flag_Y = check_mask_collision_simple(self,cave,self.Vx,0)
        self.Vy += self.gravity
        return Flag_X, Flag_Y

    def explode(self,cave):
        center = self.rect.center
        self.image = pygame.image.load('src\Textures\Explosion.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.mask = pygame.mask.from_surface(self.image)
        cave.damage_blocks(self)
        
      
class shooting(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bullets = []
        self.angles = []
        
        
    def shoot(self,camera_scroll,player):
        mouse_pos = camera_scroll + np.array(pygame.mouse.get_pos())
        angle = math.atan2(mouse_pos[0] - player.rect.centerx, mouse_pos[1] - player.rect.centery)
        self.bullets.append(bullet(angle,player.rect.center))
    
    def update(self,cave):
        for number,bullet in enumerate(self.bullets):
            Flag_X,Flag_Y = bullet.update(cave)
            if Flag_X or Flag_Y != 0:
                bullet.explode(cave)
                del self.bullets[number] 

            
        


        
    