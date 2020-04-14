import pygame
from modules.ressources import Ressources

def eventHandel(events,rend,mousePos):
    for event in events.get():
        if event.type == pygame.QUIT:
            Ressources.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Played = False
            for i in range(len(rend.gameChoices)):
                if(rend.gameChoices[i].isIN(mousePos) and rend.gameChoices[i].selected == False):
                    if(Ressources.selected != -1):
                        rend.gameChoices[Ressources.selected].reseting = True
                    Ressources.selected = i
                    Played = True
                    rend.gameChoices[i].selected = True
                    Ressources.mouseOffset = (mousePos[0] - rend.Offsets[Ressources.selected][0],mousePos[1] - rend.Offsets[Ressources.selected][1])
            if(rend.bg.isInGrid(mousePos)):
                Played = True
            if(Played == False):
                if(Ressources.selected != -1):
                        rend.gameChoices[Ressources.selected].reseting = True
                Ressources.selected = -1