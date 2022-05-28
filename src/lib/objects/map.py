import pygame
import random
import numpy as np
from lib.colisions.colisions import check_mask_collision

class map(pygame.sprite.Sprite):

    def __init__(self, file):
        pygame.sprite.Sprite.__init__(self)
        surface = pygame.image.load(file)

        self.image = surface.convert_alpha()

        self.rect = self.image.get_rect() # size and position

        self.mask = pygame.mask.from_surface(self.image)
        
        self.render_distance = 50
        
        self.changed = False
        
        self.health = self.get_health()
        
        
    def update(self,change):
        pass
        # if self.changed:
        #     for i in range(max(self.rect.left,int(change.rect.left)),min(self.rect.right,int(change.rect.right))):
        #         for j in range(max(self.rect.top,int(change.rect.top)),min(self.rect.bottom,int(change.rect.bottom))):
        #             if self.mask.get_at((i,j)) == 0:
        #                 self.image.set_at((i,j),(0,0,0,0))
        # self.changed = False
        
        # pass
        # inverted_mask = self.mask.copy()
        # inverted_mask.invert()
        # self.image = inverted_mask.to_surface()
        # self.image.set_colorkey((255, 255, 255, 255))
    def damage_blocks(self,shape):
        for i in range(max(self.rect.left,int(shape.rect.left)),min(self.rect.right,int(shape.rect.right))):
            for j in range(max(self.rect.top,int(shape.rect.top)),min(self.rect.bottom,int(shape.rect.bottom))):
                # damaging
                mask_pos = shape.rect.topleft
                if shape.mask.get_at((i-mask_pos[0],j-mask_pos[1])) == 1 and self.health[i][j] > 0:
                    self.health[i][j] -= shape.block_damage
                    pixel = self.image.get_at((i,j))
                    pixel[3] = int(self.health[i][j]*255)
                    self.image.set_at((i,j),pixel)
                    self.changed = True
                # breaking
                if self.health[i][j] <=0:
                    self.mask.set_at((i,j),0)
                    self.image.set_at((i,j),(0,0,0,0))
                    self.changed = False
                
    
    def break_blocks(self, shape):
        self.mask.erase(shape.mask, shape.rect.topleft)
        self.changed = True
        
    def get_health(self):
        health = np.zeros(self.rect.size)
        for i in range(self.rect.left,self.rect.right):
            for j in range(self.rect.top,self.rect.bottom):
                health[i][j] = self.mask.get_at((i,j))
        return health



def random_spawn(ball,cave):
    ball.rect.x = round(random.random() * cave.rect.width)
    ball.rect.y = round(random.random() * cave.rect.height)
    while check_mask_collision(ball,cave,0,0,0) != 0:
        ball.rect.x = round(random.random() * cave.rect.width)
        ball.rect.y = round(random.random() * cave.rect.height)