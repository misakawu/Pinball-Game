import pygame
import random
import time
import sys

#玩家角色
class Player:
    def __init__(self):
        self.health=100
        self.damage=5
        self.image=pygame.image.load('image/player.png')
        self.big_image=pygame.image.load('image/player.png')
        self.big_image=pygame.transform.scale(self.image,(100,140))
        
    def damaged(self,x):
        self.health-=x
    
    def add_weapon(self,x):
        self.damage+=x.damage
    
    def draw(self, surface):
        surface.blit(self.image, (10, 10))
        health_num = font_sc.render('血量:'+str(self.health), True, 'red')
        damage_num = font_sc.render('基础伤害:'+str(self.damage), True, 'red')
        surface.blit(health_num, (70, 10))
        surface.blit(damage_num, (70, 35))
    
#回复药
class HPbottle:
    def __init__(self,point):
        self.point=point
        self.image=pygame.image.load('image/HP.png')
        self.type=0#回复型
        
    def draw(self,surface,x):
        surface.blit(self.image, (int(x), 80))
        
    def use(self,x):
        if x.health>100-self.point:
            x.health=100
            print('使用道具：回复药，回复血量',100-x.health)
        else:
            x.health+=self.point
            print('使用道具：回复药，回复血量',self.point)
        pygame.mixer.Sound.play(heal)
        items.pop(0)
#枪
class Weapon:
    def __init__(self,damage):
        self.damage=damage
        self.image=pygame.image.load('image/gun.png')
        self.type=1#输出型
        
    def draw(self,surface,x):
        surface.blit(self.image, (int(x), 80))
        
    def use(self,x):
        if x.health>=x.health-self.damage:
            x.health-=self.damage
            print('使用道具：枪，造成伤害',self.damage)
        else:
            x.health=0
            print('使用道具：枪，造成伤害',x.health)
        pygame.mixer.Sound.play(gun)
        items.pop(0)
#祝福
class Bless:
    def __init__(self,point):
        self.point=point
        self.image=pygame.image.load('image/StrengthPotion.png')
        self.type=0#回复型
        
    def draw(self,surface,x):
        surface.blit(self.image, (int(x), 80))
        
    def use(self,x):
        x.damage+=self.point
        print('使用道具：力量药剂，基础伤害+1')
        pygame.mixer.Sound.play(potion)
        items.pop(0)
#护盾
class Shields:
    def __init__(self,point):
        self.point=point
        self.image=pygame.image.load('image/Shields.png')
        self.type=0#回复型
        
    def draw(self,surface,x):
        surface.blit(self.image, (int(x), 80))
        
    def use(self,x):
        x.health+=self.point
        print('使用道具：护盾药水，血量增加',self.point)
        pygame.mixer.Sound.play(potion)
        items.pop(0)
        
#敌人类
class Enemy:
    def __init__(self):
        self.health=200
        self.damage=4
        self.image=pygame.image.load('image/enemy.png')
        self.big_image=pygame.image.load('image/enemy.png')
        self.big_image=pygame.transform.scale(self.image,(100,140))
        
        
    def draw(self, surface):
        surface.blit(self.image, (screen_size[0]-50, 10))
        health_num = font_sc.render('血量:'+str(self.health), True, 'red')
        damage_num = font_sc.render('基础伤害:'+str(self.damage), True, 'red')
        surface.blit(health_num, (screen_size[0]-225, 10))
        surface.blit(damage_num, (screen_size[0]-225, 35)) 
        

# 定义砖块类
class Brick:
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
        self.x=x
        self.y=y
        self.image=pygame.image.load('image/tile_0099.png')
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.type=0

    def draw(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))

    def colliderect(self, x, y, width, height):
        return self.rect.colliderect(pygame.Rect(x, y, width, height))
        
    def __hash__(self):
        return hash((self.x, self.y))
    
class double_Brick(Brick):
    def __init__(self,x,y):
        self.width = 30
        self.height = 30
        self.x=x
        self.y=y
        self.image=pygame.image.load('image/tile_0337.png')
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.type=1
        
    def draw(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))
        
    def colliderect(self, x, y, width, height):
        return self.rect.colliderect(pygame.Rect(x, y, width, height))
        
