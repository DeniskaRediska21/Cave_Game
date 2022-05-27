import pygame
from lib.animation.spritesheet_to_sprites import sheet2frames

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
        
