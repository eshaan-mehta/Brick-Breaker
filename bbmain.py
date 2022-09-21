import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('bRiCk bReAkeR')

s_width, s_height = 576, 720

screen = pygame.display.set_mode((s_width,s_height))

brick = pygame.image.load('brick.png')
broken = pygame.image.load('brokenbrick.png')
block = pygame.image.load('block.png')
board = pygame.image.load('board.png')
ball = pygame.image.load('ball.png')
life = pygame.image.load('ball.png')
restart = pygame.image.load('restart.png')
nxt = pygame.image.load("next.png")
overlay = pygame.image.load('overlay.png')

restart_rect = restart.get_rect()
nxt_rect = nxt.get_rect()


level = 1

fontsize = 38
font = pygame.font.Font('font.ttf', fontsize)
level_num = pygame.font.Font('font.ttf', 250)
msg = pygame.font.Font('font.ttf', 55)

game_start = 0

benchmark = 580

touching = False
touchin = False
touchable = True

gameover = False

tolerance = 10

ballspeed = 4.8

size = 48
time = 0
tick = 0


msg_move = False
button_move = False
stars = False
            

def reset(begun, restart_rect):
    global ball_pos, ball_rect, board_pos, board_rect, ballspeedx, ballspeedy, boardright, boardleft
    global death, brick_pos, block_pos, game_map, hitlist, lives, sizex, sizey, message_pos, destination, star_size, pause

    if begun == False:
        lives = 3
        hitlist = []
        game_map = [['2','2','2','2','2','2','2','2','2','2','2','2'],
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],
                    ['2','0','1','1','0','0','0','0','1','1','0','2'],
                    ['2','0','1','1','0','0','0','0','1','1','0','2'],
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],
                    ['2','0','0','0','1','1','1','1','0','0','0','2'],
                    ['2','0','0','1','0','0','0','0','1','0','0','2'],
                    ['2','0','0','1','2','2','2','2','1','0','0','2'],  
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],  #no lower than this
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],  
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],
                    ['2','0','0','0','0','0','0','0','0','0','0','2'],
                    ['2','0','0','0','0','0','0','0','0','0','0','2']]
        

    ball_start_pos = [s_width/2 - ball.get_width()/2, benchmark]
    ball_pos = ball_start_pos

    board_start_pos = [s_width/2 - board.get_width()/2, benchmark + ball.get_height()]
    board_pos = board_start_pos

    brick_pos = [100,100]
    block_pos = [148,100]
    
    ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], ball.get_width(), ball.get_height())
    board_rect = pygame.Rect(board_pos[0], board_pos[1], board.get_width(), board.get_height())
    death = pygame.Rect(0, benchmark + ball.get_height() + 25, s_width, 720 - (benchmark + ball.get_height() + 25))
 
    boardright = False
    boardleft = False

    ballspeedx = 0
    ballspeedy = 0

    sizex = 0
    sizey = 0
    star_size = 100
    
    message_pos = [0, -75]

    destination = (s_width/2, s_height/2 + 35)
    pause = 0
    

    restart_rect.center = (480, 675)

    return restart_rect


def collision(ball_rect, rect, ballspeedx, ballspeedy, tolerance):
    if abs(ball_rect.bottom - rect.top) < tolerance and ballspeedy > 0: #bottom-top
        ballspeedy *= -1
    if abs(ball_rect.top - rect.bottom) < tolerance and ballspeedy < 0: #top-bottom
        ballspeedy *= -1
    if abs(ball_rect.left - rect.right) < tolerance and ballspeedx < 0: #left-right
        ballspeedx *= -1
    if abs(ball_rect.right - rect.left) < tolerance and ballspeedx > 0: #right-left
        ballspeedx *= -1
    return ballspeedx, ballspeedy


def hp_test(rect, hitlist):
#checking if rect has already been hit
    if rect in hitlist:
        hitlist.remove(rect)
        return 0, hitlist 
    else:
        hitlist.append(rect)
        return 1, hitlist
    

def endgame(sizex, sizey, message_pos, msg_move, restart_rect, restart, destination, button_move, touchable, stars, lives, star_size, pause, nxt, nxt_rect, result):
    touchable = False
    follow = False
    show = False
    split = False
    ystar = pygame.image.load('ystar.png')
    star = pygame.image.load('star.png')
    
