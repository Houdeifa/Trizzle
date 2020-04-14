import pygame
import math
import random
from modules.form import Form
from modules.background import Background
from modules.ressources import Ressources

class Render(Ressources):
    black = (0,0,0)
    def __init__(self,width,height,screen):
        super(Render, self).__init__()
        Ressources.screenWidth = width
        Ressources.screenHeight = height
        Ressources.screen = screen
        self.Offsets = []
        self.gameChoices = []
        self.SelectionDrawable = [True,True,True]
        self.bg = Background(self.screen,6,11)
        
        
    def background(self):
        self.bg.draw()
                
                          
    def blitOptions(self):
        for i in range(3):
            if(self.SelectionDrawable[i]):
                self.gameChoices[i].draw()
                
    def turnFinnished(self):
        if(not self.SelectionDrawable[0] and not self.SelectionDrawable[1] and not self.SelectionDrawable[2]):
            return False
        else:
            return True
    
    def calculateOffsets(self,width,height,margins):
        widthOffset = 2*margins
        HieghtOffset = Ressources.screenHeight - margins - height/2
        widthLimit = Ressources.screenWidth-margins
        self.Offsets = []

        
        size = self.gameChoices[0].size
        Offset = (widthOffset , HieghtOffset-size[1]/2)
        self.Offsets.append(Offset)
        
        
        size = self.gameChoices[1].size
        Offset = ((widthLimit-widthOffset)/2 - size[0]/2 , HieghtOffset-size[1]/2)
        self.Offsets.append(Offset)
        
        
        size = self.gameChoices[2].size
        Offset = (widthLimit - size[0] - margins*2 , HieghtOffset-size[1]/2)
        self.Offsets.append(Offset)
        
        
    def positionAssign(self):
        for i in range(3):
            self.gameChoices[i].pos = self.Offsets[i]
    
    def genOptions(self):
        for i in range(3):
            self.gameChoices.append(Form(0,(0,0),0))
        
        colorChoices = [0,1,2,3]
        
        colors = []
        self.gameChoices[0].generateAlea(colorChoices)
        colors.append(self.gameChoices[0].generateAlea(colorChoices))
        
        colorChoices.remove(colors[0])
        colors.append(self.gameChoices[1].generateAlea(colorChoices))
        
        colorChoices.remove(colors[1])
        self.gameChoices[2].generateAlea(colorChoices)
        
        self.calculateOffsets(Ressources.screenWidth - 20,150,10)
        self.positionAssign()
                
    def animations(self):
        for i in range(3):
            if(self.gameChoices[i].reseting):
                if(self.gameChoices[i].restTo(self.Offsets[i],0.07)):
                    self.SelectionDrawable[i] = True
    
    
    
    