# 定义小球类
class Ball:
    def __init__(self,screen_size,x,y):
        #(x,y)向右下为正
        self.pos = [x, y]  # 小球初始位置
        self.speed = [0,0]  # 小球初始速度
        self.radius = 8  # 小球半径
        self.gy=0.5
        self.image=pygame.image.load('image/tile_0000.png')

    def draw(self,surface):
        surface.blit(self.image, (int(self.pos[0]-self.radius), int(self.pos[1]-self.radius)))
        

    def update_position(self):
        # 更新小球位置
        self.pos[0] += self.speed[0] 
        self.pos[1] += self.speed[1]
        # 更新小球纵向速度
        self.speed[1]+=0.4

    def check_walls(self,sceen_size):
        # 检查小球是否碰到屏幕边缘，如果是则反弹
        #横向检测
        if self.pos[0] < self.radius: 
            self.speed[0] = -self.speed[0]
            self.pos[0]=self.radius+1
        if self.pos[0] > sceen_size[0] - self.radius:
            self.speed[0] = -self.speed[0]
            self.pos[0]=sceen_size[0] - self.radius-1
        #纵向检测
        if self.pos[1] < self.radius+120:
            self.speed[1] += 0.5
            self.speed[1] = -self.speed[1]
            self.pos[1]=self.radius+123

    def check_brick_collision(self, bricks):
        # 检查小球是否与砖块碰撞
        for brick in bricks:
           if brick.colliderect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2): 
               #横向边碰撞
               if abs(self.pos[1]+self.radius-brick.y)<10:
                   self.speed[1] = -self.speed[1]
                   self.speed[1] +=0.8
               if abs(self.pos[1]-self.radius-(brick.y+brick.height))<10:
                   self.speed[1] = -self.speed[1]
                   self.speed[1] -=0.8
               #纵向边碰撞
               if abs(self.pos[0]+self.radius-brick.x)<10:
                   self.speed[0] = -self.speed[0]
               if abs(self.pos[0]-self.radius-(brick.x+brick.width))<10:
                   self.speed[0] = -self.speed[0]
               #判断获得的状态
               if brick.type==1:
                   new_ball=Ball(screen,self.pos[0],self.pos[1])
                   new_ball.speed[0]=-self.speed[0]
                   new_ball.speed[1]=self.speed[1]
                   balls.append(new_ball)
               #记分
               global score
               score+=1
               sc=ScorePoint(brick.x,brick.y,score)
               score_list.append(sc)
               
               score_show()
               bricks.remove(brick)
               return True
        return False
    

#线段类
class Line:
    def __init__(self):
        self.start_pos = [500,150]
        self.end_pos = [500,50]
        self.color = 'white'
        self.width = 1
    def update_end_pos(self, end_pos):
        self.end_pos = end_pos
    def draw(self,surface):
        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)
        
#得分类
class ScorePoint:
    def __init__(self,x,y,point):
        self.x=x
        self.y=y
        self.point=point
        self.time=25

################################################
# 初始化Pygame
pygame.init()
screen_size = (1000, 700)
screen = pygame.display.set_mode(screen_size)
tem_screen = pygame.Surface(screen_size)
pygame.display.set_caption("Bagatelle")

#加载背景
background = pygame.image.load("image/background.png").convert()
blackground = pygame.image.load("image/blackground.png").convert()
#加载字体
font = pygame.font.Font(None, 50)
font_s = pygame.font.Font(None, 30)
font_sB = pygame.font.Font(None, 100)
font_sc = pygame.font.Font('front/卡通.ttf',30)
font_scB = pygame.font.Font('front/卡通.ttf',100)
#创建游戏元素
balls = []
bricks = []  # 砖块列表
#加载受击gif动画
image_list=['01.png','02.png','03.png','04.png','05.png','06.png']
damage_list = []
for i in image_list:
    ii = pygame.image.load(f'image/{i}')
    ii=pygame.transform.scale(ii,(100,200))
    damage_list.append(ii)
#加载音效
pygame.mixer.init()
heal=pygame.mixer.Sound('sound/回复.wav')
gain=pygame.mixer.Sound('sound/获得.wav')
gun=pygame.mixer.Sound('sound/枪攻击.wav')
potion=pygame.mixer.Sound('sound/使用药水.wav')
attack=pygame.mixer.Sound('sound/一般攻击.wav')
BGM=pygame.mixer.music.load('sound/BGM.mp3')
#玩家
player = Player()
#道具
items =[]
food=HPbottle(20)
items.append(food)
#敌人
enemy = Enemy()
#得分
score = 0
score_list = []

################################################################
#障碍物生成函数
#横向生成
def horizon(line,lenth,x,y,space):
    for i in range(line):
        for j in range(lenth):
            ju = random.randint(0,10)
            if ju==2:
                bricks.append(double_Brick(x + j * 30*space, y + i * 30))
            else:
                bricks.append(Brick(x + j * 30*space, y + i * 30))
