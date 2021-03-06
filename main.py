import pygame
from modules.render import Render
from modules.ressources import Ressources
import modules.eventHandler as eventHandler

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
Ressources.configFileExists = False
Ressources.canContinue = False
Ressources.readConfigFile()
Ressources.yearOffset = 2020
if(Ressources.configFileExists and Ressources.screenConf != []):
    screenWidth = int(Ressources.screenConf[0].getAttribute("width"))
    screenHeight = int(Ressources.screenConf[0].getAttribute("height"))
    Ressources.getScores()
else:
    screenWidth = 500
    screenHeight = 500
    Ressources.maxScore = {"value" : "0", "date": "00000000"}
    Ressources.minScore = {"value" : "0", "date": "00000000"}
    Ressources.scores = []
screen = pygame.display.set_mode([screenWidth, screenHeight])


Ressources.running = True
clock = pygame.time.Clock()
rend = Render(screenWidth,screenHeight,screen)

if(Ressources.canContinue):
    Render.getSave()
    
pygame.display.update()

#----gameVariables
Ressources.selected = -1
mousePos = pygame.mouse.get_pos()
Ressources.selectedGameObject = 0
Ressources.mouseOffset = (0,0)
Ressources.screen = screen

while Ressources.running:
    mousePos = pygame.mouse.get_pos()
    eventHandler.eventHandel(pygame.event,rend,mousePos)
    if(not Ressources.running):
        break
    pygame.display.flip()
    #draw background and options
    if(Ressources.mode == 0):
        rend.chsMenu.draw()
    if(Ressources.mode == 1):
        rend.background()
        rend.blitOptions()

        if(Ressources.selected != -1 and rend.gameChoices[Ressources.selected].selected):
            rend.gameChoices[Ressources.selected].selected = True
            Ressources.selectedGameObject = rend.gameChoices[Ressources.selected]
        elif(Ressources.selected == -1):
            Ressources.selectedGameObject = 0
        if(Ressources.selectedGameObject != 0):
            Ressources.selectedGameObject.draw((mousePos[0]-Ressources.mouseOffset[0],mousePos[1]-Ressources.mouseOffset[1]))

        rend.animations()
    if(Ressources.mode == 2):
        rend.lsMenu.draw()
    if(Ressources.mode == 3):
        rend.scoreMenu.draw()
pygame.quit()
