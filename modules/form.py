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
        self.mouvable = True
        self.disabled = False
        self.selected = False
        self.played = False
        self.playing = False
        self.destoyed = False
        self.PlayedPos = ()
        self.selectedBox = 0
        self.reseting = True
        self.colls = 0
        self.rows = 0
        self.score = 0
        self.iPos = (-1,-1)
        self.optimalSelectionPos = (0,0)
                    
    def boxesDefinition(self):
        types = Ressources.getGameObjectType(self.type)[0]
        self.score = Ressources.getGameObjectType(self.type)[2]
        self.optimalSelectionPos = Ressources.getGameObjectType(self.type)[3]
        self.boxes = []
        for i in range(len(types)):
            if(type(types[i]) == list):
                boxi = []
                for j in range(len(types[i])):
                    if(types[i][j] != -1):
                        x = j * Ressources.trXSpace
                        y = i * Ressources.trYSpace
                        boxi.append(Triangle(self,Ressources.screen,types[i][j],(x,y),self.color))
                    else:
                        boxi.append(-1)
                self.boxes.append(boxi)
            else:
                y = 0
                x = i * Ressources.trXSpace
                self.boxes.append(Triangle(self,Ressources.screen,types[i],(x,y),self.color))
        
        if(type(self.boxes[0])!=list):
            self.colls = len(self.boxes)
            self.rows = 1
        else:
            self.rows = len(self.boxes)
            self.colls = len(self.boxes[0])
                
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
        
    def playTo(self,pos,v0,iPos):
        self.playing = True
        self.selected = False
        self.iPos = iPos
        stepX = (pos[0] - self.pos[0])*v0
        stepY = (pos[1] - self.pos[1])*v0
        self.pos = (self.pos[0] + stepX , self.pos[1] + stepY)
        self.PlayedPos = pos
        self.draw()
        if(self.pos[0] > (pos[0]-1) and self.pos[0] < (pos[0]+1) and  self.pos[1] > (pos[1]-1) and self.pos[1] < (pos[1]+1) ):
            self.pos = (pos[0],pos[1])
            self.reseting = False
            self.mouvable = False
            self.playing = False
            self.played = True
            Ressources.score = Ressources.score + self.score
            return True
        else:
            return False
        
            
    def draw(self,pos=-1):
        if(pos != -1):
            self.pos = pos
        self.destoyed = True
        if(self.disabled):
            self.mouvable = False
            opacity = 128
        else:
            opacity = -1
        for i in range(len(self.boxes)):
            if(type(self.boxes[i]) == list):
                for j in range(len(self.boxes[i])):
                    if(self.boxes[i][j] != -1 and not self.boxes[i][j].destoyed):
                        self.boxes[i][j].draw(-1,opacity)
                        self.destoyed = False
            elif(not self.boxes[i].destoyed):
                self.boxes[i].draw(-1,opacity)
                self.destoyed = False
            
                    
    def generateAlea(self,corlorRange=range(4),type = -1):
        if(type == -1):
            self.type = random.randrange(1,14,1)
        else:
            self.type = type
        self.color = random.choice(corlorRange)
        self.boxesDefinition()
        self.size = Ressources.getGameObjectType(self.type)[1]
        return self.color
    
    def isIN(self,pixelPos):
        normalizedX = pixelPos[0] - self.pos[0]
        normalizedY = pixelPos[1] - self.pos[1]
        for i in range(len(self.boxes)):
            if(type(self.boxes[i]) == list):
                for j in range(len(self.boxes[i])):
                    if(self.boxes[i][j] != -1):
                        NX = normalizedX - self.boxes[i][j].pos[0]
                        NY = normalizedY - self.boxes[i][j].pos[1]
                        if(self.boxes[i][j].isIN((NX,NY))):
                            Ressources.selectedTr = (j,i)
                            return True
            else:
                NX = normalizedX - self.boxes[i].pos[0]
                NY = normalizedY - self.boxes[i].pos[1]
                if(self.boxes[i].isIN((NX,NY))):
                    Ressources.selectedTr = (i,-1)
                    return True
                
        return False
        