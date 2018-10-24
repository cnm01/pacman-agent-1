# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

class PartialAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up!"
        name = "Pacman"
        self.last = Directions.STOP
        self.visited = []
        self.food = []
        self.isTraversing = True
        self.startPos = None
        self.startDir = None
        self.startCtr = 0
        self.counter = 0


    # This is what gets run in between multiple games
    def final(self, state):
        self.last = Directions.STOP
        self.visited = []
        self.food = []
        self.isTraversing = True
        self.startPos = None
        self.startDir = None
        self.startCtr = 0
        self.counter = 0
        print " __________________"
        print "|                  |"
        print "|    Game Over!    |"
        print "|                  |"
        print " ------------------"


    def getAction(self, state):
        self.counter+=1

        ## Choose starting direction and record starting point
        #
        # only runs on first move of game
        if self.isStarting(state) == True:
            return self.start(state)

        # ## Run from ghosts if near
        # if self.ghostNear(state) == True:
        #     return self.runFromGhost(state)


        ## Traverse exterior walls until reaching starting point
        #
        # - stop if endlessly looping
        # - assumes start pos along exterior wall, not in corner
        # - ends when start position reached, while facing same direction
        # - ends if gone back to start point 2 times, to stop endless looping
        if self.isTraversing == True:
            self.incStartCtr(state)
            # continue to explore, unless reached start pos multiple times implying stuck in endless loop of same territory
            if (api.whereAmI(state) != self.startPos):
                return self.traverseExterior(state)
            # end traversal if reached start point, facing same direction as start
            elif (api.whereAmI(state) == self.startPos and self.last == self.startDir):
                self.isTraversing = False
            # continue if reached start point but havent gone over start point multiple times
            elif (api.whereAmI(state) == self.startPos and self.startCtr <= 1):
                return self.traverseExterior(state)
            # end if reached start point and gone over multiple times
            elif (api.whereAmI(state) == self.startPos and self.startCtr > 1):
                self.isTraversing = False
        # entire perimeter traversed




        ## Go to smallest food on map when possible
        #
        # smallest food : westmost/southmost (smallest x then y coord)
        if self.foodOnMap(state):
            return self.goTowardsSmallestFood(state)


        ## Randomly traverse map
        #
        # if no food on map, then randomly look for food
        # continue straightm never go backwards if possible
        return self.randomlySearch(state)

    def isStarting(self, state):
        if self.counter <= 1:
            return True
        else:
            return False

    def foodOnMap(self, state):
        if len(self.food) > 0:
            return True
        else:
            return False

    def incStartCtr(self, state):
        if api.whereAmI(state) == self.startPos:
            print "incrementing startCtr"
            self.startCtr+=1


    def start(self, state):

        if self.last ==Directions.STOP:
            self.startPos = api.whereAmI(state)
            # print "Starting()"
            if Directions.WEST in api.legalActions(state):
                self.last = Directions.WEST
                self.startDir = self.last
                # print "start: west"
                return self.last
            elif Directions.EAST in api.legalActions(state):
                self.last = Directions.EAST
                self.startDir = self.last
                # print "start: east"
                return self.last
            elif Directions.SOUTH in api.legalActions(state):
                self.last = Directions.SOUTH
                self.startDir = self.last
                # print "start: south"
                return self.last
            else:
                self.last = Directions.NORTH
                self.startDir = self.last
                # print "start: north"
                return self.last

    def traverseExterior(self, state):
        self.update(state)

        print "traversing exterior"
        print "--------------------------"

        if Directions.LEFT[self.last] in api.legalActions(state):
            self.last = Directions.LEFT[self.last]
            return self.last
        if self.last in api.legalActions(state):
            self.last = self.last
            return self.last
        if Directions.RIGHT[self.last] in api.legalActions(state):
            self.last = Directions.RIGHT[self.last]
            return self.last
        if Directions.LEFT[Directions.LEFT[self.last]] in api.legalActions(state):
            self.last = Directions.LEFT[Directions.LEFT[self.last]]
            return self.last

    def ghostNear(self, state):
        cur = api.whereAmI(state)
        if len(api.ghosts(state)) > 0:
            return True
        return False

    def ghostDirection(self, state):
        cur = api.whereAmI(state)
        ghosts = api.ghosts(state)
        for x in range(1, 6):
            #east
            if (cur[0]+x, cur[1]) in ghosts:
                return Directions.EAST
            #west
            if (cur[0]-x, cur[1]) in ghosts:
                return Directions.WEST
            #north
            if (cur[0], cur[1]+x) in ghosts:
                return Directions.NORTH
            #south
            if (cur[0], cur[1]-x) in ghosts:
                return Directions.SOUTH


    def runFromGhost(self, state):
        moves = api.legalActions(state)
        moves.remove(Directions.STOP)

        if self.ghostDirection(state) == Directions.NORTH:
            if len(moves) > 1:
                if Directions.NORTH in moves: moves.remove(Directions.NORTH)
                self.last = random.choice(moves)
                return self.last
        if self.ghostDirection(state) == Directions.EAST:
            if len(moves) > 1:
                if Directions.EAST in moves: moves.remove(Directions.EAST)
                self.last = random.choice(moves)
                return self.last
        if self.ghostDirection(state) == Directions.SOUTH:
            if len(moves) > 1:
                if Directions.SOUTH in moves: moves.remove(Directions.SOUTH)
                self.last = random.choice(moves)
                return self.last
        if self.ghostDirection(state) == Directions.WEST:
            if len(moves) > 1:
                if Directions.WEST in moves: moves.remove(Directions.WEST)
                self.last = random.choice(moves)
                return self.last

        self.last = random.choice(moves)
        return self.last


    #returns coordinate of westmost/southmost food
    def smallest(self, state):
        if len(self.food) > 0:
            temp = self.food[0]
            for x in self.food:
                if x[0] < temp[0]:
                    temp = x
                elif x[0] == temp[0]:
                    if x[1] < temp[1]:
                        temp = x
            # print "smallest is ", temp
            return temp
        print "no food on map"


    #go to smallest food
    def goTowardsSmallestFood(self, state):
        print "--------------------------"

        self.update(state)


        print "Attemping to go to smallest food"
        cur = api.whereAmI(state)
        coord = self.smallest(state)
        # print coord
        legal = api.legalActions(state)
        print "smallest food: ", self.smallest(state)

        #if North
        if coord[1] > cur[1]:
            print "food is north"
            if Directions.NORTH in legal:
                self.last = Directions.NORTH
                print "going north"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                print "going random direction"
                return self.last

        #if East
        if coord[0] > cur[0]:
            print "food is east"
            if Directions.EAST in legal:
                self.last = Directions.EAST
                print "going east"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                "going random direction"
                return self.last

        #if South
        if coord[1] < cur[1]:
            print "food is south"
            if Directions.SOUTH in legal:
                self.last = Directions.SOUTH
                print "going south"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                print "going random direction"
                return self.last

        #if West
        if coord[0] < cur[0]:
            print "food is west"
            if Directions.WEST in legal:
                self.last = Directions.WEST
                print "going west"
                return self.last
            elif self.last in legal:
                print "going straight"
                return self.last
            else:
                legal.remove(Directions.STOP)
                self.last = random.choice(legal)
                print "going random direction"
                return self.last




    def followFood(self, state):
        print "following adjacent food"
        self.update(state)
        cur = api.whereAmI(state)
        foodAndCapsules = api.union(api.food(state), api.capsules(state))


        for x in range(1,6):
            #South
            if (cur[0], cur[1]-x) in foodAndCapsules:
                self.last = Directions.SOUTH
                return self.last
            #West
            if (cur[0]-x, cur[1]) in foodAndCapsules:
                self.last = Directions.WEST
                return self.last
            #North
            if (cur[0], cur[1]+x) in foodAndCapsules:
                self.last = Directions.NORTH
                return self.last
            #East
            if (cur[0]+x, cur[1]) in foodAndCapsules:
                self.last = Directions.EAST
                return self.last

    def foodWithin1(self, state):
        cur = api.whereAmI(state)
        foodAndCapsules = api.union(api.food(state), api.capsules(state))

        for x in range(1,6):
            #South
            if (cur[0], cur[1]-x) in foodAndCapsules:
                return True
            #West
            if (cur[0]-x, cur[1]) in foodAndCapsules:
                return True
            #North
            if (cur[0], cur[1]+x) in foodAndCapsules:
                return True
            #East
            if (cur[0]+x, cur[1]) in foodAndCapsules:
                return True
        return False

    def randomlySearch(self, state):
        self.update(state)
        print "randomly searching for food"
        print "--------------------------"
        if self.last in api.legalActions(state):
            return self.last

        #remove stop
        moves = api.legalActions(state)
        moves.remove(Directions.STOP)

        #if at intersection, dont go backwards
        if len(moves) >= 2:
            if self.last == Directions.NORTH:
                moves.remove(Directions.SOUTH)
            if self.last == Directions.SOUTH:
                moves.remove(Directions.NORTH)
            if self.last == Directions.EAST:
                moves.remove(Directions.WEST)
            if self.last == Directions.WEST:
                moves.remove(Directions.EAST)


        self.last = random.choice(moves)
        return self.last


    def update(self, state):
        self.addFood(state)
        self.updateVisited(state)
        self.removeFood(state)

    def updateVisited(self, state):
        coord = api.whereAmI(state)
        if coord not in self.visited:
            self.visited.append(coord)

    def addFood(self, state):
        for x in api.food(state):
            if x not in self.food:
                self.food.append(x)

    def removeFood(self, state):
        for x in self.food:
            if x in self.visited:
                self.food.remove(x)















































    ###
