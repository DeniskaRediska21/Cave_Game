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
    # Границы карты
    if ball.rect.top < map.rect.top:
        ball.rect.top = map.rect.top
        Flag = 1
    if ball.rect.bottom > map.rect.bottom:
        ball.rect.bottom = map.rect.bottom
        Flag = 2
    if ball.rect.left < map.rect.left:
        ball.rect.left = map.rect.left   
    if ball.rect.right > map.rect.right:
        ball.rect.right = map.rect.right 
        
    # Остальная коллизия    
      
    if pygame.sprite.collide_mask(map,ball) != None:
        Flag = 4
        if Vx>0:
            for i in range(abs(int(Vx))):
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
            for i in range(abs(int(Vx))):
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
            for i in range(abs(int(Vy))):
                ball.rect.top += 1
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag
            

        elif Vy>0:
            Flag = 2
            for i in range(abs(int(Vy))):
                ball.rect.bottom -= 1
                if pygame.sprite.collide_mask(map,ball) == None:
                    return Flag
    return Flag


def check_mask_collision_simple(object,map,Vx,Vy):
    Flag = 0  
    # Границы карты
    if object.rect.top < map.rect.top:
        object.rect.top = map.rect.top
        Flag = 1
    if object.rect.bottom > map.rect.bottom:
        object.rect.bottom = map.rect.bottom
        Flag = 2
    if object.rect.left < map.rect.left:
        object.rect.left = map.rect.left 
        Flag = 3  
    if object.rect.right > map.rect.right:
        object.rect.right = map.rect.right
        Flag = 3
        
    # Остальная коллизия    
      
    if pygame.sprite.collide_mask(map,object) != None:
        Flag = 4
        if Vx>0 :
            Flag = 3
        elif Vx<0:
            Flag = 3

        if Vy<0:
            Flag = 1
        elif Vy>0:
            Flag = 2

    return Flag

