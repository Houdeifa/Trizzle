import pygame
from modules.ressources import Ressources
class ScoresMenu:
    x = 0
    def __init__(self):
        self.ListyPos = []
        self.screen = Ressources.screen
        self.font = Ressources.fonts[0]
        self.fontSmall = Ressources.fonts[2]
        self.squareWidth = (Ressources.screenWidth*2)/3
        self.squareHeight = (Ressources.screenHeight*3)/5
        self.squarePos = (Ressources.screenWidth / 2 - self.squareWidth / 2, Ressources.screenHeight / 2 - self.squareHeight / 2)
        back = pygame.image.load('assets/imgs/back.png').convert_alpha()
        backSel = pygame.image.load('assets/imgs/backSel.png').convert_alpha()
        self.buttonSize = (int(self.squareWidth // 7), int(self.squareHeight // 7))
        self.back = [pygame.transform.scale(back, (self.buttonSize[0], self.buttonSize[1])) , pygame.transform.scale(backSel, (self.buttonSize[0], self.buttonSize[1])) ]
        self.button = [
            ((Ressources.screenWidth - self.buttonSize[0]) / 2, (self.squarePos[1] + self.squareHeight + Ressources.screenHeight - self.buttonSize[1])/2)
        ]
        self.button.append((self.button[0][0] + self.buttonSize[0], self.button[0][1] + self.buttonSize[1]))
        self.buttonState = 0
        """
        0 : activated
        1 : Over
        2 : desactivated

        0 : current
        3 : default
        """
        self.tabs = [
            [0,"Best",self.swithToBest,0],
            [2,"Last",self.swithToLast,2]
        ]
        self.boxesDefnied = False
        self.tabsBox = [
            [],
            []
        ]
        self.mode = 0
        for i in range(10):
            self.ListyPos.append(self.squarePos[1] + self.squareHeight/10 * i)
        self.scoreSort(Ressources.scores,"value")
        self.scoreSort(Ressources.lastScores,"duration")
            
        for i in range(len(Ressources.scores)):
            d = ""
            for j in range(len(Ressources.scores[i]["date"])):
                d = d + (Ressources.scores[i]["date"][j])
                if(j == 1 or j == 3):
                    d = d + "/"
            Ressources.scores[i]["date"] = d
    def inTabBox(self,pos,index):
        if(not self.boxesDefnied):
            return False
        x = pos[0]
        y = pos[1]
        xinf = self.tabsBox[index][0][0]
        yinf = self.tabsBox[index][0][1]
        xlim = self.tabsBox[index][1][0]
        ylim = self.tabsBox[index][1][1]
        if( x >= xinf and x <= xlim and y >= yinf and y <= ylim):
            return True
        return False
    
    def inButtonBox(self,pos):
        if(not self.boxesDefnied):
            return False
        x = pos[0]
        y = pos[1]
        xinf = self.button[0][0]
        yinf = self.button[0][1]
        xlim = self.button[1][0]
        ylim = self.button[1][1]
        if( x >= xinf and x <= xlim and y >= yinf and y <= ylim):
            return True
        return False
    
    def drawButton(self):
        self.drawSquare(self.button[0],self.buttonSize[0],self.buttonSize[1],(255,0,0),True,(0,0,0))
        self.screen.blit(self.back[self.buttonState],self.button[0])
    
    def swithToBest(self):
        self.mode = 0
        self.tabs[0][0] = 0
        self.tabs[1][0] = 2
        self.tabs[0][3] = 0
        self.tabs[1][3] = 2
    def swithToLast(self):
        self.mode = 1
        self.tabs[0][0] = 2
        self.tabs[1][0] = 0
        self.tabs[0][3] = 2
        self.tabs[1][3] = 0
    def draw(self):
        self.drawScore()
        self.drawButton()
        
    def drawScore(self):
        Black = (0,0,0)
        Gray = (100,100,100)
        self.screen.fill(Gray)
        width = self.squareWidth
        height = self.squareHeight
        pos = self.squarePos
        self.tabsBox = []
        self.drawSquare(pos,width,height,Black)
        for i in range(len(self.tabs)):
            self.drawTab(i,self.tabs[i][0],self.tabs[i][3],pos,self.tabs[i][1])
        if(self.mode == 0):
            self.drawList(Ressources.scores)
        elif(self.mode == 1):
            self.plotList(Ressources.lastScores)
        self.boxesDefnied = True
        
    def drawSquare(self,pos,width,height,color,fill=True,fillcolor=-1):
        #drawing the square where Object are generated
        if(fillcolor == -1):
            fillcolor = color
        points = [(0 ,0), (width,0), (width, height),(0, height)]
        size = (width+2,height+2)
        lines_closed = pygame.Surface(size)
        RED = pygame.Color(255, 0, 0)
        if(fill):
            lines_closed.fill(fillcolor)
        pygame.draw.lines(lines_closed, RED, True, points)
        self.screen.blit(lines_closed, pos)
        
    def drawList(self,List):
        for i in range(len(List)):
            pos = (self.squarePos[0] + self.squareWidth/10,self.ListyPos[i])
            self.printText(List[i]["date"],pos)
            pos = (self.squarePos[0] + self.squareWidth - self.squareWidth/5,self.ListyPos[i])
            self.printText(str(List[i]["value"]),pos,True)
    def plotList(self,List):
        self.drawAxes()
        maxValue = List[0]["value"]
        for i in range(len(List)):
            if(maxValue < List[i]["value"]):
                maxValue = List[i]["value"]
        self.plot(List,maxValue)
        
    def drawHorizentalLine(self,color,Y,Arrows = True):
        lineWidth = int(Ressources.screenHeight / 250)
        XAxisWidth = self.squareWidth - 2*self.margeX
        YAxisHeight = self.squareHeight - 2*self.margeY
        margeX = self.margeX
        margeY = self.margeY
        size = (XAxisWidth,Ressources.screenHeight / 250)
        line = pygame.Surface(size,pygame.SRCALPHA)
        pygame.draw.line(line, color, (0,0), (int(size[0]),0), lineWidth)
        pos = (self.squarePos[0] + margeX, Y)
        self.screen.blit(line,pos)
        if(Arrows):
            #arraow line 1
            size = (Ressources.screenWidth / 100,Ressources.screenHeight / 100)
            line = pygame.Surface(size,pygame.SRCALPHA)
            pygame.draw.line(line, color, (0,0), (int(size[0]),int(size[1])), lineWidth)
            pos = (self.squarePos[0] + self.squareWidth - margeX - int(size[0]), self.squarePos[1] + self.squareHeight - margeY - int(size[1]))
            self.screen.blit(line,pos)
            #arraow line 2
            size = (Ressources.screenWidth / 100,Ressources.screenHeight / 100)
            line = pygame.Surface(size,pygame.SRCALPHA)
            pygame.draw.line(line, color, (0,int(size[1])), (int(size[0]),0), lineWidth)
            pos = (self.squarePos[0] + self.squareWidth - margeX - int(size[0]), self.squarePos[1] + self.squareHeight - margeY)
            self.screen.blit(line,pos)
        
        
    def drawVerticalLine(self,color,X,Arrows = True):
        lineWidth = int(Ressources.screenHeight / 250)
        XAxisWidth = self.squareWidth - 2*self.margeX
        YAxisHeight = self.squareHeight - 2*self.margeY
        margeX = self.margeX
        margeY = self.margeY
        size = (Ressources.screenWidth / 250,YAxisHeight)
        line = pygame.Surface(size,pygame.SRCALPHA)
        pygame.draw.line(line, color, (0,0), (0,int(size[1])), lineWidth)
        pos = (X, self.squarePos[1] + margeY)
        self.screen.blit(line,pos)
        if(Arrows):
            #arraow line 1
            size = (Ressources.screenWidth / 100,Ressources.screenHeight / 100)
            line = pygame.Surface(size,pygame.SRCALPHA)
            pygame.draw.line(line, color, (0,0), (int(size[0]),int(size[1])), lineWidth)
            pos = (self.squarePos[0] + margeX, self.squarePos[1] + margeY)
            self.screen.blit(line,pos)
            #arraow line 2
            size = (Ressources.screenWidth / 100,Ressources.screenHeight / 100)
            line = pygame.Surface(size,pygame.SRCALPHA)
            pygame.draw.line(line, color, (0,int(size[1])), (int(size[0]),0), lineWidth)
            pos = (self.squarePos[0] + margeX - int(size[0]), self.squarePos[1] + margeY)
            self.screen.blit(line,pos)
    def drawAxes(self):
        margeX = self.squareWidth/10
        margeY = self.squareHeight/10
        self.margeY = margeY
        self.margeX = margeX
        XAxisWidth = self.squareWidth - 2*margeX
        YAxisHeight = self.squareHeight - 2*margeY
        
        RED = pygame.Color(255, 0, 0)
        GREEN = pygame.Color(0, 80, 0)
        
        lineWidth = int(Ressources.screenHeight / 250)
        self.lineWidth = lineWidth
        #horizontal line
        self.drawHorizentalLine(RED,self.squarePos[1] + self.squareHeight - margeY)
        
        #vertical line
        self.drawVerticalLine(RED,self.squarePos[0] + margeX)
        
        #small lines 1 X (vertical)
        size = (Ressources.screenWidth / 250,Ressources.screenWidth / 100)
        line = pygame.Surface(size,pygame.SRCALPHA)
        pygame.draw.line(line, RED, (0,0), (0,int(size[1])), lineWidth)
        #Values
        self.XPos = []
        self.YAxisHeight = (XAxisWidth*9/10)
        step = self.YAxisHeight / 10
        yPos = self.squarePos[1] + YAxisHeight + margeY - (size[1] / 2)
        xPos = self.squarePos[0] + margeX  
        for i in range(1,11):
            pos = (xPos + step*i,yPos)
            self.XPos.append(xPos + step*i)
            self.drawVerticalLine(GREEN,xPos + step*i,False)
            self.screen.blit(line,pos)
            self.printText(str(i),(pos[0] + step/6,pos[1] + step/10),False,self.fontSmall)
        #small lines 1 X (Horizental)
        size = (Ressources.screenWidth / 100,Ressources.screenWidth / 250)
        line = pygame.Surface(size,pygame.SRCALPHA)
        pygame.draw.line(line, RED, (0,0), (int(size[0]),0), lineWidth)
        #Values
        self.YPos = []
        step = (YAxisHeight*9/10) / 10
        yPos = self.squarePos[1] + margeY + YAxisHeight /10
        xPos = self.squarePos[0] + margeX - (size[0] / 2)
        for i in range(0,10):
            pos = (xPos,yPos + step*i)
            self.YPos.append(yPos + step*i)
            self.drawHorizentalLine(GREEN,yPos + step*i,False)
            self.screen.blit(line,pos)
            
    def plot(self,List,maxValue):
        N = 1
        while(N < maxValue):
            N = N * 10
        N = N / 10
        if(N < 1 ):
            N = 1
        s = N
        while(N < maxValue):
            N = N + s 
        width = self.XPos[1] - self.XPos[0]
        width = width + self.lineWidth*2
        margeY = self.squarePos[1] + self.margeY
        self.printText(str(int(N)),(self.squarePos[0] + self.margeX,self.YPos[0]),False,self.fontSmall)
        for i in range(1,len(List)):
            Y1 = (self.YAxisHeight*List[i]["value"]) / N
            Y1 = self.YAxisHeight - Y1
            Y0 = (self.YAxisHeight*List[i-1]["value"]) / N
            Y0 = self.YAxisHeight - Y0
            
            Height = abs(Y1 - Y0)
            Height = Height + self.lineWidth*2
            size = (width,Height)
            line = pygame.Surface(size,pygame.SRCALPHA)
            self.printText(str(int(N - N*(i)/10)),(self.squarePos[0] + self.margeX,self.YPos[i]),False,self.fontSmall)
            if(Y0 < Y1):
                pos = (self.XPos[i-1],Y0 + margeY)
                pygame.draw.line(line, (255,255,255), (0,0), (size[0],size[1]), self.lineWidth)
            else:
                pos = (self.XPos[i-1],Y1 + margeY)
                pygame.draw.line(line, (255,255,255), (0,size[1]), (size[0],0), self.lineWidth)
            self.screen.blit(line,pos)
        
    def printText(self,text,pos,right=True,font = -1):
        if(font == -1):
            font = self.font
        color = (255,255,255)
        text = font.render(text, True, color)
        if(not right):
            pos = (pos[0] - text.get_width(),pos[1])
        self.screen.blit(text,pos)
        
    def drawTab(self,index,state,defaultState,squarePos,text):
        Black = (0,0,0)
        Gray = (100,100,100)
        activatedColor = (0, 150, 0)
        desactivatedColor = (128, 128, 128)
        MouseOverColor = (0, 255, 0)
        if(defaultState == 0):
            color = Black
        else:
            color = Gray
        width = (Ressources.screenWidth)/6
        height = (Ressources.screenHeight)/15
        pos = (squarePos[0] + width * index,squarePos[1] - height)
        infos = [pos , (pos[0] + width,pos[1] + height)]
        self.tabsBox.append(infos)
        self.drawSquare(pos,width,height,color)
        if(state == 0):
            color = activatedColor
        elif(state == 1):
            color = MouseOverColor
        else:
            color = desactivatedColor
        text = self.font.render(text, True, color)
        pos = (pos[0] + width // 2 - text.get_width() // 2,pos[1] + height // 2 - text.get_height() // 2)
        self.screen.blit(text,pos)
        
    def scoreSort(self,List,condition):
        lSorted = False 
        while(not lSorted):
            lSorted = True 
            for i in range(len(List) - 1):
                if(int(List[i][condition]) < int(List[i+1][condition])):
                    lSorted = False
                    d = List[i]
                    List[i] = List[i+1]
                    List[i+1] = d
            
    