#box    
    if sizex < 300 and sizey < 240:
        sizex += 5
        sizey += 4 
    elif sizex >= 300:
        msg_move = True
    screen.blit(pygame.transform.scale(box_pic, (sizex, sizey)), (s_width/2 - sizex/2, s_height/2 - sizey/2 - 15))

#message
    if message_pos[1] < s_height/2 - sizey/2 and msg_move == True:
        message_pos[1] += 5 * 0.75
    elif message_pos[1] >= s_height/2 - sizey/2:
        msg_move = False
        follow = True
        stars = True
    screen.blit(message, message_pos)

#stars
    i = 0
    if follow == True:
        if star_size > 48:
            star_size -= 1
        else:
            button_move = True
        while i < 3:
            if i < lives:
                Star = ystar
            else:
                Star = star
            star_rect = Star.get_rect()
            star_rect.center = [s_width/2 + 5 - star.get_width() + i * star.get_width(), s_height/2 - 26]
            screen.blit(pygame.transform.scale(Star, (star_size, star_size)), (star_rect.x, star_rect.y))
            i += 1
            
#button
    if restart_rect.center > destination and button_move == True:
        restart_rect.x -= (480 - destination[0])/90
        restart_rect.y -= (672 - destination[1])/90
    elif restart_rect.center <= destination:
        if result == 0:
            touchable = True
        else:
            split = True
            if pause < 40:
                nxt_rect.center = restart_rect.center

    if split == False:
        nxt_rect.center = (-500,-500)

#button spliting
    if split == True and result == 1:
        if pause > 40:
            if restart_rect.x > 238 - 45:
                nxt_rect.x += 1
                restart_rect.x -= 1
            elif restart_rect.x <= 238 - 45:
                touchable = True
        pause += 1

#button rendering 
    screen.blit(nxt, (nxt_rect.x, nxt_rect.y))    
    screen.blit(restart, (restart_rect.x, restart_rect.y))
    
    return sizex, sizey, message_pos, restart_rect, touchable, star_size, pause
    


restart_rect = reset(False, restart_rect)

while True:
    screen.fill((169,192,201))

#level num rendering
    text = level_num.render('%d' %(level), True, (52,119,143))
    text_rect = text.get_rect()
    text_rect.center = (s_width/2, s_height/2 + 65)
    screen.blit(text, text_rect)

    mx, my = pygame.mouse.get_pos()
    
    pygame.draw.rect(screen, (44,66,74), death)
    
#lives text rendering
    text = font.render('Lives:', True, (255,255,255)) 
    screen.blit(text,(55, 657))


#lives image rendering
    i = 1
    while i <= lives:
        life_pos = [text.get_width() + 30 + i * (life.get_width() + 4),662]
        screen.blit(life,life_pos)
        i += 1

#ball, board and restart button rendering
    screen.blit(ball,ball_pos)
    screen.blit(board,board_pos)
    if button_move == False:
        screen.blit(restart,(restart_rect.x,restart_rect.y))

#rendering correct image in tile grid        
    y = 0
    tile_rects = []
    is_brick = []
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(brick, (x * size, y * size))
            if tile == '3':
                screen.blit(broken, (x * size, y * size))
            if tile == '2':
                screen.blit(block, (x * size, y * size))
            if tile != '0':
                sq_rect = pygame.Rect(x * size, y * size, size, size)
                if not(sq_rect.top == 0 or sq_rect.left == 0 or sq_rect.right == s_width):
                    tile_rects.append(sq_rect)  #adding to physics list
                    if tile != '2':
                        is_brick.append(sq_rect)    #adding to brick list
            x += 1
        y += 1


#checking for collision with each tile & hp testing
    for rect in tile_rects:
        if ball_rect.colliderect(rect):
            ballspeedx, ballspeedy = collision(ball_rect, rect, ballspeedx, ballspeedy, tolerance) #calling collision function
            if rect in is_brick:
                hp, hitlist = hp_test(rect, hitlist)    #hp test
                a = int(rect.x/size)
                b = int(rect.y/size)

                #updating game_map
                if hp == 1:
                    game_map[b][a] = '3'
                if hp == 0:
                    tile_rects.remove(rect)
                    is_brick.remove(rect)
                    game_map[b][a] = '0'

