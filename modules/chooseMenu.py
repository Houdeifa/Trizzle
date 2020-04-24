import pygame
from modules.ressources import Ressources

class ChooseMenu:
    def __init__(self):
        self.buttonWidth = Ressources.screenWidth * 2 // 5
        self.buttonHeight = Ressources.screenHeight // 12
        self.screen = Ressources.screen
        self.font = Ressources.fonts[0]
        self.clickSound = pygame.mixer.Sound("assets/sounds/selected.wav")
        self.mouseOverSound = pygame.mixer.Sound("assets/sounds/Over.wav")
        y = Ressources.screenHeight // 3 - self.buttonHeight // 2
        x = Ressources.screenWidth //2 - self.buttonWidth //2 
        pos = (x,y)
        limits = (x + self.buttonWidth,y + self.buttonHeight)
        self.buttons = [
            [pos,"Continue",limits,1,self.continue_]
        ]
        y = y + self.buttonHeight + 20
        pos = (x,y)
        limits = (x + self.buttonWidth,y + self.buttonHeight)
        status = 0
        self.buttons.append([pos,"New Game",limits,status,self.new_game])
        y = y + self.buttonHeight + 20
        pos = (x,y)
        limits = (x + self.buttonWidth,y + self.buttonHeight)
        self.buttons.append([pos,"Statistics",limits,status,self.statistics])
        y = Ressources.screenHeight -  self.buttonHeight - 50
        pos = (x,y)
        limits = (x + self.buttonWidth,y + self.buttonHeight)
        self.buttons.append([pos,"Quit",limits,status,self.quit])
        
    def draw(self):
        self.screen.fill((0,0,0))
        for button in self.buttons:
            self.createButton(button[0],self.buttonWidth,self.buttonHeight,button[1],button[3])
    def inButtonBox(self,pos,index):
        x = pos[0]
        y = pos[1]
        xinf = self.buttons[index][0][0]
        yinf = self.buttons[index][0][1]
        xlim = self.buttons[index][2][0]
        ylim = self.buttons[index][2][1]
        if( x >= xinf and x <= xlim and y >= yinf and y <= ylim):
            return True
        return False
        
    def createButton(self,pos,width,height,text,status):
        self.drawSquare(pos,width,height)
        if(status == 0): # activated not selected
            color = (0, 128, 0)
        elif(status == 1): #desactivated
            color = (128, 128, 128)
        elif(status == 2): #mouseOver
            color = (0, 255, 0)
        text = self.font.render(text, True, color)
        pos = (pos[0] + width // 2 - text.get_width() // 2,pos[1] + height // 2 - text.get_height() // 2)
        self.screen.blit(text,pos)
        
    def drawSquare(self,pos,width,height):
        #drawing the square where Object are generated
        points = [(0 ,0), (width,0), (width, height),(0, height)]
        size = (width+2,height+2)
        lines_closed = pygame.Surface(size)
        RED = pygame.Color(255, 0, 0) 
        pygame.draw.lines(lines_closed, RED, True, points)
        self.screen.blit(lines_closed, pos)
    def quit(self):
        Ressources.running = False
    def continue_(self):
        Ressources.mode = 1
        self.clickSound.play()
        Ressources.rend.blitOptions()
    def new_game(self):
        self.clickSound.play()
        Ressources.mode = 1
        Ressources.rend.genOptions()
        Ressources.rend.blitOptions()
        Ressources.rend.bg.reset()
        Ressources.played = []
    def statistics(self):
        x = 0