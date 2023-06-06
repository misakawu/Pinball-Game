import random
import pygame
import time
from item_sprites import *

background = pygame.image.load("image/background.png")#.convert()
blackground = pygame.image.load("image/blackground.png")#.convert()

font = pygame.font.Font(None, 50)
font_s = pygame.font.Font(None, 30)
font_sB = pygame.font.Font(None, 100)
font_sc = pygame.font.Font('front/卡通.ttf',30)
font_scB = pygame.font.Font('front/卡通.ttf',100)
#障碍物生成函数
#横向生成
def horizon(line,lenth,x,y,space,bricks):
    for i in range(line):
        for j in range(lenth):
            ju = random.randint(0,10)
            if ju==2:
                bricks.append(double_Brick(x + j * 30*space, y + i * 30))
            else:
                bricks.append(Brick(x + j * 30*space, y + i * 30))
#纵向生成
def lengthwise(line,lenth,x,y,space,bricks):
    for i in range(lenth):
        for j in range(line):
            ju = random.randint(0,10)
            if ju==2:
                bricks.append(double_Brick(x + j * 20, y + i * 20*space))
            else:
                bricks.append(Brick(x + j * 20, y + i * 20*space))
                
#斜向生成，0为左上到右下，1为右上到左下
def cross(x,y,lenth,way,bricks):
    if way==0:
        for i in range(lenth):
            ju = random.randint(0,10)
            if ju==2:
                bricks.append(double_Brick(x + i*20,y + i*20))
            else:
                bricks.append(Brick(x + i*20,y + i*20))
    elif way==1:
        for i in range(lenth):
            ju = random.randint(0,10)
            if ju==2:
                bricks.append(double_Brick(x - i*20,y + i*20))
            else:
                bricks.append(Brick(x - i*20,y + i*20))
#随机生成
def randompic(num,bricks):
    for i in range(num):
        ju = random.randint(0,10)
        x = random.choice(range(20,980,20))
        y = random.choice(range(170,680,20))
        if ju==2:
            bricks.append(double_Brick(x,y))
        else:
            bricks.append(Brick(x,y))

#图形函数
#梯形(0为上底为短边，1位下底为短边)
def trapezoid(x,y,lenth,height,way,bricks):
    if way==0:
        for i in range(height):
            horizon(1,lenth+i,x-i*15,y + i*30,1,bricks)
    else:
        for i in range(height):
            horizon(1,lenth-i,x+i*15,y + i*30,1,bricks)
            
#菱形(只有三层，(x,y)为第一层最左边坐标，作为主要元素填充，建议长度不超过6)
def diomond(x,y,lenth,bricks):
    horizon(1,lenth,x,y,1,bricks)
    horizon(1,lenth+2,x-30,y+30,1,bricks)
    horizon(1,lenth,x,y+60,1,bricks)
#方形
def square(x,y,lenth,fill,bricks):
    if fill==1:
        for i in range(lenth-1):
            lengthwise(1,lenth,x+20*i,y,1,bricks)
    else:
        lengthwise(1,lenth,x,y,1,bricks)
        lengthwise(1,lenth,x+20*(lenth-1)+(lenth-1)*6,y,1,bricks)
        horizon(1,lenth-1,x,y-20,1,bricks)
        horizon(1,lenth-1,x,y+20*lenth,1,bricks)
        
def new_game(screen,player,enemy):
    close=True
    while close:
        screen.blit(background, (0, 0))
        text = font_scB.render("PRESS TO START", True, 'red')
        text2=font_scB.render("A NEW GAEW", True, 'red')
        screen.blit(text, (100, 200))
        screen.blit(text2, (200, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:  
                player.health=100
                enemy.health=random.randint(150,200)
                enemy.damage=random.randint(1,5)
                return
    
def end_game(screen,player,enemy):
    if enemy.health<=0:
        while True:
            screen.blit(background, (0, 0))
            text = font_sB.render("GOOD GAME", True, 'yellow')
            screen.blit(text, (300, 300))
            pygame.display.update()
            time.sleep(1)
            new_game(screen,player,enemy)
            return 1
    elif player.health<=0:
        while True:
            screen.blit(background, (0, 0))
            text = font_scB.render("YOU DEAD", True, 'red')
            screen.blit(text, (300, 300))
            pygame.display.update() 
            time.sleep(1)
            new_game(screen,player,enemy)
            return 1
    return 0