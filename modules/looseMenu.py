import pygame
from modules.ressources import Ressources

class LooseMenu:
    def __init__(self):
        self.buttonWidth = Ressources.screenWidth * 2 // 5
        self.buttonHeight = Ressources.screenHeight // 12
        self.screen = Ressources.screen
        self.logoOff = pygame.image.load('assets/Logo/Trizzle.png').convert_alpha()
        self.logoOn = pygame.image.load('assets/Logo/light.png').convert_alpha()
        self.sound = pygame.mixer.Sound("assets/sounds/logo.wav")
        self.soundNeon = pygame.mixer.Sound("assets/sounds/neon.wav")
        self.soundFailure = pygame.mixer.Sound("assets/sounds/failure2.wav")
        self.first = True
        self.screen = Ressources.screen
        self.scWidth = Ressources.screenWidth
        self.scHeight = Ressources.screenHeight
        propLH = 327 / 103
        self.LogoWidth = int((self.scWidth*propLH) // 5)
        self.LogoHeight = int((self.scHeight) // 5)
        self.logoOff = pygame.transform.scale(self.logoOff, (self.LogoWidth, self.LogoHeight))
        self.logoOn = pygame.transform.scale(self.logoOn, (self.LogoWidth, self.LogoHeight))
        self.numberFont = Ressources.fonts[1]
        self.stringFont = Ressources.fonts[0]
        retrayImgs = [
            pygame.image.load('assets/imgs/retry.png').convert_alpha(),
            pygame.image.load('assets/imgs/retrySel.png').convert_alpha()
        ]
        exitImgs = [
            pygame.image.load('assets/imgs/exit.png').convert_alpha(),
            pygame.image.load('assets/imgs/exitSel.png').convert_alpha()
        ]
        buttonsWidth = self.scWidth // 7
        buttonsHeight = buttonsWidth
        buttonY = (self.scHeight*3) // 5
        buttonX = (self.scWidth) * 2 // 5 - buttonsWidth
        pos1 = (buttonX, buttonY)
        pos2 = (buttonX + buttonsWidth + (self.scWidth) // 5, buttonY)
        self.buttons = [
            [buttonsWidth, buttonsHeight, pos1,exitImgs,0,(pos1[0] + buttonsWidth, pos1[1] + buttonsHeight),self.exit],
            [buttonsWidth, buttonsHeight, pos2,retrayImgs,0,(pos2[0] + buttonsWidth, pos2[1] + buttonsHeight),self.retry]
        ]
        self.i = 0
        
    def draw(self):
        self.animation()
        color = (255,255,255)
        text = self.stringFont.render("Score :", True, color)
        textScore = self.numberFont.render(str(Ressources.score), True, color)
        pos = (((self.scWidth * 9) // 20) - (text.get_width() // 2) - textScore.get_width(), (self.scHeight // 2) - (text.get_height() // 2))
        self.screen.blit(text,pos)
        pos = (pos[0] + text.get_width() + (self.scWidth // 10), pos[1])
        self.screen.blit(textScore,pos)
        for button in self.buttons:
            self.drawButton(button[0],button[1],button[2],button[3],button[4])
    def drawButton(self,width,height,pos,imgs,sel):
        img = pygame.transform.scale(imgs[sel], (width, height))
        self.screen.blit(img,pos)
    def retry(self):
        Ressources.reset()
        Ressources.mode = 1
        Ressources.rend.genOptions()
        Ressources.rend.blitOptions()
    def exit(self):
        Ressources.reset()
        Ressources.mode = 0
        
    def inButtonBox(self,pos,index):
        x = pos[0]
        y = pos[1]
        xinf = self.buttons[index][2][0]
        yinf = self.buttons[index][2][1]
        xlim = self.buttons[index][5][0]
        ylim = self.buttons[index][5][1]
        if( x >= xinf and x <= xlim and y >= yinf and y <= ylim):
            return True    
    def animation(self):
        if(self.first):
            self.soundFailure.play()
            temp = pygame.Surface((self.scWidth, self.scHeight)).convert()
            temp.blit(self.screen, (0, 0))
            for i in range(255):   
                self.screen.fill((0,0,0))
                temp.set_alpha(255-i)
                self.screen.blit(temp, (0,0))
                pygame.display.flip()
                pygame.time.delay(1)
        self.screen.fill((0,0,0))
        if(self.first):
            self.sound.play()
            for i in range(100):
                LogoWidth = int((self.LogoWidth*i) // 100)
                LogoHeight = int((self.LogoHeight*i) // 100)
                Logo = pygame.transform.scale(self.logoOff, (LogoWidth, LogoHeight))
                self.screen.blit(Logo,(self.scWidth // 2 - LogoWidth //2, self.scHeight // 3 -  self.LogoHeight //2))
                pygame.display.flip()
                pygame.time.delay(1)
        i = self.i / 100
        intI = int(i)
        if(intI < 10 or intI == 12):
            self.screen.blit(self.logoOff,(self.scWidth // 2 - self.LogoWidth //2, self.scHeight // 3 -  self.LogoHeight //2))
        if(intI == 10 or intI == 11 or intI > 12):
            self.screen.blit(self.logoOn,(self.scWidth // 2 - self.LogoWidth //2, self.scHeight // 3 -  self.LogoHeight //2))
        if(intI == 10):
            self.soundNeon.play()
        self.first = False
        if(self.i < 1500):
            self.i = self.i + 1
        
    def reset(self):
        self.first = True
        self.i = 0
        