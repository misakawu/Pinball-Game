import pygame
import math
pygame.init()
pygame.mixer.init()
heal=pygame.mixer.Sound('sound/回复.wav')
gain=pygame.mixer.Sound('sound/获得.wav')
gun=pygame.mixer.Sound('sound/枪攻击.wav')
potion=pygame.mixer.Sound('sound/使用药水.wav')
attack=pygame.mixer.Sound('sound/一般攻击.wav')
BGM=pygame.mixer.music.load('sound/BGM.mp3')

font = pygame.font.Font(None, 50)
font_s = pygame.font.Font(None, 30)
font_sB = pygame.font.Font(None, 100)
font_sc = pygame.font.Font('front/卡通.ttf',30)
font_scB = pygame.font.Font('front/卡通.ttf',100)

screen_size = (1000, 700)
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
        health_num = font_s.render('HP:'+str(self.health), True, 'red')
        damage_num = font_s.render('DPS:'+str(self.damage), True, 'yellow')
        surface.blit(health_num, (70, 10))
        surface.blit(damage_num, (70, 40))

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
        health_num = font_s.render('HP:'+str(self.health), True, 'red')
        damage_num = font_s.render('DPS:'+str(self.damage), True, 'yellow')
        surface.blit(health_num, (screen_size[0]-150, 10))
        surface.blit(damage_num, (screen_size[0]-150, 35)) 

############障碍物#############

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
    

#############道具################
#回复药
class HPbottle:
    def __init__(self,point):
        self.point=point
        self.image=pygame.image.load('image/HP.png')
        self.type=0#回复型
        
    def draw(self,surface,x):
        surface.blit(self.image, (int(x), 80))
        
    def use(self,x,items):
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
        
    def use(self,x,items):
        if x.health>=x.health-self.damage:
            x.health-=self.damage
            print('使用道具：枪，造成伤害',self.damage)
        else:
            x.health=0
            print('使用道具：枪，造成伤害',x.health)
        pygame.mixer.Sound.play(gun)
        items.pop(0)
        

#力量药剂
class Bless:
    def __init__(self,point):
        self.point=point
        self.image=pygame.image.load('image/StrengthPotion.png')
        self.type=0#回复型
        
    def draw(self,surface,x):
        surface.blit(self.image, (int(x), 80))
        
    def use(self,x,items):
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
        
    def use(self,x,items):
        x.health+=self.point
        print('使用道具：护盾药水，血量增加',self.point)
        pygame.mixer.Sound.play(potion)
        items.pop(0)
        

#线段类
class Line:
    def __init__(self):
        self.start_pos = [500,150]
        self.end_pos = [500,150]
        self.color = 'white'
        self.width = 1
    def update_end_pos(self, end_pos):
        self.end_pos = end_pos
    def draw(self,surface):
        pygame.draw.line(surface, self.color, self.start_pos, self.end_pos, self.width)
    def draw_parabola_trajectory(self, v0,surface):
        x0, y0 = 500, 150 # 起点坐标
        if self.end_pos[0]-x0 !=0:
            tan_a=(self.end_pos[1]-y0)/(self.end_pos[0]-x0)
            g = 0.4 # 重力加速度
            a = math.atan(abs(tan_a)) # 抛射角度（弧度制）
            t = 0
            t_step = 1 # 时间间隔
            points = [] # 保存绘制点的列表
            while True:
                if self.end_pos[0]<500:# 计算当前位置的x坐标
                    x = x0 - v0 * math.cos(a) * t 
                else:
                    x = x0 + v0 * math.cos(a) * t 
                if self.end_pos[1]>150:# 计算当前位置的y坐标
                    y = y0 + v0 * math.sin(a) * t + 0.5 * g * t ** 2
                else:
                    y = y0 - v0 * math.sin(a) * t + 0.5 * g * t ** 2 
                    
                point = [x, y] # 将坐标转换为整数
                points.append(point) # 将坐标添加到列表中
                if point[1] >= screen_size[1]: # 如果到达地面，则退出循环
                    break
                if point[1] <= 100: # 如果到达地面，则退出循环
                    break
                t += t_step # 更新时间值
            # 绘制抛物线
            pygame.draw.lines(surface, self.color, False, points, 2)
            
        else:
            return
    
#得分类
class ScorePoint:
    def __init__(self,x,y,point):
        self.x=x
        self.y=y
        self.point=point
        self.time=25
        
        
        
        
        