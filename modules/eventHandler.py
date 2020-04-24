import pygame
from modules.ressources import Ressources

def eventHandel(events,rend,mousePos):
    #choose Menus
    if(Ressources.mode == 0):
        for event in events.get():
            if event.type == pygame.QUIT:
                Ressources.running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(rend.chsMenu.buttons)):
                    if(rend.chsMenu.inButtonBox(mousePos,i) and rend.chsMenu.buttons[i][3] != 1):
                        rend.chsMenu.buttons[i][4]()
        #mouseOver Tests
        mouseOver = False
        for i in range(len(rend.chsMenu.buttons)):
            if(rend.chsMenu.inButtonBox(mousePos,i) and rend.chsMenu.buttons[i][3] != 1):
                if(Ressources.mouseOver == False):
                    rend.chsMenu.mouseOverSound.play()
                    Ressources.mouseOver = True
                rend.chsMenu.buttons[i][3] = 2
                mouseOver = True
            elif(rend.chsMenu.buttons[i][3] != 1):
                rend.chsMenu.buttons[i][3] = 0
        if(mouseOver == False):
            Ressources.mouseOver = False
    #loose menu        
    elif(Ressources.mode == 2):
        for event in events.get():
            if event.type == pygame.QUIT:
                Ressources.running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(rend.lsMenu.buttons)):
                    if(rend.lsMenu.inButtonBox(mousePos,i)):
                        rend.lsMenu.buttons[i][6]()
                        
        mouseOver = False
        for i in range(len(rend.lsMenu.buttons)):
            if(rend.lsMenu.inButtonBox(mousePos,i)):
                if(Ressources.mouseOver == False):
                    rend.chsMenu.mouseOverSound.play()
                    Ressources.mouseOver = True
                rend.lsMenu.buttons[i][4] = 1
                mouseOver = True
            else:
                rend.lsMenu.buttons[i][4] = 0
        if(mouseOver == False):
            Ressources.mouseOver = False
    #playing mode
    elif(Ressources.mode == 1):
        for event in events.get():
            if event.type == pygame.QUIT:
                Ressources.save()
                Ressources.running = False
                return
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Played = False
                for i in range(len(rend.gameChoices)):
                    if(rend.gameChoices[i].selected == False and rend.gameChoices[i].mouvable == True and rend.gameChoices[i].played == False and rend.gameChoices[i].isIN(mousePos)):
                        if(Ressources.selected != -1):
                            rend.gameChoices[Ressources.selected].reseting = True
                        Ressources.selected = i
                        Played = True
                        rend.gameChoices[i].selected = True
                        Ressources.mouseOffset = (mousePos[0] - rend.Offsets[Ressources.selected][0],mousePos[1] - rend.Offsets[Ressources.selected][1])
                if(rend.bg.isInGrid(mousePos) and Ressources.selected != -1):
                    if(Ressources.canPlay and rend.bg.isPlayable(rend.gameChoices[Ressources.selected],True)):
                        rend.bg.DestroyLines(rend.gameChoices[Ressources.selected])
                        Ressources.selected = -1
                    Played = True
                elif(rend.bg.isInBackground(mousePos)):
                    Played = True
                if(Played == False):
                    if(Ressources.selected != -1):
                            Ressources.returnedSound.play()
                            rend.gameChoices[Ressources.selected].reseting = True
                    Ressources.selected = -1
        turnFinished = rend.turnFinnished()
        if(turnFinished):
            rend.genOptions()
            rend.blitOptions()
        Lost = rend.checkIfLoose()
        if(Lost):
            rend.lsMenu.reset()
            Ressources.mode = 2
            Ressources.canContinue = False
            Ressources.del_save()
            rend.chsMenu.buttons[0][3] = 1
