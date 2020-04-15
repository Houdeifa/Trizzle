import pygame
from modules.triangle import Triangle
from modules.ressources import Ressources

class Background:
    def __init__(self,screen,rows,colls):
        self.screen = screen
        self.rows = rows #6
        self.colls = colls #11
        self.rows = self.rows - self.rows%2
        self.colls = self.colls - self.colls%2 + 1
        Ressources.Rows = self.rows
        Ressources.Colls = self.colls
        
        self.width = Ressources.trXSpace*(self.colls-1) + Ressources.trWidth
        self.height = Ressources.trYSpace*(self.rows-1) + Ressources.trHeight
        xPos = Ressources.screenWidth/2-self.width/2
        yPos = 2*Ressources.screenHeight/5-self.height/2
        self.pos = (xPos,yPos)
        self.PlayPosS = []
        
        self.gridCalculator()
        self.draw()
    
    def gridCalculator(self):
        Ressources.grid = []
        for j in range(self.rows):
            k = (j - self.rows/2)
            if(k < 0 ):
                 k = (k+1)* -1;
            rawGrid = []
            for i in range (self.colls):
                if(i >= k and i < (self.colls-k)):
                    pos = (i*Ressources.trXSpace, j*Ressources.trYSpace)
                    tr = Triangle(self,self.screen,(i+j+1)%2,pos)
                    rawGrid.append(tr)
                else:
                    pos = (-1,-1)
                    rawGrid.append(-1)
            Ressources.grid.append(rawGrid)
    
    def draw(self):
        self.screen.fill((0,0,0))
        self.PlayPosS = []
        for j in range(self.rows):
            for i in range (self.colls):
                if(Ressources.grid[j][i] != -1):
                    Ressources.grid[j][i].draw()
        self.drawOptionsSquare(Ressources.screenWidth - 20,150,10)
        for form in Ressources.played:
            if(form.played):
                form.draw()
    
    def drawOptionsSquare(self,width,height,margins):
        #drawing the square where Object are generated
        points = [(0 ,0), (width,0), (width, height),(0, height)]
        size = (width+2,height+2)
        lines_closed = pygame.Surface(size)
        RED = pygame.Color(255, 0, 0) 
        pygame.draw.lines(lines_closed, RED, True, points)
        self.screen.blit(lines_closed, (margins, Ressources.screenHeight-height-margins))
        
    def isInGrid(self,pixelPos):
        normalizedX = pixelPos[0] - self.pos[0]
        normalizedY = pixelPos[1] - self.pos[1]
        
        for j in range(self.rows):
            for i in range (self.colls):
                if(Ressources.grid[j][i] != -1):
                    pos = (normalizedX - Ressources.grid[j][i].pos[0],normalizedY - Ressources.grid[j][i].pos[1])
                    if(Ressources.grid[j][i].isIN(pos)):
                        Ressources.selectedBgTr = (i,j)
                        return True
        Ressources.selectedBgTr = (-1,-1)
        return False
    
    def isPlayable(self,form,plays):
        if(Ressources.selectedBgTr[0] == -1 and Ressources.selectedBgTr[1] == -1):
            return False
        if(Ressources.selectedTr[0] == -1 and Ressources.selectedTr[1] == -1):
            return False
        
        boxes = form.boxes
        xf = Ressources.selectedTr[0]
        yf = Ressources.selectedTr[1]
        
        xg = Ressources.selectedBgTr[0]
        yg = Ressources.selectedBgTr[1]
        k = (yg - self.rows/2)
        if(k < 0 ):
            k = (k+1)* -1;
        if(yf == -1):
            if(boxes[xf].type != Ressources.grid[yg][xg].type):
                return False
            dleft = xg - xf
            dright = (self.colls - xg - 1 - k) + xf + 1
            if(dleft < k or dright < form.colls):
                return False
            for i in range(form.colls): 
                if(Ressources.grid[yg][dleft+i].occupied):
                    return False
                
            if(plays):
                for j in range(form.colls):
                    if(Ressources.grid[yg][dleft+j] != -1):
                        Ressources.grid[yg][dleft+j].occupied = True
                xg = xg - xf
                pos = (xg * Ressources.trXSpace + self.pos[0],yg * Ressources.trYSpace + self.pos[1])
                form.playTo(pos,0.1)
                Ressources.played.append(form)
            return True
        else:
            if(boxes[yf][xf].type != Ressources.grid[yg][xg].type):
                return False
            dleft = xg - xf
            
            dtop = yg - yf
            
            ymax = dtop + form.rows - 1
            xmax = dleft + form.colls - 1
            if(ymax >= self.rows or xmax >= (self.colls-k) or dleft< 0 or dtop< 0):
                return False
            for i in range(form.rows):
                for j in range(form.colls):
                    y = dtop+i
                    x = dleft+j
                    if(boxes[i][j] != -1 and (Ressources.grid[y][x] == -1 or Ressources.grid[y][x] != -1 and Ressources.grid[y][x].occupied)):
                        return False
            if(plays):
                for i in range(form.rows):
                    for j in range(form.colls):
                        y = dtop+i
                        x = dleft+j
                        if(Ressources.grid[y][x] != -1 and boxes[i][j] != -1):
                            Ressources.grid[y][x].occupied = True
                xg = xg - xf 
                yg = yg - yf 
                pos = (xg * Ressources.trXSpace+ self.pos[0],yg * Ressources.trYSpace + self.pos[1])
                form.playTo(pos,0.1)
                Ressources.played.append(form)
            return True
    
    def canPlays(self,form):
        for i in range(self.rows):
            for j in range(self.colls):
                if(Ressources.grid[i][j] != -1):
                    Ressources.selectedTr = (0,0)
                    Ressources.selectedBgTr = (j,i)
                    self.isPlayable(form,False)