import pygame
class Ressources:
    def __init__(self):
        Ressources.screenWidth = 0
        Ressources.screenHeight = 0
        Ressources.screen = 0
        Ressources.Running = True
        Ressources.DestroyedForm = 0
        Ressources.selected = -1
        Ressources.selectedTr = (-1,-1)
        Ressources.selectedBgTr = (-1,-1)
        Ressources.selectedGameObject = 0
        Ressources.played = []
        Ressources.gridForms = []
        Ressources.lineToDestroy = [[],[],[]] #cobtains all lines that will be destroyed after cheking all possibilitys
        Ressources.kOfEveryRow = []
        Ressources.mouseOffset = (0,0)
        Ressources.animationIndex = 0
        Ressources.mode = 0
        Ressources.canPlay = True
        Ressources.playedSound = pygame.mixer.Sound("assets/sounds/played.wav")
        Ressources.returnedSound = pygame.mixer.Sound("assets/sounds/returned.wav")
        Ressources.destroyedSound = pygame.mixer.Sound("assets/sounds/blows.wav")
        self.getColoredUpAndDowns()
        
        
    def getColoredUpAndDowns(self):
        greyUp = pygame.image.load('assets/up.png').convert_alpha()
        greyDown = pygame.image.load('assets/down.png').convert_alpha()
        
        greyUp = pygame.transform.scale(greyUp, (40, 34))
        greyDown = pygame.transform.scale(greyDown, (40, 34))
        
        Ressources.trWidth = 40
        Ressources.trHeight = 34
        Ressources.trXSpace = 25
        Ressources.trYSpace = 37
        Ressources.Rows = 0
        Ressources.Colls = 0
        Ressources.grid = [[]]
        
        greenUp = pygame.image.load('assets/up/green.png').convert_alpha()
        greenDown = pygame.image.load('assets/down/green.png').convert_alpha()
        yellowUp = pygame.image.load('assets/up/yellow.png').convert_alpha()
        yellowDown = pygame.image.load('assets/down/yellow.png').convert_alpha()
        orangeUp = pygame.image.load('assets/up/orange.png').convert_alpha()
        orangeDown = pygame.image.load('assets/down/orange.png').convert_alpha()
        cyonUp = pygame.image.load('assets/up/cyon.png').convert_alpha()
        cyonDown = pygame.image.load('assets/down/cyon.png').convert_alpha()
        
        greenUp = pygame.transform.scale(greenUp, (40, 34))
        greenDown = pygame.transform.scale(greenDown, (40, 34))
        yellowUp = pygame.transform.scale(yellowUp, (40, 34))
        yellowDown = pygame.transform.scale(yellowDown, (40, 34))
        orangeUp = pygame.transform.scale(orangeUp, (40, 34))
        orangeDown = pygame.transform.scale(orangeDown, (40, 34))
        cyonUp = pygame.transform.scale(cyonUp, (40, 34))
        cyonDown = pygame.transform.scale(cyonDown, (40, 34))
        
        Ressources.up = greyUp
        Ressources.down = greyDown
        Ressources.ups = [greenUp , yellowUp, orangeUp, cyonUp]
        Ressources.downs = [greenDown , yellowDown, orangeDown, cyonDown]
        Ressources.mouseOver = False
       
    @staticmethod
    def getGameObjectType(type):
        forms = {
            1 : [[[1,0,1],[0,1,0]],(3*Ressources.trXSpace,2*Ressources.trYSpace)],
            2 :  [[[1,-1,-1],[0,1,0]],(3*Ressources.trXSpace,2*Ressources.trYSpace)],
            3 :  [[0,1,0],(3*Ressources.trXSpace,Ressources.trYSpace)],
            4 :  [[[0,1,-1],[-1,0,1]],(3*Ressources.trXSpace,2*Ressources.trYSpace)],
            5 :  [[[-1,1,0],[1,0,-1]],(3*Ressources.trXSpace,2*Ressources.trYSpace)],
            6 :  [[[-1,1],[1,0],[0,-1]],(2*Ressources.trXSpace,3*Ressources.trYSpace)],
            7 :  [[[1,-1],[0,1],[-1,0]],(2*Ressources.trXSpace,3*Ressources.trYSpace)],
            8 :  [[1,0,1],(3*Ressources.trXSpace,Ressources.trYSpace)],
            9 :  [[0,1],(2*Ressources.trXSpace,Ressources.trYSpace)],
            10 :  [[1,0],(2*Ressources.trXSpace,Ressources.trYSpace)],
            11 :  [[[1],[0]],(Ressources.trXSpace,2*Ressources.trYSpace)],
            12 :  [[0],(Ressources.trXSpace,Ressources.trYSpace)],
            13 :  [[1],(Ressources.trXSpace,Ressources.trYSpace)],
        }
        return forms[type]
    