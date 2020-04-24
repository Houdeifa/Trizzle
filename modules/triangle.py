import pygame
from modules.ressources import Ressources
class Triangle:
    def __init__(self,parent = 0,screen=0,type = 1,pos = (0,0),color=-1):
        self.type = type
        self.pos = pos
        self.color = color
        self.parent = parent
        self.screen = screen
        self.destoyed = False
    
    
    def draw(self,pos=-1,opacity = -1):
        if(pos != -1):
            self.pos = pos
        GTypes = [Ressources.down,Ressources.up]
        getTypes = [Ressources.downs,Ressources.ups]
        if(self.color == -1):
            img = GTypes[self.type]
            self.screen.blit(GTypes[self.type],(self.pos[0]+self.parent.pos[0],self.pos[1]+self.parent.pos[1]))
        else:
            img = getTypes[self.type][self.color]
            if(opacity != -1):
                self.blit_alpha(self.screen,img,(self.pos[0]+self.parent.pos[0],self.pos[1]+self.parent.pos[1]),opacity)
            else:
                self.screen.blit(img,(self.pos[0]+self.parent.pos[0],self.pos[1]+self.parent.pos[1]))
    
    def isIN(self,pos):
        NormalizedX = pos[0]
        NormalizedY = pos[1]
        if(NormalizedX >= 0 and NormalizedX <= Ressources.trWidth and NormalizedY >= 0 and NormalizedY <= Ressources.trHeight):
            NormalizedX = NormalizedX / Ressources.trWidth
            NormalizedY = NormalizedY / Ressources.trHeight
            T = NormalizedX - 0.5
            if(T < 0):
                T = T * -1
            T = T * 2
            if(self.type == 0):
                T = (1 - T)
                if(NormalizedY <= T):
                    return True
                else:
                    return False
            else:
                if(NormalizedY >= T):
                    return True
                else:
                    return False
        else:
            return False
    def destoy(self):
        self.destoyed = True
        
    def blit_alpha(self,target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
            