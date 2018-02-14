import numpy as np
from sets import Set

class Robot(object):
    def __init__(self, maze_dim):
        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.maze_grid = np.zeros((maze_dim, maze_dim))
        self.run = 0
        self.canPop = True
        self.goal_bounds = [self.maze_dim/2 - 1, self.maze_dim/2]
        self.current = self.Node([0, 0])
        
        #Change this variable for the optimization phase
        self.optimization = 'aStar' #Can be aStar or floodFill
        
        if self.optimization == 'floodFill':
            self.stack = self.Stack(('up', [0,0]))
            self.visited = self.Stack(self.Node([0,0]))
        elif self.optimization == 'aStar':
            self.stack = self.Stack(('up', self.Node([0,0])))
            self.visited = self.Stack(self.Node([0,0]))
        
        self.count = 1
        self.floodFillValue = 0

    def next_move(self, sensors):
        rotation = 0
        movement = 0

        #print self.location
        
        #print 'heading = ' + str(self.heading)
        print '-------------------------------------------'
        print 'location = ' + str(self.location)
        print 'heading = ' + self.heading
        print 'sensors = '  + str(sensors)
        print 'visited = ',
        for s in self.visited.items:
            if not isinstance(s, self.Node):
                print str(s) + ',',
            else:
                print str(s.location) + ',',
        print ' '
        print 'stack = ',
        for s in self.stack.items:
            if not isinstance(self.stack.top()[1], self.Node):
                print '(' + str(s[0]) + ', ' + str(s[1]) + '),',
            else:
                print str(s[1].location) + ',',
        print ' '
        print 'count = '  + str(self.count)

        self.count += 1
        
        #Found goal
        if self.run == 0 and self.location[0] in self.goal_bounds and self.location[1] in self.goal_bounds:
            print self.goal_bounds
            self.run += 1
            self.location = [0, 0]
            self.heading = 'up'
            self.canPop = True
            if self.optimization == 'dfs':
                self.stack = self.Stack(('up', [0,0]))
                self.visited = self.Stack([0,0])
            elif self.optimization == 'aStar':
                self.stack = self.Stack(('up', self.Node([0,0])))
                self.visited = self.Stack(self.Node([0,0]))
            elif self.optimization == 'floodFill':
                self.stack = self.Stack(('up', [0,0]))
                self.visited = self.Stack(self.Node([0,0]))
            print self.optimization
            return 'Reset', 'Reset'
        
        self.printGrid()
        if self.run == 0:
            return self.depth_first_search(sensors)
        elif self.run == 1:
            #return self.depth_first_search(sensors)#Flood fill using DFS
            return self.a_star_search(sensors)
    
    def depth_first_search(self, sensors):
        canMoveLeft = False
        canMoveForward = False
        canMoveRight = False
        
        if sensors[0] > 0:
            canMoveLeft = True

        if sensors[1] > 0:
            canMoveForward = True
        
        if sensors[2] > 0:
            canMoveRight = True
        
        rotation = 0
        movement = 1
        
        successors = []
        if self.run == 0 and self.optimization == 'floodFill':
            #self.floodFillValue += 1
            successors = self.generateSuccessors(sensors)
    
        visited = self.visited.items
    
        #Check heading. It is facing down in this case
        if(self.heading == 'down'):
            #Check if can move right
            if canMoveRight and [self.location[0] - 1, self.location[1]] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0] - 1][self.location[1]] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0] - 1][self.location[1]] > self.floodFillValue))):
                self.heading = 'left'
                print self.location
                print self.maze_grid[self.location[0]][self.location[1]]
                print self.maze_grid[self.location[0] - 1][self.location[1]]
                print self.maze_grid[self.location[0] - 1][self.location[1]] > self.floodFillValue
                print self.floodFillValue
                print 'dfs IN HERE'
                
                self.location[0] -= 1
                rotation = 90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1

            #Check if can move forward
            elif canMoveForward and [self.location[0], self.location[1] - 1] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] - 1] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] - 1] > self.floodFillValue))):
                self.location[1] -= 1
                rotation = 0
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1


            #Check if can move left
            elif canMoveLeft and [self.location[0] + 1, self.location[1]] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0] + 1][self.location[1]] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0] + 1][self.location[1]] > self.floodFillValue))):
                self.heading = 'right'
                self.location[0] += 1
                rotation = -90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1

            
            #Hit a dead or surrounded by all visited nodes
            else:
                return self.back_up()
    
        #Check heading. It is facing right in this case
        elif self.heading == 'right':
            #Check if can move right
            if canMoveRight and [self.location[0], self.location[1] - 1] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] - 1] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] - 1] > self.floodFillValue))):
                self.heading = 'down'
                self.location[1] -= 1
                rotation = 90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1

            
            #Check if can move forward
            elif canMoveForward and [self.location[0] + 1, self.location[1]] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0] + 1][self.location[1]] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0] + 1][self.location[1]] > self.floodFillValue))):
                self.location[0] += 1
                rotation = 0
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1
                
            #Check if can move left
            elif canMoveLeft and [self.location[0], self.location[1] + 1] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] + 1] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] + 1] > self.floodFillValue))):
                self.heading = 'up'
                self.location[1] += 1
                rotation = -90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1


            #Hit a dead or surrounded by all visited nodes
            else:
                return self.back_up()
    
        #Check heading. It is facing up in this case
        elif self.heading == 'up':
            print 'IN HERE up'
            #Check if can move right
            if canMoveRight and [self.location[0] + 1, self.location[1]] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0] + 1][self.location[1]] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0] + 1][self.location[1]] > self.floodFillValue))):
                self.heading = 'right'
                self.location[0] += 1
                rotation = 90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1


            #Check if can move forward
            elif canMoveForward and [self.location[0], self.location[1] + 1] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] + 1] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] + 1] > self.floodFillValue))):
                self.location[1] += 1
                rotation = 0
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1


            #Check if can move left
            elif canMoveLeft and [self.location[0] - 1, self.location[1]] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0] - 1][self.location[1]] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0] - 1][self.location[1]] > self.floodFillValue))):
                self.heading = 'left'
                self.location[0] -= 1
                rotation = -90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1


            #Hit a dead or surrounded by all visited nodes
            else:
                return self.back_up()
            
        #Check heading. It is facing left in this case
        elif self.heading == 'left':
            #Check if can move right
            if canMoveRight and [self.location[0], self.location[1] + 1] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] + 1] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] + 1] > self.floodFillValue))):
                self.heading = 'up'
                self.location[1] += 1
                rotation = 90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1

        
            #Check if can move forward
            elif canMoveForward and [self.location[0] - 1, self.location[1]] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0] - 1][self.location[1]] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0] - 1][self.location[1]] > self.floodFillValue))):
                self.location[0] -= 1
                rotation = 0
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1

            
            #Check if can move left
            elif canMoveLeft and [self.location[0], self.location[1] - 1] not in self.visited.items and (self.run == 0 or self.run != 0 and ((self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] - 1] == 1) or (self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] - 1] > self.floodFillValue))):
                self.heading = 'down'
                self.location[1] -= 1
                rotation = -90
                if self.run == 0 and self.optimization == 'floodFill':
                    self.floodFillValue += 1
                
            #Hit a dead or surrounded by all visited nodes
            else:
                return self.back_up()

        print 'floodFillValue = ' + str(self.floodFillValue)
        #if self.run == 0 and self.optimization == 'aStar':
        if self.run == 0 and self.optimization == 'aStar':
            self.maze_grid[self.location[0]][self.location[1]] = 1
        if self.run == 0 and self.optimization == 'floodFill':
            for s in successors:
                self.maze_grid[s.location[0]][s.location[1]] = s.f
        self.visited.push([self.location[0], self.location[1]])
        if not self.stack.containsItem(self.location):
            self.stack.push((self.heading, [self.location[0], self.location[1]]))
        if self.canPop == False:
            self.canPop = True
        return rotation, movement

    def back_up(self):
        print 'BACKING UP'
        #print self.canPop
        rotation = 0
        movement = 0
        print 'top of stack = ' + str(self.stack.top())
        self.prev_heading = self.stack.top()[0]
        
        if self.canPop == True and self.location != [0,0]:
            if self.run == 0 and self.optimization == 'aStar':
                self.maze_grid[self.location[0]][self.location[1]] = 0
            self.stack.pop()
        
        if not isinstance(self.stack.top()[1], self.Node):
            x = self.stack.top()[1][0]
            y = self.stack.top()[1][1]
        else:
            print 'top of stack: ' + self.stack.top()[0] + ', ' + str(self.stack.top()[1].location)
            x = self.stack.top()[1].location[0]
            y = self.stack.top()[1].location[1]
        if self.heading != self.stack.top()[0] and self.location != [x,y]:
            print 'Backing up1'
            self.updateLocationByBackingUp(x, y)
            if self.canPop == True:
                self.canPop = False
            self.floodFillValue = self.maze_grid[x][y]
            print 'floodFillValue = ' + str(self.floodFillValue)
            return 0, -1
        elif self.heading == self.stack.top()[0]:
            print 'Backing up2'
            self.updateLocationByBackingUp(x, y)
            if self.canPop == False:
                self.canPop = True
            self.floodFillValue = self.maze_grid[x][y]
            print 'floodFillValue = ' + str(self.floodFillValue)
            return 0, -1
        else:
            print 'ROTATING'
            if self.heading == 'down':
                if self.stack.top()[0] == 'right':
                    rotation = -90
                elif self.stack.top()[0] == 'left':
                    rotation = 90
            elif self.heading == 'right':
                if self.stack.top()[0] == 'down':
                    rotation = 90
                elif self.stack.top()[0] == 'up':
                    rotation = -90
            elif self.heading == 'up':
                if self.stack.top()[0] == 'right':
                    rotation = 90
                elif self.stack.top()[0] == 'left':
                    rotation = -90
            elif self.heading == 'left':
                if self.stack.top()[0] == 'down':
                    rotation = -90
                elif self.stack.top()[0] == 'up':
                    rotation = 90

            self.heading = self.stack.top()[0]
            if self.canPop == False:
                self.canPop = True
            return rotation, movement
    
    def updateLocationByBackingUp(self, x, y):
        # Go back to the previous location
        if x > self.location[0]:
            #print 'here1'
            self.location[0] += 1
        elif x < self.location[0]:
            #print 'here2'
            self.location[0] -= 1
        
        if y > self.location[1]:
            #print 'here3'
            self.location[1] += 1
        elif y < self.location[1]:
            #print 'here4'
            self.location[1] -= 1

    #Exploration run using A* Shortest Path Algorithm
    def a_star_search(self, sensors):
        print 'a_star'
        leastCostNode = None
        successors = self.generateSuccessors(sensors)
        if len(successors) > 0:
            leastCostNode = self.getNextSuccessor(successors)
            self.visited.push(leastCostNode)
            self.current = leastCostNode
            return self.determineNextMove(sensors, leastCostNode)
        else:
            return self.back_up()

    def getNextSuccessor(self, successors):
        leastCostNode = None
        
        if len(successors) > 0:
            leastCostNode = successors[0]
            for s in successors:
                if s.f < leastCostNode.f:
                    leastCostNode = s
                elif s.f == leastCostNode.f:
                    if s.h < leastCostNode.h:
                        leastCostNode = np.random.choice([leastCostNode, h])
        return leastCostNode

    def generateSuccessors(self, sensors):
        print 'generate'
        #print str(self.location[0]) + ', ' + str(self.location[1])
        canMoveLeft = False
        canMoveForward = False
        canMoveRight = False
        
        if sensors[0] > 0:
            canMoveLeft = True

        if sensors[1] > 0:
            canMoveForward = True
        
        if sensors[2] > 0:
            canMoveRight = True
        
        successors = []

        nodeNorth = None
        nodeSouth = None
        nodeEast = None
        nodeWest = None
        
        print self.visited.items[0].location
        
        visited = []
        for i in self.visited.items:
            if not isinstance(i, self.Node):
                visited.append(i)
            else:
                visited.append(i.location)
        
        print 'visited = ' + str(visited)

        #North
        if self.location[1] < self.maze_dim - 1 and [self.location[0], self.location[1] + 1] not in visited and ((self.heading == 'up' and sensors[1] > 0) or (self.heading == 'left' and sensors[2] > 0) or (self.heading == 'right' and sensors[0] > 0)) and ((self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] + 1] == 0) or (self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] + 1] != 0)):
            print 'creating node north'
            nodeNorth = self.Node([self.location[0], self.location[1] + 1])
            if self.optimization == 'aStar':
                nodeNorth.g = 10 + self.current.g
                nodeNorth.h = self.manhattenDistance(nodeNorth.location[0], nodeNorth.location[1])
                nodeNorth.f = nodeNorth.g + nodeNorth.h
            elif self.optimization == 'floodFill':
                nodeNorth.f = self.floodFillValue + 1

        #South
        if self.location[1] > 0 and [self.location[0], self.location[1] - 1] not in visited and ((self.heading == 'down' and sensors[1] > 0) or (self.heading == 'left' and sensors[0] > 0) or (self.heading == 'right' and sensors[2] > 0)) and ((self.optimization == 'floodFill' and self.maze_grid[self.location[0]][self.location[1] - 1] == 0) or (self.optimization == 'aStar' and self.maze_grid[self.location[0]][self.location[1] - 1] != 0)):
            print 'creating node south'
            nodeSouth = self.Node([self.location[0], self.location[1] - 1])
            if self.optimization == 'aStar':
                nodeSouth.g = 10 + self.current.g
                nodeSouth.h = self.manhattenDistance(nodeSouth.location[0], nodeSouth.location[1])
                nodeSouth.f = nodeSouth.g + nodeSouth.h
            elif self.optimization == 'floodFill':
                nodeSouth.f = self.floodFillValue + 1
        
        #East
        if self.location[0] < self.maze_dim - 1 and [self.location[0] + 1, self.location[1]] not in visited and ((self.heading == 'up' and sensors[2] > 0) or (self.heading == 'down' and sensors[0] > 0) or (self.heading == 'right' and sensors[1] > 0)) and ((self.optimization == 'floodFill' and self.maze_grid[self.location[0] + 1][self.location[1]] == 0) or (self.optimization == 'aStar' and self.maze_grid[self.location[0] + 1][self.location[1]] != 0)):
            print 'creating node east'
            nodeEast = self.Node([self.location[0] + 1, self.location[1]])
            if self.optimization == 'aStar':
                nodeEast.g = 10 + self.current.g
                nodeEast.h = self.manhattenDistance(nodeEast.location[0], nodeEast.location[1])
                nodeEast.f = nodeEast.g + nodeEast.h
            elif self.optimization == 'floodFill':
                nodeEast.f = self.floodFillValue + 1
        
        #West
        if self.location[0] > 0 and [self.location[0] - 1, self.location[1]] not in visited and ((self.heading == 'up' and sensors[0] > 0) or (self.heading == 'down' and sensors[2] > 0) or (self.heading == 'left' and sensors[1] > 0)) and ((self.optimization == 'floodFill' and self.maze_grid[self.location[0] - 1][self.location[1]] == 0) or (self.optimization == 'aStar' and self.maze_grid[self.location[0] - 1][self.location[1]] != 0)):
            nodeWest = self.Node([self.location[0] - 1, self.location[1]])
            if self.optimization == 'aStar':
                nodeWest.g = 10 + self.current.g
                nodeWest.h = self.manhattenDistance(nodeWest.location[0], nodeWest.location[1])
            elif self.optimization == 'floodFill':
                nodeWest.f = self.floodFillValue + 1

        if nodeNorth != None:
            successors.append(nodeNorth)
        
        if nodeSouth != None:
            successors.append(nodeSouth)
        
        if nodeEast != None:
            successors.append(nodeEast)
        
        if nodeWest != None:
            successors.append(nodeWest)

        #if successors != None:
            #self.floodFillValue += 1

        print 'successors = [',
        for s in successors:
            print '(f: ' + str(s.f) + ', h: ' + str(s.h) + ', g: ' +  str(s.g) + ', ' + str(s.location) + '),',
        print '] '
        return successors
    
    def manhattenDistance(self, x, y):
        return abs(x - self.goal_bounds[0]) + abs(y - self.goal_bounds[1])
    
    def findLeastFScoreInOpenList(self):
        min = self.openList.get(0)
        for i in self.openList.items:
            if min.f > i.f:
                min = i

        return min
        
    def determineNextMove(self, sensors, n):
        #print 'determining next move'
        canMoveLeft = False
        canMoveForward = False
        canMoveRight = False
        print 'location: ' + str(self.location)
        print 'n: ' + str(n.location)
        
        x = n.location[0]
        y = n.location[1]
        
        if sensors[0] > 0:
            canMoveLeft = True

        if sensors[1] > 0:
            canMoveForward = True
        
        if sensors[2] > 0:
            canMoveRight = True
        
        rotation = 0
        movement = 1

        if self.location[0] < x:
            if self.heading == 'up' and canMoveRight:
                print 'IN HERE'
                self.heading = 'right'
                if not any(i[1].location == [self.location[0] + 1, self.location[1]] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[0] += 1
                rotation = 90

            elif self.heading == 'down' and canMoveLeft:
                print 'IN HERE2'
                self.heading = 'right'
                if not any(i[1].location == [self.location[0] + 1, self.location[1]] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[0] += 1
                rotation = -90

            elif self.heading == 'right' and canMoveForward:
                print 'IN HERE3'
                if not any(i[1].location == [self.location[0] + 1, self.location[1]] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[0] += 1
                rotation = 0
                
        if self.location[0] > x:
            if self.heading == 'up' and canMoveLeft:
                print 'IN HERE4'
                self.heading = 'left'
                if not any(i[1].location == [self.location[0] - 1, self.location[1]] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[0] -= 1
                rotation = -90
            
            elif self.heading == 'down' and canMoveRight:
                print 'IN HERE5'
                self.heading = 'left'
                if not any(i[1].location == [self.location[0] - 1, self.location[1]] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[0] -= 1
                rotation = 90
            
            elif self.heading == 'left' and canMoveForward:
                print 'IN HERE6'
                if not any(i[1].location == [self.location[0] - 1, self.location[1]] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[0] -= 1
                rotation = 0

        if self.location[1] < y:
            if self.heading == 'up' and canMoveForward:
                print 'IN HERE7'
                if not any(i[1].location == [self.location[0], self.location[1] + 1]  for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[1] += 1
                rotation = 0
            
            elif self.heading == 'left' and canMoveRight:
                print 'IN HERE8'
                self.heading = 'up'
                if not any(i[1].location == [self.location[0], self.location[1] + 1] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[1] += 1
                rotation = 90
            
            elif self.heading == 'right' and canMoveLeft:
                print 'IN HERE9'
                self.heading = 'up'
                if not any(i[1].location == [self.location[0], self.location[1] + 1] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[1] += 1
                rotation = -90

        if self.location[1] > y:
            if self.heading == 'down' and canMoveForward:
                print 'IN HERE10'
                if not any(i[1].location == [self.location[0], self.location[1] - 1] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[1] -= 1
                rotation = 0
            
            elif self.heading == 'left' and canMoveLeft:
                print 'IN HERE11'
                self.heading = 'down'
                if not any(i[1].location == [self.location[0], self.location[1] - 1] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[1] -= 1
                rotation = -90
            
            elif self.heading == 'right' and canMoveRight:
                print 'IN HERE12'
                self.heading = 'down'
                if not any(i[1].location == [self.location[0], self.location[1] - 1] for i in self.stack.items):
                    self.stack.push((self.heading, n))
                self.location[1] -= 1
                rotation = 90
                
        if self.canPop == False:
            self.canPop = True
        #self.maze_grid[n.location[0]][n.location[1]] = 1
        return rotation, movement

    def printGrid(self):
        for i in range(self.maze_dim):
            for j in range(self.maze_dim):
                print int(self.maze_grid[i][j]),
            print ' '
        
    class Stack:
        def __init__(self, x):
            if x is None:
                self.items = []
            else:
                self.items = [x]

        def isEmpty(self):
            return self.items == []

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop()

        def top(self):
            return self.items[len(self.items)-1]

        def size(self):
            return len(self.items)
        
        def get(self, i):
            return self.items[i]
        
        def items(self):
            return self.items
        
        def containsItem(self, x):
            for i in self.items:
                if x == i[1]:
                    return True
            return False

    class Node:
        def __init__(self, location):
            self.f = 0
            self.g = 0
            self.h = 0
            self.location = location
