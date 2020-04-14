import pygame
from modules.render import Render


pygame.init()
screenWidth = 500
screenHeight = 500
screen = pygame.display.set_mode([screenWidth, screenHeight])


running = True
clock = pygame.time.Clock()
rend = Render(screenWidth,screenHeight,screen)
rend.background()
rend.genOptions()
rend.blitOptions()
pygame.display.update()

#----gameVariables
selected = -1
mousePos = pygame.mouse.get_pos()
selectedGameObject = 0
mouseOffset = (0,0)
while running:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(rend.gameChoices)):
                if(rend.gameChoices[i].isIN(mousePos) and rend.gameChoices[i].selected == False):
                    if(selected != -1):
                        rend.gameChoices[selected].reseting = True
                    selected = i
                    rend.gameChoices[i].selected = True
                    mouseOffset = (mousePos[0] - rend.Offsets[selected][0],mousePos[1] - rend.Offsets[selected][1])
    pygame.display.flip()
    #draw background and options
    rend.background()
    rend.blitOptions()

    
    if(selected != -1 and rend.SelectionDrawable[selected] == True):
        rend.SelectionDrawable[selected] = False
        selectedGameObject = rend.gameChoices[selected]
    if(selectedGameObject != 0):
        selectedGameObject.draw((mousePos[0]-mouseOffset[0],mousePos[1]-mouseOffset[1]))
        
    rend.animations()
pygame.quit()
