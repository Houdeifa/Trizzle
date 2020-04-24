import pygame
import xml.dom.minidom
from datetime import date

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
        Ressources.fonts = [
            pygame.font.Font("assets/fonts/BebasNeue-Regular.ttf", 28),
            pygame.font.Font("assets/fonts/3X5_____.TTF", 28)
        ]
        Ressources.canPlay = True
        Ressources.playedSound = pygame.mixer.Sound("assets/sounds/played.wav")
        Ressources.returnedSound = pygame.mixer.Sound("assets/sounds/returned.wav")
        Ressources.destroyedSound = pygame.mixer.Sound("assets/sounds/blows.wav")
        Ressources.numbers = [
            pygame.image.load('assets/imgs/numbers/0.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/1.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/2.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/3.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/4.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/5.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/6.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/7.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/8.png').convert_alpha(),
            pygame.image.load('assets/imgs/numbers/9.png').convert_alpha()
        ]
        self.getColoredUpAndDowns()
        Ressources.canContinue = False
    
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
        Ressources.score = 0
        Ressources.configFileExists = False
        
        
       
    @staticmethod
    def getGameObjectType(type):
        forms = {
            1 : [[[1,0,1],[0,1,0]],(3*Ressources.trXSpace,2*Ressources.trYSpace),6,(0,0)],
            2 :  [[[1,-1,-1],[0,1,0]],(3*Ressources.trXSpace,2*Ressources.trYSpace),6,(0,0)],
            3 :  [[0,1,0],(3*Ressources.trXSpace,Ressources.trYSpace),3,(0,0)],
            4 :  [[[0,1,-1],[-1,0,1]],(3*Ressources.trXSpace,2*Ressources.trYSpace),6,(0,0)],
            5 :  [[[-1,1,0],[1,0,-1]],(3*Ressources.trXSpace,2*Ressources.trYSpace),6,(1,0)],
            6 :  [[[-1,1],[1,0],[0,-1]],(2*Ressources.trXSpace,3*Ressources.trYSpace),6,(1,0)],
            7 :  [[[1,-1],[0,1],[-1,0]],(2*Ressources.trXSpace,3*Ressources.trYSpace),6,(0,0)],
            8 :  [[1,0,1],(3*Ressources.trXSpace,Ressources.trYSpace),3,(0,0)],
            9 :  [[0,1],(2*Ressources.trXSpace,Ressources.trYSpace),2,(0,0)],
            10 :  [[1,0],(2*Ressources.trXSpace,Ressources.trYSpace),2,(0,0)],
            11 :  [[[1],[0]],(Ressources.trXSpace,2*Ressources.trYSpace),2,(0,0)],
            12 :  [[0],(Ressources.trXSpace,Ressources.trYSpace),1,(0,0)],
            13 :  [[1],(Ressources.trXSpace,Ressources.trYSpace),1,(0,0)],
        }
        return forms[type]
    
    @staticmethod
    def printNumber(N,scale,pos):
        i = 0
        if(N == 0):
            img = Ressources.numbers[0]
            width = int(img.get_width()*scale)
            height = int(img.get_height()*scale)
            img = pygame.transform.scale(img, (width, height))
            Ressources.screen.blit(img,pos)
            
        while(N != 0):
            CurrnetN = int(N % 10)
            img = Ressources.numbers[CurrnetN]
            width = int(img.get_width()*scale)
            height = int(img.get_height()*scale)
            img = pygame.transform.scale(img, (width, height))
            pos = (pos[0] + i * width,pos[1])
            Ressources.screen.blit(img,pos)
            N = N / 10
            i = i + 1
    @staticmethod
    def reset():
        Ressources.played = []
        Ressources.canPlay = True
        Ressources.mouseOffset = (0,0)
        Ressources.animationIndex = 0
        Ressources.rend.reset()
        Ressources.score = 0
    @staticmethod
    def readConfigFile():
        try:
            doc = xml.dom.minidom.parse("assets/config.xml")
            Ressources.doc = doc
            Ressources.configFileExists = True
            Ressources.saves = doc.getElementsByTagName("save")
            Ressources.scores = doc.getElementsByTagName("score")
            Ressources.screenConf = doc.getElementsByTagName("screen")
            if(len(Ressources.saves) != 0):
                Ressources.canContinue = True
        except Exception:
            Ressources.configFileExists = False
    @staticmethod
    def save(saveGame = True):
        if(saveGame):
            save = Ressources.doc.createElement("save")
            for form in Ressources.played:
                playedForm = Ressources.doc.createElement("playedForm")
                playedForm.setAttribute("type", str(form.type))
                playedForm.setAttribute("pos", str(form.pos))
                playedForm.setAttribute("iPos", str(form.iPos))
                playedForm.setAttribute("color", str(form.color))
                for i in range(len(form.boxes)):
                    if(type(form.boxes[0]) != list and form.boxes[i].destoyed):
                        box = Ressources.doc.createElement("distroyedBox")
                        box.setAttribute("pos", str((i,-1)))
                        playedForm.appendChild(box)
                    elif(type(form.boxes[0]) == list):
                        for j in range(len(form.boxes[i])):
                            if(form.boxes[i][j] != -1 and form.boxes[i][j].destoyed):
                                box = Ressources.doc.createElement("distroyedBox")
                                box.setAttribute("pos", str((j,i)))
                                playedForm.appendChild(box)
                save.appendChild(playedForm)
                choices = Ressources.doc.createElement("choices")
                for i in range(len(Ressources.rend.gameChoices)):
                    choice = Ressources.doc.createElement("choice")
                    choice.setAttribute("type", str(Ressources.rend.gameChoices[i].type))
                    choice.setAttribute("color", str(Ressources.rend.gameChoices[i].color))
                    choice.setAttribute("played", str(Ressources.rend.gameChoices[i].played))
                    choices.appendChild(choice)
                save.appendChild(choices)
            SavesParent = Ressources.doc.getElementsByTagName("saves")[0]
            oldSaves = SavesParent.getElementsByTagName("save")
            for anySave in oldSaves:
                SavesParent.removeChild(anySave)
            SavesParent.appendChild(save)
            
            
        if(Ressources.score > int(Ressources.minScore["value"])):
            Ressources.scores.remove(Ressources.minScore)
        
            today = date.today()

            # dd/mm/YY
            d = today.strftime("%d%m%Y")
            infos = {
                "value" : Ressources.score,
                "date" : d
            }
            Ressources.scores.append(infos)
            Ressources.minScoreElement.setAttribute("value",str(Ressources.score))
            Ressources.minScoreElement.setAttribute("date",str(d))
            
        with open("assets/config.xml", "w") as xml_file:
            Ressources.doc.writexml(xml_file)
    def getScores():
        Ressources.scores = Ressources.doc.getElementsByTagName("score")
        scores = []
        maxx = Ressources.scores[0].getAttribute("value")
        minn = maxx
        for i in range(len(Ressources.scores)):
            infos = {
                "value" : Ressources.scores[i].getAttribute("value"),
                "date" : Ressources.scores[i].getAttribute("date")
            }
            maxx = max(maxx, infos["value"])
            minn = min(minn, infos["value"])
            if(maxx == Ressources.scores[i].getAttribute("value")):
                Ressources.maxScore = infos
           
            if(minn == Ressources.scores[i].getAttribute("value")):
                Ressources.minScore = infos
                Ressources.minScoreElement = Ressources.scores[i]
                
            scores.append(infos)
            
        Ressources.scores = scores
    def getSave():
        x = 0
        