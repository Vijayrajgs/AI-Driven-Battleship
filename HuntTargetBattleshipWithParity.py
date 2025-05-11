import random
import queue
from tkinter import *
import time

#-------------------------------------------------------------------------------Functions-------------------------------------------------------------------------------#

def randomChoose(matrix):
	x = random.randrange(0,100,1)
	tup = numberToTuple(x)
	while(matrix[tup[0]][tup[1]]==-1):
		x = random.randrange(0,100,1)
		tup = numberToTuple(x)
	return tup

def parityChoose(matrix):
        tup = getParityTup()
        while(matrix[tup[0]][tup[1]]==-1):
            tup = getParityTup()
        return tup

def getParityTup():
    x = random.randrange(0,10,1)
    if(x%2==0):
        y = random.randrange(0,10,2)
    else:
        y = random.randrange(1,10,2)
    tup = (x,y)
    return tup

def numberToTuple(x):
	row = int(x/10)
	col = x-(row*10)
	return (row,col)

def getPlayerShipPosition():
	#GUI
	#For now use arbritary numbers
	"""shipPosition = list()
	ship1 = [(0,0),(0,1),(0,2),(0,3),(0,4)]
	ship2 = [(1,0),(2,0),(3,0),(4,0)]
	ship3 = [(3,8),(4,8),(5,8)]
	ship4 = [(9,7),(9,8),(9,9)]
	ship5 = [(4,2),(5,2)]
	shipPosition = [ship1,ship2,ship3,ship4,ship5]
	return shipPosition"""
	return getCompShipPosition();

def getCompShipPosition():
	
	shipPosition = [0,0,0,0,0]
	finish = list()
	done = list()
	count = 0

	while(count<5):
		
		ship = list()
		
		shipType = random.randrange(1,6,1)
		while(shipType in finish):
			shipType = random.randrange(1,6,1)
		finish.append(shipType)
		
		x = random.randrange(0,10,1)
		y = random.randrange(0,10,1)
		while((x,y) in done):
			x = random.randrange(0,10,1)
			y = random.randrange(0,10,1)
		done.append((x,y))
		ship.append((x,y))
		
		direction = random.randrange(0,2,1)
		shiplen = shipsLen[shipType]-1

		if(direction==0):
			ytemp = y
			while((ytemp-1>=0) and (shiplen!=0) and ((x,ytemp-1) not in done)):
				ship.append((x,ytemp-1))
				done.append((x,ytemp-1))
				shiplen -= 1
				ytemp = ytemp-1
			if(shiplen!=0):
				ytemp = y
				while((ytemp+1<10) and (shiplen!=0) and ((x,ytemp+1) not in done)):
					ship.append((x,ytemp+1))
					done.append((x,ytemp+1))
					shiplen -= 1
					ytemp = ytemp+1
			if(shiplen!=0):
				ship = [(x,y)]
				direction = 1
				shipLen = shipsLen[shipType] - 1

		if(direction==1):
			xtemp = x
			while((xtemp-1>=0) and (shiplen!=0) and ((xtemp-1,y) not in done)):
				ship.append((xtemp-1,y))
				done.append((xtemp-1,y))
				shiplen -= 1
				xtemp = xtemp-1
			if(shiplen!=0):
				xtemp = x
				while((xtemp+1<10) and (shiplen!=0) and ((xtemp+1,y) not in done)):
					ship.append((xtemp+1,y))
					done.append((xtemp+1,y))
					shiplen -= 1
					xtemp = xtemp+1
			if(shiplen!=0):
				ship = [(x,y)]
				direction = 0
				shipLen = shipsLen[shipType] - 1

		if(shiplen==0):
			shipPosition[shipType-1] = ship
			count+=1

	return shipPosition

def makeMatrix(shipPosition):
	matrix = list()
	for i in range(0,10):
		matrix.append([0,0,0,0,0,0,0,0,0,0])
	num = 1
	for i in shipPosition:
		for j in i:
			matrix[j[0]][j[1]] = num
		num=num+1 
	return matrix

