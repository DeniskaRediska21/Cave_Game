import pygame

def check_ground(ball,map):
    onground = True
    ball.rect.bottom += 1
    if pygame.sprite.collide_mask(map,ball) == None:
        onground = False
    ball.rect.bottom -= 1
    
    return onground

def check_mask_collision(ball,map,Vx,Vy,slope_tolarance = 10):
    Flag = 0    
    if pygame.sprite.collide_mask(map,ball) != None:
        Flag = 4
        if Vx>0:
            for i in range(abs(Vx)):
                Flag = 3
                ball.rect.right -= 1
                for j in range(slope_tolarance):
                    ball.rect.bottom -= 1
                    if pygame.sprite.collide_mask(map,ball) == None:
                        return Flag
                ball.rect.bottom += slope_tolarance
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag


        elif Vx<0:
            for i in range(abs(Vx)):
                Flag = 3
                ball.rect.left += 1
                for j in range(slope_tolarance):
                    ball.rect.bottom -= 1
                    if pygame.sprite.collide_mask(map,ball) == None:
                        return Flag
                ball.rect.bottom += slope_tolarance
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag


        if Vy<0:
            Flag = 1
            for i in range(abs(Vy)):
                ball.rect.top += 1
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag
            

        elif Vy>0:
            Flag = 2
            for i in range(abs(Vy)):
                ball.rect.bottom -= 1
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag
    return Flag
