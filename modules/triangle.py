import pygame
from modules.ressources import Ressources
class Triangle:
    def __init__(self,parent = 0,screen=0,type = 1,pos = (0,0),color=-1):
        self.type = type
        self.pos = pos
        self.color = color
        self.parent = parent
        self.screen = screen
        self.occupied = False
        self.destoyed = False
        self.destoing = False
    
    
    def draw(self,pos=-1):
        if(pos != -1):
            self.pos = pos
        GTypes = [Ressources.down,Ressources.up]
        getTypes = [Ressources.downs,Ressources.ups]
        if(self.color == -1):
            self.screen.blit(GTypes[self.type],(self.pos[0]+self.parent.pos[0],self.pos[1]+self.parent.pos[1]))
        else:
            self.screen.blit(getTypes[self.type][self.color],(self.pos[0]+self.parent.pos[0],self.pos[1]+self.parent.pos[1]))
    
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
            