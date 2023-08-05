import pygame, os, random
pygame.init()
SW=875
SH=750
LV=50
FPS=30
gpow=3
money=150
clock=pygame.time.Clock()
screen=pygame.display.set_mode((SW,SH))
creating_timer=0
bosscd=1250
#font
font=pygame.font.SysFont("Lucida Sans", 25)
bigfont=pygame.font.SysFont("Lucida Sans", 70)
#pic
ppic=pygame.image.load(os.path.join("tank.png")).convert_alpha()
ppic=pygame.transform.scale(ppic, (200,100))
apic=pygame.image.load(os.path.join("ball.png")).convert_alpha()
apic=pygame.transform.scale(apic, (25,25))
epic=pygame.image.load(os.path.join("zombie.png")).convert_alpha()
epic=pygame.transform.scale(epic, (50,65))
panelpic=pygame.image.load(os.path.join("block.png")).convert_alpha()
panelpic=pygame.transform.scale(panelpic, (45,45))
#mus
alarmsnd=pygame.mixer.Sound(os.path.join("warning.mp3"))
# game
def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)
    screen.blit(img, (x,y))

def draw_obj():
    pygame.draw.rect(screen, (100,100,100),(0,0,SW,50))
    draw_text("LV: "+str(LV),font,(0,255,0),25,2)
    draw_text("ZOMBIE: "+str(len(enemyg)),font,(255,255,0),125,2)
    draw_text(("BOSS C/D {"+str(bosscd//60)+" : "+str(bosscd%60)+"}"),font,(255,255,0),275,2)
    draw_text("MONEY:"+str(money)+"$",font,(255,255,0),525,2)
    draw_text("POWER "+str(gpow),font,(0,255,0),2,50)
    draw_text("FPS: "+str(FPS),font,(0,255,0),2,75)
class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=ppic
        self.rect=self.image.get_rect()
        self.mx=0
        self.my=random.choice((-6,6))
        self.shoot=0
        self.gpow=gpow
        global money
        while not pygame.mouse.get_pressed()[0]:
            screen.fill((0,0,0))
            draw_obj()
            draw_text("#click mouse button right to cencel^_^",font,(255,255,0),SW//3,150)
            if pygame.mouse.get_pressed()[2] and len(gung)>0:
                self.kill()
                self.create=False
                break
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    global run
                    run=False
                    break
            self.rect.center=pygame.mouse.get_pos()
            pygame.draw.circle(screen, (25,25,25), (self.rect.centerx,self.rect.centery), self.gpow*50*money//100)
            gung.draw(screen)
            pygame.display.update()
            self.level=money//100
            self.create=True
            self.click=True
        try:
            if self.click==True:
                money-=(self.level-1)*100
                self.create=True
            else:
                self.create=False
        except:
            money-=(self.level-1)*100
            self.create=True
        self.x=self.rect.centerx
    def move(self):
        mpos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            pygame.draw.circle(screen, (25,25,25), (self.rect.centerx,self.rect.centery), self.gpow*50*money//100)
        if self.create==False:
            self.kill()
        self.rect.x-=int(self.mx)
        self.mx*=0.2
        if self.rect.y<=0 or self.rect.bottom>=SH:
            self.my*=-1
        self.rect.y+=self.my
        self.rect.x+=2
        self.shoot+=10
        if self.shoot>=50:
            self.mx=8
            self.shoot=0
            ammo=Ammo(self.rect.centerx,self.rect.centery,random.choice((-self.gpow, self.gpow*self.level, self.gpow*self.level, self.gpow*self.level, self.gpow*self.level, self.gpow*self.level, self.gpow*self.level, self.gpow*self.level, self.gpow*self.level, self.gpow*self.level, self.gpow)))
            ammog.add(ammo)
        if self.rect.centerx>self.x:
            self.rect.centerx=self.x

class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y, mx):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(apic, (25,25))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.centery=y
        self.mx=int(mx)
        self.life=50
    def move(self):
        self.rect.x+=self.mx
        self.life-=1
        if self.life<=0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, lv, boss):
        pygame.sprite.Sprite.__init__(self)
        self.image=epic
        self.boss=boss
        if self.boss==True:
            self.spd=lv//50-1
            self.image=pygame.transform.scale(self.image, (100,200))
            self.my=1
        else:
            self.spd=lv//50
            self.image=pygame.transform.scale(self.image, (50,100))
            self.my=0
        self.rect=self.image.get_rect()
        self.rect.x=SW+random.randrange(25,100)
        self.rect.centery=random.randrange(50,SH-50)
        self.lv=lv+10
        self.life=lv+10
        if self.boss==True:
            self.lv+=100
            self.life+=100
            self.rect.x-=50
    def move(self):
        self.rect.y+=self.my
        if self.rect.centery>=SH or self.rect.centery<=0:
            self.my*=-1
        self.rect.x-=self.spd
        if pygame.sprite.spritecollide(self, ammog,False):
            self.life-=1
            self.rect.x+=1
        if self.life<=0:
            global LV, gpow, money
            LV+=3
            if self.boss==False:
                gpow+=self.lv//50
                money+=self.lv//2
            self.kill()
            if money>=100:
                gun=Gun()
                gung.add(gun)

class Fps(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=panelpic
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=SH-45
        self.updfps=1
    def move(self):
        mpos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            global FPS
            FPS+=self.updfps
            if FPS>=40 or FPS<=10:
                self.updfps*=-1

gung=pygame.sprite.Group()
ammog=pygame.sprite.Group()
enemyg=pygame.sprite.Group()
screen.fill((0,0,0))
draw_obj()
pygame.display.update()
gun=Gun()
gung.add(gun)
b=False
enemy=Enemy(LV, b)
enemyg.add(enemy)
panel=Fps()
show_inst=True
run=True
while run:
    creating_timer+=1
    bosscd-=1
    clock.tick(FPS)
    screen.fill((0,0,0))
    key=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    if bosscd<=0:
        bosscd=1250
        b=True
        enemy=Enemy(LV,b)
        enemyg.add(enemy)
    if key[pygame.K_p] and creating_timer>=100:
        creating_timer=0
        b=False
        enemy=Enemy(LV,b)
        enemyg.add(enemy)
    
    if (key[pygame.K_LSHIFT] and show_inst==True) or (key[pygame.K_RSHIFT] and show_inst==True):
        show_inst=False
    
    #update sprite
    for g in gung:
        g.move()
    gung.draw(screen)
    for a in ammog:
        a.move()
    ammog.draw(screen)
    for e in enemyg:
        e.move()
    enemyg.draw(screen)
    panel.move()
    screen.blit(panel.image,panel.rect)
    if show_inst==True:
        draw_text("press shift before start! :)",font, (255,0,0),50,SH//3)
        draw_text("press p to create enemies! Have fun!",font, (255,0,0),50,SH//3+50)
        draw_text("move your mouse to the white box to change FPS >:o",font, (255,255,0),50,SH//3+75)
    draw_obj()
    pygame.display.update()











pygame.quit()