#纵向生成
def lengthwise(line,lenth,x,y,space):
    for i in range(lenth):
        for j in range(line):
            ju = random.randint(0,10)
            if ju==2:
                bricks.append(double_Brick(x + j * 20, y + i * 20*space))
            else:
                bricks.append(Brick(x + j * 20, y + i * 20*space))
                
#斜向生成，0为左上到右下，1为右上到左下
def cross(x,y,lenth,way):
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
def randompic(num):
    for i in range(num):
        ju = random.randint(0,10)
        x = random.choice(range(20,980,20))
        y = random.choice(range(170,680,20))
        global bricks
        if ju==2:
            bricks.append(double_Brick(x,y))
        else:
            bricks.append(Brick(x,y))
            bricks=list(set(bricks))
            
#图形函数
#梯形(0为上底为短边，1位下底为短边)
def trapezoid(x,y,lenth,height,way):
    if way==0:
        for i in range(height):
            horizon(1,lenth+i,x-i*15,y + i*30,1)
    else:
        for i in range(height):
            horizon(1,lenth-i,x+i*15,y + i*30,1)
            
#菱形(只有三层，(x,y)为第一层最左边坐标，作为主要元素填充，建议长度不超过6)
def diomond(x,y,lenth):
    horizon(1,lenth,x,y,1)
    horizon(1,lenth+2,x-30,y+30,1)
    horizon(1,lenth,x,y+60,1)
#方形
def square(x,y,lenth,fill):
    if fill==1:
        for i in range(lenth-1):
            lengthwise(1,lenth,x+20*i,y,1)
    else:
        lengthwise(1,lenth,x,y,1)
        lengthwise(1,lenth,x+20*(lenth-1)+(lenth-1)*6,y,1)
        horizon(1,lenth-1,x,y-20,1)
        horizon(1,lenth-1,x,y+20*lenth,1)
        
######################################################
#随机生成关卡
def random_state():
    x=random.randint(0,30)
    x=int(x/10)
    x=3
    if x==0:#简单多行
        for i in range(6):
            horizon(1,int(35/(i+1)),10,300+i*30,i+1)
        for i in range(6):
            horizon(1,int(5*(i+1)),10,480+i*30,6-i)
        #horizon(3,35,10,600,1)
    elif x==1:#几何图形
        for j in range(3):
            for i in range(5):
                x=random.randint(180,200)
                y=random.randint(100,170)
                trapezoid(70+x*i,170+y*j,3+i%2,2,i%2)
        for i in range(5):
            if i == 2:
                diomond(50+i*200,600,3)
            else:
                diomond(50+i*200,600,2)
            
    elif x==2:#生成网状
        #基本6根线
        cross(280,150,10,0)
        cross(680,150,10,1)
        horizon(1,12,110,360,1)
        horizon(1,12,520,360,1)
        cross(460,400,12,1)
        cross(500,400,12,0)
        #装饰线(内层)
        horizon(1,6,405,248,1)
        horizon(1,6,405,484,1)
        cross(600,270,4,0)
        cross(660,390,4,1)
        cross(300,390,4,0)
        cross(360,270,4,1)
        #装饰线(外层)
        horizon(1,10,345,185,1)
        horizon(1,10,345,550,1)
        cross(660,195,8,0)
        cross(800,390,8,1)
        cross(160,390,8,0)
        cross(300,200,8,1)
    elif x==3:#矩阵
        for i in range(3):
            square(80+i*300,350,10,0)
        for i in range(3):
            square(135+i*300,380,6,0)
        for i in range(3):
            square(185+i*300,400,4,1)
        horizon(1,35,10,300,1)
        horizon(1,35,10,580,1)
    elif x== 4:#完全随机
        randompic(150)
        
##########################################################
#计分函数
def score_show():
#显示分数
    for x,i in enumerate(score_list):
        if i.time!=0:
            i.time-=1
            text = font_s.render(str(i.point), True, 'white')
            screen.blit(text, (i.x, i.y))
        else:
            del score_list[x]
    return
#########################################################