def huntTargetMode(matrix,hitFlag):
        global targetQueue 
        if(targetQueue.empty() and hitFlag[1]<0):
                return randomChoose(matrix)
        elif(hitFlag[1]<0 and not(targetQueue.empty())):
                return targetQueue.get()
        elif(hitFlag[1]>=0):
                coor = [(hitFlag[0],hitFlag[1]-1),(hitFlag[0],hitFlag[1]+1),(hitFlag[0]-1,hitFlag[1]),(hitFlag[0]+1,hitFlag[1])]
                for i in coor:
                        if(i[0]<10 and i[0]>=0 and i[1]<10 and i[1]>=0 and matrix[i[0]][i[1]]>=0):
                                targetQueue.put(i)
                if(targetQueue.empty()):
                        return randomChoose(matrix)
                else:
                        return targetQueue.get()

def huntTargetwithParityMode(matrix,hitFlag):
        global pTargetQueue 
        if(pTargetQueue.empty() and hitFlag[1]<0):
                return parityChoose(matrix)
        elif(hitFlag[1]<0 and not(pTargetQueue.empty())):
                return pTargetQueue.get()
        elif(hitFlag[1]>=0):
                coor = [(hitFlag[0],hitFlag[1]-1),(hitFlag[0],hitFlag[1]+1),(hitFlag[0]-1,hitFlag[1]),(hitFlag[0]+1,hitFlag[1])]
                for i in coor:
                        if(i[0]<10 and i[0]>=0 and i[1]<10 and i[1]>=0 and matrix[i[0]][i[1]]>=0):
                                pTargetQueue.put(i)
                if(pTargetQueue.empty()):
                        return parityChoose(matrix)
                else:
                        return pTargetQueue.get()


#-------------------------------------------------------------------------------GUI Code-------------------------------------------------------------------------------#
class Block:
        def  __init__(self, x1, y1, x2, y2):
                self.x1 = x1;
                self.y1 = y1;
                self.x2 = x2;
                self.y2 = y2;
                self.marked = 0;
                self.ship = 0;
                self.colour = "white";

        def checkClick(self, x, y):
                if((x>=self.x1) and (x<=self.x2) and (x>=self.x1) and (x<=self.x2)):
                    return 1;
                else:
                    return 0;
   
        def markBlock(self, canvas):
                if(self.ship==0):
                        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="red", width =2);
                        canvas.create_line(self.x1+50, self.y1, self.x2-50, self.y2, fill="red", width=2);
                else:
                        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.colour)
                        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="white", width =2);
                        canvas.create_line(self.x1+50, self.y1, self.x2-50, self.y2, fill="white", width=2);
                self.marked=1;

                
        def setShip(self, x, canvas):
                print(x);
                self.ship = x;
                if(x==1):
                        self.colour = "green"
                elif(x==2):
                        self.colour = "violet"
                elif(x==3):
                        self.colour = "blue"
                elif(x==4):
                        self.colour = "orange"
                elif(x==5):
                        self.colour = "black"

class RootClass:
        def __init__(self, name):
             print("Hmm, Will this Work?");
             self.Blocks = [];
             self.canvas=0;
             self.name = name;
             self.x=-1;
             self.y=-1;
             self.clickedFlag=0;
             self.rows=0;
             self.cols=0;
             
        def getCanvas(self):
            return self.canvas;

        def getClickedBox(self, event):
            self.clickedFlag=0;
            for i in range (0, self.rows):
                        for j in range (0, self.cols):
                                if((self.Blocks[i][j].marked==0)and(self.Blocks[i][j].checkClick(event.x, event.y)==1)):
                                       self.x=i;
                                       self.y=j;
                                       self.clickedFlag=1;
        
        def create_grid(self, rows, columns, event=None):
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            self.canvas.delete('grid_line')
            for i in range(0, w, int(w/rows)):
                self.canvas.create_line([(i, 0), (i, h)], tag='grid_line', width=2)
            for i in range(0, h, int(h/columns)):
                self.canvas.create_line([(0, i), (w, i)], tag='grid_line', width=2)

        def getBlocks(self):
            return self.Blocks;
        
        def makeRoot(self, matrix, root):
                rows = len(matrix)
                root.title(self.name);
                columns = len(matrix[0])
                self.rows = rows;
                self.cols = columns
                self.canvas = Canvas(root, height=500, width=500, bg='white')
                self.canvas.pack(fill=BOTH, expand=True)
                w = 500
                h = 500
                self.canvas.bind('<Configure>', lambda X: self.create_grid(rows, columns));
                for i in range(0,rows):
                        self.Blocks.append([0,0,0,0,0,0,0,0,0,0]);

                for i in range(0, w, int(w/rows)):
                        for j in range(0, h, int(h/columns)):
                                self.Blocks[int(i/50)][int(j/50)] = Block(i, j, i+50, j+50);
                
                for i in range (0, rows):
                        for j in range (0, columns):
                                if(matrix[i][j]!=0):
                                        self.Blocks[i][j].setShip(matrix[i][j], self.canvas);
        def Update(self, root):
                root.update();

