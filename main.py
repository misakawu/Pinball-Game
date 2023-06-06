import pygame
import random
import time
import sys
import math
from item_sprites import *
from create_map import *

# 定义小球类
class Ball:
    def __init__(self,screen_size,x,y):
        #(x,y)向右下为正
        self.pos = [x, y]  # 小球初始位置
        self.speed = [0,0]  # 小球初始速度
        self.radius = 8  # 小球半径
        self.gy=0.4
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
            self.speed[1] += 0.4
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
    

#
##线段类
#class Line:
#    def __init__(self):
#        self.start_pos = [500,150]
#        self.end_pos = [500,150]
#        self.color = 'white'
#        self.width = 1
#    def update_end_pos(self, end_pos):
#        self.end_pos = end_pos
#    def draw(self,surface):
#        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)
#    def draw_parabola_trajectory(self, v0):
#        x0, y0 = 500, 150 # 起点坐标
#        if self.end_pos[0]-x0 !=0:
#            tan_a=(self.end_pos[1]-y0)/(self.end_pos[0]-x0)
#            g = 0.4 # 重力加速度
#            a = math.atan(abs(tan_a)) # 抛射角度（弧度制）
#            t = 0
#            t_step = 1 # 时间间隔
#            points = [] # 保存绘制点的列表
#            while True:
#                if self.end_pos[0]<500:# 计算当前位置的x坐标
#                    x = x0 - v0 * math.cos(a) * t 
#                else:
#                    x = x0 + v0 * math.cos(a) * t 
#                if self.end_pos[1]>150:# 计算当前位置的y坐标
#                    y = y0 + v0 * math.sin(a) * t + 0.5 * g * t ** 2
#                else:
#                    y = y0 - v0 * math.sin(a) * t + 0.5 * g * t ** 2 
#                    
#                point = [x, y] # 将坐标转换为整数
#                points.append(point) # 将坐标添加到列表中
#                if point[1] >= screen_size[1]: # 如果到达地面，则退出循环
#                    break
#                if point[1] <= 100: # 如果到达地面，则退出循环
#                    break
#                t += t_step # 更新时间值
#            # 绘制抛物线
#            pygame.draw.lines(screen, self.color, False, points, 2)
#            
#        else:
#            return
#        
#    
##得分类
#class ScorePoint:
#    def __init__(self,x,y,point):
#        self.x=x
#        self.y=y
#        self.point=point
#        self.time=25

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
food=Shields(20)
items.append(food)
#敌人
enemy = Enemy()
#得分
score = 0
score_list = []

#######################################################
#随机生成关卡
def random_state():
    x=random.randint(0,499)
    x=int(x/100)
    if x==0:#简单多行
        for i in range(6):
            horizon(1,int(35/(i+1)),10,300+i*30,i+1,bricks)
        for i in range(6):
            horizon(1,int(5*(i+1)),10,480+i*30,6-i,bricks)
        #horizon(3,35,10,600,1)
    elif x==1:#几何图形
        for j in range(3):
            for i in range(5):
                x=random.randint(180,200)
                y=random.randint(100,170)
                trapezoid(70+x*i,170+y*j,3+i%2,2,i%2,bricks)
        for i in range(5):
            if i == 2:
                diomond(50+i*200,600,3,bricks)
            else:
                diomond(50+i*200,600,2,bricks)
            
    elif x==2:#生成网状
        #基本6根线
        cross(280,150,10,0,bricks)
        cross(680,150,10,1,bricks)
        horizon(1,12,110,360,1,bricks)
        horizon(1,12,520,360,1,bricks)
        cross(460,400,12,1,bricks)
        cross(500,400,12,0,bricks)
        #装饰线(内层)
        horizon(1,6,405,248,1,bricks)
        horizon(1,6,405,484,1,bricks)
        cross(600,270,4,0,bricks)
        cross(660,390,4,1,bricks)
        cross(300,390,4,0,bricks)
        cross(360,270,4,1,bricks)
        #装饰线(外层)
        horizon(1,10,345,185,1,bricks)
        horizon(1,10,345,550,1,bricks)
        cross(660,195,8,0,bricks)
        cross(800,390,8,1,bricks)
        cross(160,390,8,0,bricks)
        cross(300,200,8,1,bricks)
    elif x==3:#矩阵
        for i in range(3):
            square(80+i*300,350,10,0,bricks)
        for i in range(3):
            square(135+i*300,380,6,0,bricks)
        for i in range(3):
            square(185+i*300,400,4,1,bricks)
        horizon(1,35,10,300,1,bricks)
        horizon(1,35,10,580,1,bricks)
    elif x== 4:#完全随机
        randompic(150,bricks)
        
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
                mouse_x, mouse_y = pygame.mouse.get_pos()
                verx=mouse_x-balls[0].pos[0]
                very=mouse_y-balls[0].pos[1]
                
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if len(items)!=0:
                        if items[0].type==1:
                            items[0].use(enemy,items)
                        else:
                            items[0].use(player,items)
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Start = False
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
                    text = font.render("click to fire", True, 'white')
                    screen.blit(text, (420, 110))
                    #绘制预测抛物线
                    x0,y0=0,0
                    if verx/30<10 and verx/30 > -10:
                        x0=verx/30
                    else:
                         if verx>0: x0=10
                         else: x0=-10
                         
                    if very/20<10 and very/20 > -10:
                        y0=very/20
                    else:
                        if very>0:  y0=10
                        else: y0=-10
                    v=math.sqrt(x0*x0+y0*y0)
                    line=Line()
                    line.update_end_pos(list(event.pos))
                    #line.draw(screen)
                    line.draw_parabola_trajectory(v,screen)
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
                        item.use(enemy,items)
                    else:
                        item.use(player,items)
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
        screen.blit(text, (375, 110))
        #渲染道具
        for i,item in enumerate(items):
            item.draw(screen,20+i*40)
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if item.type==1:
                        item.use(enemy,items)
                    else:
                        item.use(player,items)
                    #item.use(player)
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
    x=random.randint(0,1000)
    x=int(x/300)
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
        if enemy.health<=0:
            end_game(screen,player,enemy)
            main()
        #再次生成砖块
        del bricks[:]
        random_state()
        score=0
        #敌方行动
        enemy_acting()
        acting(player,int(enemy.damage*score/10))
        #游戏结束动画
        x=end_game(screen,player,enemy)
        if x==1:
            main()
        reword()
        score_list.clear()
    
main()