#开始循环
def start_cilcle():
    Start=True
    while Start:    
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Start = False
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    verx=mouse_x-balls[0].pos[0]
                    very=mouse_y-balls[0].pos[1]
    
                    #判断速度
                    if verx/30<10 and verx/30 > -10:
                        balls[0].speed[0]=verx/30
                    else:
                         if verx>0: balls[0].speed[0]=10
                         else: balls[0].speed[0]=-10
                         
                    if very/20<10 and very/20 > -10:
                        balls[0].speed[1]=very/20
                    else:
                        if very>0:  balls[0].speed[1]=10
                        else: balls[0].speed[1]=-10
                    return
                elif event.type == pygame.MOUSEMOTION:
                    # 渲染背景
                    screen.blit(background, (0, 0))   
                    # 渲染游戏元素
                    for brick in bricks:
                        brick.draw(screen)
                    balls[0].draw(screen)
                    text = font.render("click to start", True, 'white')
                    screen.blit(text, (350, 0))
                    line=Line()
                    line.update_end_pos(list(event.pos))
                    line.draw(screen)
                    #渲染角色
                    player.draw(screen)
                    enemy.draw(screen)
                    for i,item in enumerate(items):
                        item.draw(screen,20+i*40)
                    pygame.display.update()
                    
                    
#玩家循环
def main_cilcle():
    
    main_game=True
    while main_game:
        #加载BGM
        if pygame.mixer.music.get_busy() == False: #检查是否正在播放音乐
            pygame.mixer.music.play()
        # 渲染背景
        screen.blit(background, (0, 0))
        for brick in bricks:
            brick.draw(screen)
        for i,all_ball in enumerate(balls):
            # 渲染游戏元素
            all_ball.draw(screen)
            #碰撞检测
            all_ball.check_brick_collision(bricks)
            all_ball.check_walls(screen_size)
            #更新位置
            all_ball.update_position()
            #落到底时结束
            if all_ball.pos[1] > screen_size[1] - all_ball.radius:
                del balls[i]
            if len(balls)==0:
                main_game= False
        
        #渲染角色
        player.draw(screen)
        enemy.draw(screen)
        #渲染道具
        for i,item in enumerate(items):
            item.draw(screen,20+i*40)
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if item.type==1:
                        item.use(enemy)
                    else:
                        item.use(player)
        #渲染分数
        score_show()
        #刷新频率
        pygame.display.update()
        time.sleep(1/60)
        
        
#敌方行动回合
def enemy_acting():
    #随机发射
    new_ball = Ball(screen_size,500,150)
    balls.append(new_ball)
    new_ball.speed=[random.randint(-10,10),random.randint(-10,10)]
    main_game=True
    while main_game:
        if pygame.mixer.music.get_busy() == False: #检查是否正在播放音乐
            pygame.mixer.music.play()
        # 渲染背景
        screen.blit(background, (0, 0))
        for brick in bricks:
            brick.draw(screen)
        for i,all_ball in enumerate(balls):
            # 渲染游戏元素
            all_ball.draw(screen)
            #碰撞检测
            all_ball.check_brick_collision(bricks)
            all_ball.check_walls(screen_size)
            #更新位置
            all_ball.update_position()
            #落到底时结束
            if all_ball.pos[1] > screen_size[1] - all_ball.radius:
                del balls[i]
            if len(balls)==0:
                main_game= False
        #渲染角色
        player.draw(screen)
        enemy.draw(screen)
        #渲染提示
        text = font.render("Enemy acting", True, 'red')
        screen.blit(text, (375, 0))
        #渲染道具
        for i,item in enumerate(items):
            item.draw(screen,20+i*40)
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if item.type==1:
                        item.use(enemy)
                    else:
                        item.use(player)
                    item.use(player)
        #显示得分
        score_show()
        #刷新频率
        pygame.display.update()
        time.sleep(1/200)

#受击演示
def acting(x,damage):
    #建立缓冲
    #显示当前血量
    tem_screen.blit(blackground, (0, 0))
    #角色显示
    tem_screen.blit(x.big_image,(430,200))
    #生命值显示
    text = font.render("Health:"+str(x.health), True, 'red')
    tem_screen.blit(text, (400, 350))
    pygame.display.update()
    #显示受击血量
    text = font.render('-'+str(x.damage)+'x'+str(score/10), True, 'red')
    tem_screen.blit(text, (600, 300))
    #展示受击动画
    acting_more()
    
    #显示受击后血量
    x.health-=damage
    screen.blit(blackground, (0, 0))
    pygame.display.update()
    #角色显示
    screen.blit(x.big_image,(430,200))
    text = font.render("Health:"+str(x.health), True, 'red')
    screen.blit(text, (400, 350))
    
    pygame.display.update()
    time.sleep(1)

