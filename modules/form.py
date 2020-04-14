import pygame
import random
import math
from modules.triangle import Triangle
from modules.ressources import Ressources

class Form:
    def __init__(self,type,pos,color):
        self.type = type
        self.pos = pos
        self.color = color
        self.boxes = []
        self.size = 0
        self.boxNumber = (0,0)
        self.movable = True
        self.selected = False
        self.selectedBox = 0
        self.reseting = True
        
    def boxesDefinition(self):
        boxes = Ressources.getGameObjectType(self.type)[0]
        types = Ressources.getGameObjectType(self.type)[1]
        self.boxes = []
        for i in range(len(boxes)):
            self.boxes.append(Triangle(self,Ressources.screen,types[i],boxes[i],self.color))
            
    def restTo(self,pos,v0):
        self.reseting = True
        self.selected = False
        stepX = (pos[0] - self.pos[0])*v0
        stepY = (pos[1] - self.pos[1])*v0
        self.pos = (self.pos[0] + stepX , self.pos[1] + stepY)
        self.draw()
        if(self.pos[0] > (pos[0]-1) and self.pos[0] < (pos[0]+1) and  self.pos[1] > (pos[1]-1) and self.pos[1] < (pos[1]+1) ):
            self.pos = (pos[0],pos[1])
            self.reseting = False
            self.movable = True
            return True
        else:
            return False
            
    def draw(self,pos=-1):
        if(pos != -1):
            self.pos = pos        
        for i in range(len(self.boxes)):
            self.boxes[i].draw()
                    
    def generateAlea(self,corlorRange=range(4),type = -1):
        if(type == -1):
            self.type = random.randrange(1,14,1)
        else:
            self.type = type
        self.color = random.choice(corlorRange)
        self.boxesDefinition()
        self.size = Ressources.getGameObjectType(self.type)[2]
        return self.color
    
    def isIN(self,pixelPos):
        normalizedX = pixelPos[0] - self.pos[0]
        normalizedY = pixelPos[1] - self.pos[1]
        
        for i in range(len(self.boxes)):
            NX = normalizedX - self.boxes[i].pos[0]
            NY = normalizedY - self.boxes[i].pos[1]
            if(self.boxes[i].isIN((NX,NY))):
                return True
        return False
        