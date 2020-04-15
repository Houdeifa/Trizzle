import pygame
from modules.render import Render
from modules.ressources import Ressources
import modules.eventHandler as eventHandler

pygame.init()
screenWidth = 500
screenHeight = 500
screen = pygame.display.set_mode([screenWidth, screenHeight])


Ressources.running = True
clock = pygame.time.Clock()
rend = Render(screenWidth,screenHeight,screen)
rend.background()
rend.genOptions()
rend.blitOptions()
pygame.display.update()

#----gameVariables
Ressources.selected = -1
mousePos = pygame.mouse.get_pos()
Ressources.selectedGameObject = 0
Ressources.mouseOffset = (0,0)


while Ressources.running:
    mousePos = pygame.mouse.get_pos()
    eventHandler.eventHandel(pygame.event,rend,mousePos)
    pygame.display.flip()
    #draw background and options
    rend.background()
    rend.blitOptions()

    if(Ressources.selected != -1 and rend.SelectionDrawable[Ressources.selected] == True):
        rend.SelectionDrawable[Ressources.selected] = False
        Ressources.selectedGameObject = rend.gameChoices[Ressources.selected]
    elif(Ressources.selected == -1):
        Ressources.selectedGameObject = 0
    if(Ressources.selectedGameObject != 0):
        Ressources.selectedGameObject.draw((mousePos[0]-Ressources.mouseOffset[0],mousePos[1]-Ressources.mouseOffset[1]))
        
    rend.animations()
pygame.quit()