def acting_more():
    pygame.mixer.Sound.play(attack)
    for i in damage_list:
        screen.blit(tem_screen,(0,0))
        screen.blit(i,(430,150))
        pygame.display.update()
        time.sleep(1/10)
        
#回合结束奖励动画
def reword():
    x=random.randint(0,39)
    x=int(x/10)
    pygame.mixer.Sound.play(gain)
    if x==0:
        #生成
        new_food = HPbottle(20)
        items.append(new_food)
        screen.blit(blackground, (0, 0))
        pygame.display.update()
        #展示
        big_image=pygame.image.load('image/HP.png')
        big_image=pygame.transform.scale(big_image,(100,80))
        screen.blit(big_image,(450,200))
        text = font_sB.render("Gain Healing Potion", True, 'yellow')
        text2 = font_sc.render("Restores 20 health points", True, 'grey')
        screen.blit(text, (155, 300))
        screen.blit(text2, (370, 400))
        pygame.display.update()
        print('获得道具：回复药')
        close=True
        while close:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:  
                    return
            time.sleep(0.5)
    elif x==1:
        #生成
        new_weapon = Weapon(20)
        items.append(new_weapon)
        screen.blit(blackground, (0, 0))
        pygame.display.update()
        #展示
        big_image=pygame.image.load('image/gun.png')
        big_image=pygame.transform.scale(big_image,(50,180))
        screen.blit(big_image,(700,200))
        text = font_sB.render("Gain a gun", True, 'yellow')
        text2 = font_sc.render("Deals 20 damage to enemies", True, 'grey')
        screen.blit(text, (305, 300))
        screen.blit(text2, (370, 400))
        pygame.display.update()
        print('获得道具：枪')
        close=True
        while close:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:    
                    return
            time.sleep(0.5)
    elif x==2:
        new_bless = Bless(2)
        items.append(new_bless)
        screen.blit(blackground, (0, 0))
        pygame.display.update()
        screen.blit(new_bless.image,(480,200))
        big_image=pygame.image.load('image/StrengthPotion.png')
        big_image=pygame.transform.scale(big_image,(100,80))
        screen.blit(big_image,(450,200))
        text = font_sB.render("Gain Strength Potion", True, 'yellow')
        text2 = font_sc.render("Increases base damage by 2", True, 'grey')
        screen.blit(text, (155, 300))
        screen.blit(text2, (370, 400))
        pygame.display.update()
        print('获得道具：力量药水')
        close=True
        while close:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:  
                    return
            time.sleep(0.5)
    elif x==3:
        new_Shields = Shields(1)
        items.append(new_Shields)
        screen.blit(blackground, (0, 0))
        pygame.display.update()
        big_image=pygame.image.load('image/Shields.png')
        big_image=pygame.transform.scale(big_image,(100,80))
        screen.blit(big_image,(450,200))
        text = font_sB.render("Gain Shield Potion", True, 'yellow')
        text2 = font_sc.render("Increases shield value by 20", True, 'grey')
        screen.blit(text, (155, 300))
        screen.blit(text2, (370, 400))
        pygame.display.update()
        print('获得道具：护盾药水')
        close=True
        while close:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:   
                    return
            time.sleep(0.5)

#新关卡
def new_game():
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
                main()
                return
    
def end_game():
    if enemy.health<=0:
        while True:
            screen.blit(background, (0, 0))
            text = font_sB.render("GOOD GAME", True, 'yellow')
            screen.blit(text, (300, 300))
            pygame.display.update()
            time.sleep(1)
    elif player.health<=0:
        while True:
            screen.blit(background, (0, 0))
            text = font_scB.render("YOU DEAD", True, 'red')
            screen.blit(text, (300, 300))
            pygame.display.update() 
            time.sleep(1)
            new_game()
###########################################################
def main():
    while player.health>0 and enemy.health>0:
        global score
        score=0
        #渲染道具
        new_ball = Ball(screen_size,500,150)
        balls.append(new_ball)
        #生成砖块
        del bricks[:]
        random_state()
        #加载GBM
        if pygame.mixer.music.get_busy() == False: #检查是否正在播放音乐
            pygame.mixer.music.play()
        #开始界面循环
        start_cilcle()
        # 游戏主循环
        main_cilcle()
        acting(enemy,int(player.damage*score/10))
        #再次生成砖块
        del bricks[:]
        random_state()
        score=0
        #敌方行动
        enemy_acting()
        acting(player,int(enemy.damage*score/10))
        #游戏结束动画
        end_game()
        reword()
        score_list.clear()
    
main()



WEfw4