#game end
    result = -1
    if len(is_brick) == 0 or lives <= 0:
        time += 1
        if len(is_brick) == 0:
            result = 1
        elif lives <= 0:
            result = 0
        screen.blit(pygame.transform.scale(overlay, (s_width, s_height)), (0,0))
        box_pic = pygame.image.load('box.png')
        if result == 0:
            second = "Lose"
        else:
            second = "Win"
    
        message = msg.render('You %s' %(second), True, (255,255,255))
        message_pos[0] = s_width/2 - message.get_width()/2

        if time >= 45:
            sizex, sizey, message_pos, restart_rect, touchable, star_size, pause = endgame(sizex, sizey, message_pos, msg_move, restart_rect, restart,destination, button_move,
                                                                                                touchable, stars, lives, star_size, pause, nxt, nxt_rect, result)
        boardright = False
        boardleft = False
        ballspeedx = 0
        ballspeedy = 0
        gameover = True
    


#board movement
    if boardright:
        board_pos[0] += 5
    if boardleft:
        board_pos[0] -= 5
    board_rect.x = board_pos[0]
    board_rect.y = board_pos[1]


#ball movement
    ball_pos[0] += ballspeedx
    ball_pos[1] += ballspeedy
    ball_rect.x = ball_pos[0]
    ball_rect.y = ball_pos[1]


#collision with walls
    if ball_rect.right >= s_width - size or ball_rect.left <= 0 + size:       #ball
        ballspeedx *= -1
    if ball_rect.bottom >= s_height or ball_rect.top <= 0 + size:
        ballspeedy *= -1

    if board_rect.right >= s_width - size:      #board
        boardright = False
    if board_rect.left <= 0 + size:
        boardleft = False


#collision with board
    if ball_rect.colliderect(board_rect):
        if abs(ball_rect.bottom - board_rect.top) < tolerance and ballspeedy > 0:
            ballspeedy *= -1
            if ballspeedx > 0 and boardleft == True:
                ballspeedx *= -1
            if ballspeedx < 0 and boardright == True:
                ballspeedx *= -1
        if abs(ball_rect.top - board_rect.bottom) < tolerance and ballspeedy < 0:
            ballspeedy *= -1
        if abs(ball_rect.left - board_rect.right) < tolerance and ballspeedx < 0:
            ballspeedx *= -1
        if abs(ball_rect.right - board_rect.left) < tolerance and ballspeedx > 0:
            ballspeedx *= -1


#collision with deathzone
    if ball_rect.colliderect(death):
        restart_rect = reset(True, restart_rect)
        game_start = 0
        lives -= 1

#events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if gameover == False:
            if event.type == KEYDOWN:
                if event.key == 97 or event.key == K_LEFT and board_rect.left > 0 + size:
                    begun = True
                    boardleft = True
                    if game_start == 0:
                        ballspeedx = -ballspeed - 1
                        ballspeedy = -ballspeed
                    game_start += 1
                if event.key == 100 or event.key == K_RIGHT and board_rect.right < s_width - size:
                    begun = True
                    boardright = True
                    if game_start == 0:
                        ballspeedx = ballspeed + 0.8
                        ballspeedy = -ballspeed
                    game_start += 1
            if event.type == KEYUP:
                if event.key == 97 or event.key == K_LEFT:
                    boardleft = False
                if event.key == 100 or event.key == K_RIGHT:
                    boardright = False

                    
#restart button collision
        if restart_rect.collidepoint(mx,my) and touchable == True:
            touching = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    restart_rect = reset(False, restart_rect)
                    game_start = 0
                    gameover = False
        else:
            touching = False

#next level button collision
        if nxt_rect.collidepoint(mx,my) and touchable == True and result == 1:
            touchin = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    restart_rect = reset(False, restart_rect)
                    game_start = 0
                    gameover = False
                    level += 1
        else:
            touchin = False

#button resizing
    if touchin == True:
        screen.blit(pygame.transform.scale(nxt, (74,74)),(nxt_rect.x - 5, nxt_rect.y - 5))
    if touching == True:
        screen.blit(pygame.transform.scale(restart, (74, 74)),(restart_rect.x - 5,restart_rect.y - 5))
            
    tick += 1
    if tick % 60 == 0:
        level += 0
    pygame.display.update()
    clock.tick(60)
