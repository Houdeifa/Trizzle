import pygame
import math
import random
from modules.form import Form
from modules.background import Background
from modules.ressources import Ressources
from modules.chooseMenu import ChooseMenu
from modules.looseMenu import LooseMenu
from modules.scoresMenu import ScoresMenu

class Render(Ressources):
    black = (0,0,0)
    def __init__(self,width,height,screen):
        super(Render, self).__init__()
        Ressources.screenWidth = width
        Ressources.screenHeight = height
        Ressources.screen = screen
        
        Ressources.fonts = [
            pygame.font.Font("assets/fonts/BebasNeue-Regular.ttf", width // 20),
            pygame.font.Font("assets/fonts/3X5_____.TTF", width // 20),
            pygame.font.Font("assets/fonts/BebasNeue-Regular.ttf", width // 30)
        ]
        self.Offsets = []
        self.gameChoices = []
        N = 6
        M = 11
        self.bg = Background(self.screen,N,M)
        self.chsMenu = ChooseMenu()
        self.lsMenu = LooseMenu()
        self.scoreMenu = ScoresMenu()
        Ressources.rend = self
        for i in range(N):
            tmp = []
            for j in range(M):
                tmp.append(-1)
            Ressources.gridForms.append(tmp)
        
    def reset(self):
        N = Ressources.Rows
        M = Ressources.Colls
        
        self.bg = Background(self.screen,N,M)
        self.gameChoices = []
        Ressources.gridForms = []
        for i in range(N):
            tmp = []
            for j in range(M):
                tmp.append(-1)
            Ressources.gridForms.append(tmp)
    def background(self):
        self.bg.draw()
        
    def checkIfLoose(self):
        Lost = True
        for i in range(3):
            if(not self.gameChoices[i].selected and not self.gameChoices[i].played and not self.bg.canPlays(self.gameChoices[i])):
                self.gameChoices[i].disabled = True
            else:
                self.gameChoices[i].disabled = False
                self.gameChoices[i].mouvable = True
        for i in range(3):
             if(not self.gameChoices[i].played and not self.gameChoices[i].disabled):
                Lost = False
        return Lost 
                          
    def blitOptions(self):
        for i in range(3):
            if(not self.gameChoices[i].selected and not self.gameChoices[i].played):
                self.gameChoices[i].draw()
                
    def turnFinnished(self):
        for i in range(len(self.gameChoices)):
            if(not self.gameChoices[i].played):
                return False
        return True
    
    def calculateOffsets(self):
        width = Ressources.screenWidth - 20
        height = 150
        margins = 10
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
        self.gameChoices = []
        for i in range(3):
            self.gameChoices.append(Form(0,(0,0),0))
        
        colorChoices = [0,1,2,3]
        
        colors = []
        colors.append(self.gameChoices[0].generateAlea(colorChoices))
        
        colorChoices.remove(colors[0])
        colors.append(self.gameChoices[1].generateAlea(colorChoices))
        
        colorChoices.remove(colors[1])
        self.gameChoices[2].generateAlea(colorChoices)
        
        self.calculateOffsets()
        self.positionAssign()
                
    def animations(self):
        for i in range(len(self.gameChoices)):
            if(self.gameChoices[i].reseting):
                if(self.gameChoices[i].restTo(self.Offsets[i],0.07)):
                    self.gameChoices[i].selected = False
                    
        for i in range(len(Ressources.played)):
            if(Ressources.played[i].playing):
                Ressources.played[i].playTo(Ressources.played[i].PlayedPos,0.07,Ressources.played[i].iPos)
                
        self.bg.DestAnimation()
        
    @staticmethod
    def getSave():
        playedForms = Ressources.doc.getElementsByTagName("playedForm")
        
        Ressources.played = []
        Ressources.rend.chsMenu.buttons[0][3] = 0
        for i in range(len(playedForms)):
            xPos = playedForms[i].getAttribute("xPos")
            yPos = playedForms[i].getAttribute("yPos")
            pos = (float(xPos), float(yPos))
            color = playedForms[i].getAttribute("color")
            color = int(color)
            typeN = playedForms[i].getAttribute("type")
            typeN = int(typeN)
            newForm = Form(typeN,pos,color)
            xPos = int(playedForms[i].getAttribute("jX"))
            yPos = int(playedForms[i].getAttribute("iY"))
            newForm.iPos = (xPos,yPos)
            newForm.played = True
            newForm.mouvable = False
            newForm.destoyed = False
            newForm.boxesDefinition()
            Ressources.played.append(newForm)
            distroyedBox = playedForms[i].getElementsByTagName("distroyedBox")
            
            for k in range(len(newForm.boxes)):
                if(type(newForm.boxes[0]) == list):
                    for l in range(len(newForm.boxes[0])):
                        Ressources.gridForms[k+yPos][l+xPos] = newForm.boxes[k][l]
                else:
                    Ressources.gridForms[yPos][k+xPos] = newForm.boxes[k]
                    
                    
            for j in range(len(distroyedBox)):
                jPos = int(distroyedBox[j].getAttribute("xPos"))
                iPos = int(distroyedBox[j].getAttribute("yPos"))
                if(iPos == -1):
                    newForm.boxes[jPos].destoyed = True
                    Ressources.gridForms[yPos][jPos+xPos] = -1
                else:
                    newForm.boxes[iPos][jPos].destoyed = True
                    Ressources.gridForms[iPos+yPos][jPos+xPos] = -1
                    
        choices = Ressources.doc.getElementsByTagName("choice")
        score = Ressources.doc.getElementsByTagName("TheScore")
        Ressources.score = int(score[0].getAttribute("value"))
        Ressources.gameChoices = []
        for i in range(len(choices)):
            typeN = choices[i].getAttribute("type")
            played = choices[i].getAttribute("played")
            typeN = int(typeN)
            color = choices[i].getAttribute("color")
            color = int(color)
            pos = (0,0)
            newForm = Form(typeN,pos,color)
            if(played == "True"): 
                played = True 
            else: 
                played = False
            newForm.played = played
            newForm.selected = played
            
            newForm.destoyed = False
            newForm.boxesDefinition()
            Ressources.gameChoices.append(newForm)
        
        Ressources.rend.gameChoices = Ressources.gameChoices
        Ressources.rend.calculateOffsets()
        for i in range(len(Ressources.gameChoices)):
            Ressources.gameChoices[i].pos = Ressources.rend.Offsets[i]
        Ressources.rend.gameChoices = Ressources.gameChoices
        
    
    
    