def getPlayerPosition(Obj):
        canvas = Obj.getCanvas()
        print("helloWorld")
        canvas.bind("<Button-1>", lambda:getClickedBox())
        while((Obj.x==-1) and (Obj.y==-1)):
                pass
        p = tuple(Obj.x, Obj.y)
        Obj.x=-1
        Obj.y=-1
        canvas.unbind("<Button-1>")

#-------------------------------------------------------------------------------Global Variables-------------------------------------------------------------------------------#

shipsLen = {1:5,2:4,3:3,4:3,5:2}
shipName = {1:"Aircraft Carrier",2:"Battleship",3:"Submarine",4:"Cruiser",5:"Destroyer"}
targetQueue = queue.Queue(maxsize=50)
pTargetQueue = queue.Queue(maxsize=50)
pShipLengths = [5,4,3,3,2]
cShipLengths = [5,4,3,3,2]
playerSunk = list()
compSunk = list()

pShipPosition = getPlayerShipPosition()
playerMatrix = makeMatrix(pShipPosition)

cShipPosition = getCompShipPosition()
#print(cShipPosition)
compMatrix = makeMatrix(cShipPosition)
hitFlag = (-1,-1)
pHitFlag = (-1,-1)

playerRoot = Tk();
computerRoot = Tk();

PObj = RootClass("Player's Board - H and T with Parity");
CObj = RootClass("Computer's Board - H and T");

PObj.makeRoot(playerMatrix, playerRoot);
CObj.makeRoot(compMatrix, computerRoot);


#-------------------------------------------------------------------------------Main Code-------------------------------------------------------------------------------#

while((len(playerSunk)!=5) and (len(compSunk)!=5)): 
	
        print("\nPlayer's Chance:")
        #p = input("Enter x,y coordinates of your move: ")
        #p = huntTargetMode(compMatrix, pHitFlag);
        #x = int(p[0])
        #y = int(p[2])
        #y = int(p[1])
        CObj.Update(computerRoot)
        p = getPlayerPosition(CObj)
        while(compMatrix[p[0]][p[1]]==-1):
                print(p,"is already played")
                temp = input("Enter a new x,y coordinate: ")
                temp = huntTargetMode(compMatrix, pHitFlag);
                x = int(temp[0])
                y = int(temp[2])
                y = int(temp[1]);
                p = (x,y)
        pflag = compMatrix[p[0]][p[1]]
        compMatrix[p[0]][p[1]] = -1
        CObj.Update(computerRoot)
        Blocks = CObj.getBlocks()
        Blocks[p[0]][p[1]].markBlock(CObj.getCanvas());
        if(pflag>0):
                pHitFlag = (p[0],p[1])
                print("Player has Hit")
                cShipLengths[pflag-1] -= 1
                if(cShipLengths[pflag-1]==0):
                        compSunk.append(pflag)
                        print("Computer's ship",shipName[pflag],"of length",shipsLen[pflag],"has sunk")
        else:
                pHitFlag = (-1,-1)
                print("Player has Miss")

        print("\nComputer's Chance:")
        c = huntTargetwithParityMode(playerMatrix,hitFlag)
        print("Computer plays:",c)
        flag = playerMatrix[c[0]][c[1]]
        playerMatrix[c[0]][c[1]] = -1
        time.sleep(0.5)
        PObj.Update(playerRoot)
        Blocks = PObj.getBlocks()
        Blocks[c[0]][c[1]].markBlock(PObj.getCanvas());
        if(flag>0):
                print("Computer has hit")
                hitFlag = (c[0],c[1])
                pShipLengths[flag-1] -= 1
                if(pShipLengths[flag-1]==0):
                        playerSunk.append(flag)
                        print("Your ship",shipName[flag],"of length",shipsLen[flag],"has sunk")
        else:
                print("Computer has Miss")
                hitFlag = (-1,-1)
        print()
        print()
        time.sleep(0.5)
        CObj.Update(computerRoot)
        PObj.Update(playerRoot)

if(len(playerSunk)==5):
	print("Computer Wins")
else:
	print("Player Wins")

time.sleep(20)

