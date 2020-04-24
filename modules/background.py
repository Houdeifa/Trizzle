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
        M = 6
        for i in range(self.rows):
            Ressources.lineToDestroy[0].append(-1)
            
        for i in range(M):
            Ressources.lineToDestroy[1].append(-1)
            Ressources.lineToDestroy[2].append(-1)
        
        self.width = Ressources.trXSpace*(self.colls-1) + Ressources.trWidth
        self.height = Ressources.trYSpace*(self.rows-1) + Ressources.trHeight
        xPos = Ressources.screenWidth/2-self.width/2
        yPos = 2*Ressources.screenHeight/5-self.height/2
        self.pos = (xPos,yPos)
        self.scorePos = (Ressources.screenWidth - Ressources.screenWidth/20,Ressources.screenHeight/20)
        self.bestScorePos = (Ressources.screenWidth/20,Ressources.screenHeight/20)
        self.font = Ressources.fonts[1]
        self.PlayPosS = []
        
        self.gridCalculator()
    def reset(self):
        N = Ressources.Rows
        M = Ressources.Colls
        Ressources.gridForms = []
        for i in range(N):
            tmp = []
            for j in range(M):
                tmp.append(-1)
            Ressources.gridForms.append(tmp)
    def gridCalculator(self):
        Ressources.grid = []
        for j in range(self.rows):
            k = (j - self.rows/2)
            if(k < 0 ):
                 k = (k+1)* -1
            Ressources.kOfEveryRow.append(int(k))
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
        self.print_score()
        self.print_best_score()
        for form in Ressources.played:
            if(form.played and not form.destoyed):
                form.draw()
            elif(form.destoyed):
                Ressources.played.remove(form)
    def print_score(self): 
        color = (255,255,255)
        text = self.font.render(str(Ressources.score), True, color)
        pos = self.scorePos
        pos = (pos[0] - text.get_width(),pos[1])
        self.screen.blit(text,pos)
        
    def print_best_score(self): 
        color = (255,255,255)
        text = self.font.render("BEST : " + str(Ressources.maxScore["value"]), True, color)
        pos = self.bestScorePos
        self.screen.blit(text,pos)
        
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
    def isInBackground(self,pixelPos):
        y = (pixelPos[1] - self.pos[1]) // Ressources.trYSpace
        x = (pixelPos[0] - self.pos[0]) // Ressources.trXSpace
        k = (y - self.rows/2)
        if(k < 0 ):
            k = (k+1)* -1
        if(x >= k and x < (self.colls-k) and y >= 0 and y < self.rows):
            return True
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
        
        k = Ressources.kOfEveryRow[yg]
        if(yf == -1):
            if(boxes[xf].type != Ressources.grid[yg][xg].type):
                return False
            dleft = xg - xf
            dright = (self.colls - xg - 1 - k) + xf + 1
            if(dleft < k or dright < form.colls):
                return False
            for i in range(form.colls): 
                if(Ressources.gridForms[yg][dleft+i] != -1):
                    return False
                
            if(plays):
                Ressources.playedSound.play(loops=0, maxtime=0, fade_ms=0)
                for j in range(form.colls):
                    if(Ressources.grid[yg][dleft+j] != -1):
                        Ressources.gridForms[yg][dleft+j] = boxes[j]
                xg = xg - xf
                pos = (xg * Ressources.trXSpace + self.pos[0],yg * Ressources.trYSpace + self.pos[1])
                form.playTo(pos,0.1,(xg,yg))
                Ressources.played.append(form)
            return True
        else:
            if(boxes[yf][xf] != -1 and boxes[yf][xf].type != Ressources.grid[yg][xg].type):
                return False
            dleft = xg - xf
            
            dtop = yg - yf
            
            ymax = dtop + form.rows - 1
            xmax = dleft + form.colls - 1
            if(ymax >= self.rows or xmax >= self.colls or dleft< 0 or dtop< 0):
                return False
            for i in range(form.rows):
                for j in range(form.colls):
                    y = dtop+i
                    x = dleft+j
                    if(boxes[i][j] != -1 and (Ressources.grid[y][x] == -1 or Ressources.grid[y][x] != -1 and Ressources.gridForms[y][x] != -1)):
                        return False
            if(plays):
                Ressources.playedSound.play(loops=0, maxtime=0, fade_ms=0)
                for i in range(form.rows):
                    for j in range(form.colls):
                        y = dtop+i
                        x = dleft+j
                        if(Ressources.grid[y][x] != -1 and boxes[i][j] != -1):
                            Ressources.gridForms[y][x] = boxes[i][j]
                xg = xg - xf 
                yg = yg - yf 
                pos = (xg * Ressources.trXSpace+ self.pos[0],yg * Ressources.trYSpace + self.pos[1])
                form.playTo(pos,0.1,(xg,yg))
                Ressources.played.append(form)
            return True
    
    def canPlays(self,form):
        can = False
        tmp1 = Ressources.selectedTr
        tmp2 = Ressources.selectedBgTr
        for i in range(self.rows):
            for j in range(self.colls):
                if(Ressources.grid[i][j] != -1):
                    Ressources.selectedTr = form.optimalSelectionPos
                    if(type(form.boxes[0]) != list):
                        Ressources.selectedTr = (0,-1)
                    Ressources.selectedBgTr = (j,i)
                    if(self.isPlayable(form,False)):
                        can = True
        Ressources.selectedTr = tmp1
        Ressources.selectedBgTr = tmp2
        return can
                    
    def checkToDestroyIn(self,pos):
        xi = pos[0]
        yi = pos[1]
        DestroyColl = True
        DestroySlash = True
        DestroyBackSlash = True
        collScore = 0
        SlashScore = 1
        BackSlashScore = 1
        
        #0 : row 
        k = Ressources.kOfEveryRow[yi]
        width = int(self.colls - 2*k)
        for i in range(width):
            if(Ressources.gridForms[yi][k+i] == -1):
                DestroyColl = False
                break
        LineIndex = yi
        if(DestroyColl and Ressources.lineToDestroy[0][LineIndex] == -1):
            Ressources.score = Ressources.score + self.colls - 2*k
            Ressources.lineToDestroy[0][LineIndex] = pos
        
        #1 : a slash /
        dx = max(xi , self.colls - xi)
        dy = max(yi , self.rows - yi)
        if(Ressources.grid[yi][xi] != -1):
            trType = Ressources.grid[yi][xi].type
        else:
            trType = 0
        if(trType == 0):
            offset = -1
        else:
            offset = 1
        M = max(dx,dy)
        for i in range(M):
            x1 = xi + i
            y1 = yi - i
            x2 = xi - i
            y2 = yi + i
            x1p = x1 + offset
            x2p = x2 + offset
            if(x1 < self.colls and y1 >= 0 and Ressources.grid[y1][x1] != -1 and Ressources.gridForms[y1][x1] == -1):
                DestroySlash = False
                break
            elif( i != 0 and x1 < self.colls and y1 >= 0 and Ressources.grid[y1][x1] != -1 and Ressources.gridForms[y1][x1] != -1):
                SlashScore = SlashScore +1
            if(x1p < self.colls and x1p >= 0 and y1 >= 0 and Ressources.grid[y1][x1p] != -1 and Ressources.gridForms[y1][x1p] == -1):
                DestroySlash = False
                break
            elif(i != 0 and x1p < self.colls and x1p >= 0 and y1 >= 0 and Ressources.grid[y1][x1p] != -1 and Ressources.gridForms[y1][x1p] != -1):
                SlashScore = SlashScore +1
            if(x2 >= 0 and y2 < self.rows and Ressources.grid[y2][x2] != -1 and Ressources.gridForms[y2][x2] == -1):
                DestroySlash = False
                break
            elif(i != 0 and x2 >= 0 and y2 < self.rows and Ressources.grid[y2][x2] != -1 and Ressources.gridForms[y2][x2] != -1):
                SlashScore = SlashScore +1
            if(x2p >= 0 and x2p < self.colls and y2 < self.rows and Ressources.grid[y2][x2p] != -1 and Ressources.gridForms[y2][x2p] == -1):
                DestroySlash = False
                break
            elif(i != 0 and x2p >= 0 and x2p < self.colls and y2 < self.rows and Ressources.grid[y2][x2p] != -1 and Ressources.gridForms[y2][x2p] != -1):
                SlashScore = SlashScore +1
            
        offset = (trType + 1)%2
        xIndex = xi - offset
        xIndex = self.colls - xIndex
        LineIndex = xIndex - yi + 1
        LineIndex = (10 - LineIndex)/2
        LineIndex = int(LineIndex)
        if(DestroySlash and Ressources.lineToDestroy[1][LineIndex] == -1):
            Ressources.score = Ressources.score + SlashScore
            Ressources.lineToDestroy[1][LineIndex] = pos
            
        #2 : a backslash \
        
        if(trType == 0):
            offset = 1
        else:
            offset = -1
        M = max(dx,dy)
        for i in range(M):
            x1 = xi + i
            x2 = xi - i
            y1 = yi + i
            y2 = yi - i
            x1p = x1 + offset
            x2p = x2 + offset
            if(x1 < self.colls and y1 < self.rows and Ressources.grid[y1][x1] != -1 and Ressources.gridForms[y1][x1] == -1):
                DestroyBackSlash = False
                break
            elif(i != 0 and x1 < self.colls and y1 < self.rows and Ressources.grid[y1][x1] != -1 and Ressources.gridForms[y1][x1] != -1):
                BackSlashScore = BackSlashScore + 1
            if(x1p < self.colls and x1p >= 0 and y1 < self.rows and Ressources.grid[y1][x1p] != -1 and Ressources.gridForms[y1][x1p] == -1):
                DestroyBackSlash = False
                break
            elif(i != 0 and x1p < self.colls and x1p >= 0 and y1 < self.rows and Ressources.grid[y1][x1p] != -1 and Ressources.gridForms[y1][x1p] != -1):
                BackSlashScore = BackSlashScore + 1
            if(x2 >= 0 and y2 >= 0 and Ressources.grid[y2][x2] != -1 and Ressources.gridForms[y2][x2] == -1):
                DestroyBackSlash = False
                break
            elif(i != 0 and x2 >= 0 and y2 >= 0 and Ressources.grid[y2][x2] != -1 and Ressources.gridForms[y2][x2] != -1):
                BackSlashScore = BackSlashScore + 1
            if(x2p >= 0 and x2p < self.colls and y2 >= 0 and Ressources.grid[y2][x2p] != -1 and Ressources.gridForms[y2][x2p] == -1):
                DestroyBackSlash = False
                break
            elif(i != 0 and x2p >= 0 and x2p < self.colls and y2 >= 0 and Ressources.grid[y2][x2p] != -1 and Ressources.gridForms[y2][x2p] != -1):
                BackSlashScore = BackSlashScore + 1
        offset = (trType + 1)%2        
        yIndex = yi - offset 
        LineIndex = (xi - yIndex)/2 + 1
        LineIndex = int(LineIndex)
        if(DestroyBackSlash and Ressources.lineToDestroy[2][LineIndex] == -1):
            Ressources.score = Ressources.score + BackSlashScore
            Ressources.lineToDestroy[2][LineIndex] = pos
            
        if(DestroyColl or DestroySlash or DestroyBackSlash):
            Ressources.destroyedSound.play(loops=0, maxtime=0, fade_ms=0)
            Ressources.canPlay = False
            
        
                    
    def DestroyLines(self,form):
        xf = Ressources.selectedTr[0]
        yf = Ressources.selectedTr[1]
        
        xg = Ressources.selectedBgTr[0]
        yg = Ressources.selectedBgTr[1]
        
        if(yf == -1):
            yf = 0
        x = xg - xf
        y = yg - yf
        for i in range(form.rows):
            for j in range(form.colls):
                xi = x+j
                yi = y+i
                if(xi < self.colls and yi < self.rows and xi >= 0 and yi >= 0):
                    if(type(form.boxes[0])==list and form.boxes[i][j] != -1):
                        pos = (xi,yi)
                        self.checkToDestroyIn(pos)
                    elif(type(form.boxes[0])!=list and form.boxes[j] != -1):
                        pos = (xi,yi)
                        self.checkToDestroyIn(pos)
                        
        Ressources.DestroyedForm = form
    def DestAnimation(self):
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        i = Ressources.animationIndex / 100
        AnimationActivated = False
        #rows
        for j in range(len(Ressources.lineToDestroy[0])):
            if(Ressources.lineToDestroy[0][j] != -1):
                AnimationActivated = True
                if(int(i) == i):
                    i = int(i)
                    x = Ressources.lineToDestroy[0][j][0]
                    y = Ressources.lineToDestroy[0][j][1]
                    x1 = x - i
                    x2 = x + i
                    if(x1 >= 0 and Ressources.gridForms[y][x1] != -1):
                        Ressources.gridForms[y][x1].destoy()
                        Ressources.gridForms[y][x1] = -1
                    if(x2 < self.colls and Ressources.gridForms[y][x2] != -1):
                        Ressources.gridForms[y][x2].destoy()
                        Ressources.gridForms[y][x2] = -1
                    if(x1 < 0 and x2 >= self.colls and i >= self.colls):
                        Ressources.lineToDestroy[0][j] = -1
        #slash
        for j in range(len(Ressources.lineToDestroy[1])):
            if(Ressources.lineToDestroy[1][j] != -1):
                AnimationActivated = True
                if(int(i) == i):
                    i = int(i)
                    x = Ressources.lineToDestroy[1][j][0]
                    y = Ressources.lineToDestroy[1][j][1]
                    trType = 0
                    if(Ressources.grid[y][x] != -1):
                        trType = Ressources.grid[y][x].type
                    x1 = x + i
                    y1 = y - i
                    x2 = x - i
                    y2 = y + i
                    if(trType == 0):
                        offset = -1
                    else:
                        offset = 1
                    x1p = x1 + offset
                    x2p = x2 + offset
                    DidSomthing = False
                    if(x1 < self.colls and y1 >= 0 and Ressources.grid[y1][x1] != -1 and Ressources.gridForms[y1][x1] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y1][x1].destoy()
                        Ressources.gridForms[y1][x1] = -1
                        
                    if(x1p < self.colls and x1p >= 0 and y1 >= 0 and Ressources.grid[y1][x1p] != -1 and Ressources.gridForms[y1][x1p] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y1][x1p].destoy()
                        Ressources.gridForms[y1][x1p] = -1
                        
                    if(x2 >= 0 and y2 < self.rows and Ressources.grid[y2][x2] != -1 and Ressources.gridForms[y2][x2] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y2][x2].destoy()
                        Ressources.gridForms[y2][x2] = -1
                        
                    if(x2p >= 0 and x2p < self.colls and y2 < self.rows and Ressources.grid[y2][x2p] != -1 and Ressources.gridForms[y2][x2p] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y2][x2p].destoy()
                        Ressources.gridForms[y2][x2p] = -1
                    if(not DidSomthing and i >= self.colls):
                        Ressources.lineToDestroy[1][j] = -1
                        
        #backslash
        for j in range(len(Ressources.lineToDestroy[2])):
            if(Ressources.lineToDestroy[2][j] != -1):
                AnimationActivated = True
                if(int(i) == i):
                    i = int(i)
                    x = Ressources.lineToDestroy[2][j][0]
                    y = Ressources.lineToDestroy[2][j][1]
                    trType = 0
                    if(Ressources.grid[y][x] != -1):
                        trType = Ressources.grid[y][x].type
                    x1 = x + i
                    x2 = x - i
                    y1 = y + i
                    y2 = y - i
                    if(trType == 0):
                        offset = 1
                    else:
                        offset = -1
                    x1p = x1 + offset
                    x2p = x2 + offset
                    DidSomthing = False
                    if(x1 < self.colls and y1 < self.rows and Ressources.grid[y1][x1] != -1 and Ressources.gridForms[y1][x1] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y1][x1].destoy()
                        Ressources.gridForms[y1][x1] = -1
                        
                    if(x1p < self.colls and x1p >= 0 and y1 < self.rows and Ressources.grid[y1][x1p] != -1 and Ressources.gridForms[y1][x1p] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y1][x1p].destoy()
                        Ressources.gridForms[y1][x1p] = -1
                        
                    if(x2 >= 0 and y2 >= 0 and Ressources.grid[y2][x2] != -1 and Ressources.gridForms[y2][x2] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y2][x2].destoy()
                        Ressources.gridForms[y2][x2] = -1
                        
                    if(x2p >= 0 and x2p < self.colls and y2 >= 0 and Ressources.grid[y2][x2p] != -1 and Ressources.gridForms[y2][x2p] != -1):
                        DidSomthing = True
                        Ressources.gridForms[y2][x2p].destoy()
                        Ressources.gridForms[y2][x2p] = -1
                    if(not DidSomthing and i >= self.colls):
                        Ressources.lineToDestroy[2][j] = -1
                        
        if(AnimationActivated):
            Ressources.animationIndex = Ressources.animationIndex + 5
            if(i >= self.colls):
                Ressources.animationIndex = 0
                if(not Ressources.DestroyedForm.played):
                    Ressources.score = Ressources.score + Ressources.DestroyedForm.score
                    Ressources.DestroyedForm.played = True
                Ressources.canPlay = True
                