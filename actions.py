#!/usr/bin/env python3
# actions.py
# Authors: Guillaume de Moffarts, Christophe Simons

# Version: May 21, 2017
# -*- coding: utf-8 -*-

import json
import copy
from Three import Tree
#This package realy shouldn't be in a AI code. Shame on me
import random
board = [[[None, None, None, None],[None, None, None, None],[None,None,None,None],[None,None,None,None]],[[None, None, None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]
#board = [[[None, None, None, None],[None, None, None, None],[None,None,None,None],[None,None,None,None]],[[None, None, None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]

state = {'reserve' : [0, 2], 'turn': 1, 'board' : board}


#action = {'move': 'place', 'to':[0,2,1]}
moves = []

class Movement():
    '''Respresent possible Movements for a state of Pylos game'''
    def allPlace(self, st, layerRes = None):
        '''return possible placements of ball for a given state'''
        mvs = []

        #give a layer restriction for the search
        if layerRes == None:
            a = 0
            b = 4
        else:
            a = layerRes
            b = layerRes + 1

        for layer in range(a,b):
            for row in range(4-layer):
                for column in range(4-layer):
                    if st['board'][layer][row][column] == None:
                        if not self.feelTheMagic(st['board'], layer, row, column):
                            move = {
                                'move': 'place',
                                'to': [layer, row, column]
                            }

                            if layerRes == None:
                                nextState = self.applyAction(st, move)
                                #check if the placement make a square around it
                                if (self.checkSquare(nextState, layer, row, column) or
                                    self.checkSquare(nextState, layer, row, column-1) or
                                    self.checkSquare(nextState, layer, row-1, column-1) or
                                    self.checkSquare(nextState, layer, row -1, column)):
                                    mvs += self.remove(self.allRemove(nextState), move)
                                else:
                                    mvs.append(move)
                                    pass
                            else:
                                mvs.append(move)
        return mvs

    def feelTheMagic(self, st, layer, row, column):
        '''return true if the specifeid ball float in the air'''
        feelTheMagic = False
        for i in range(2):
            for j in range(2):
                if layer != 0:
                    if st[layer-1][row+i][column+j] == None:
                        feelTheMagic = True

        return feelTheMagic


    def feelThePressure(self, st, layer, row, column):
        '''return true is the specified ball can't be remove'''
        feelThePressure = False
        for i in range(2):
            for j in range(2):
                if layer < 3 and 0 <= row-i < 3-layer and 0 <= column-j < 3-layer:
                    if st[layer+1][row-i][column-j] != None:
                        feelThePressure = True

        return feelThePressure

    def allMoves(self, st):
        '''return all possible movement of ball for a specifeid state'''
        mvs = []
        removes = self.allRemove(st)
        for rmv in removes:
            layer = rmv[0]
            row = rmv[1]
            column = rmv[2]
            stcopy = copy.deepcopy(st)
            stcopy['board'][layer][row][column] = None
            movs = self.allPlace(stcopy, layer + 1)
            for mv in movs:
                move = {
                    'move': 'move',
                    'from': [layer, row, column],
                    'to': mv['to']
                }
                nextState = self.applyAction(st, move)
                l = mv['to'][0]
                r =  mv['to'][1]
                c =  mv['to'][2]
                #check if the placement make a square around it
                if (self.checkSquare(nextState, l, r, c) or
                    self.checkSquare(nextState, l, r, c-1) or
                    self.checkSquare(nextState, l, r-1, c-1) or
                    self.checkSquare(nextState, l, r -1, c)):
                    mvs += self.remove(self.allRemove(nextState), move)
                else:
                    mvs.append(move)
        return mvs

    def allRemove(self, st):
        '''return a all balls that can be removed for one player'''
        remove = []
        for layer in range(3):
            for row in range(4-layer):
                for column in range(4-layer):
                    if (
                        st['board'][layer][row][column] == st['turn'] and
                        not self.feelThePressure(st['board'], layer, row, column)
                    ):
                        remove.append([layer, row, column])
        return remove

    def checkSquare(self, st, layer, row, column):
        '''return True if the specifeid ball make a square from its upper left corner'''
        for i in range(2):
            for j in range(2):
                if layer < 3 and 0 <= row+i <= 3-layer and 0 <= column+j <= 3-layer:
                    if st['board'][layer][row+i][column+j] != st['turn']:
                        return False
                else:
                    return False
        return True

    def remove(self, freeMarble, move):
        '''add to a movement combination of balls to be removed'''
        mvs = []
        for i in range(len(freeMarble)):
            for j in range(i+1,len(freeMarble)):
                #give the combination for two balls
                move['remove'] = [freeMarble[i],freeMarble[j]]
                mv = copy.deepcopy(move)
                mvs.append(mv)
        for rmv in freeMarble:
            move['remove'] = [rmv]
            mv = copy.deepcopy(move)
            mvs.append(mv)
        return mvs

    def applyAction(self, st, action, cost = False):
        '''return a nex state after appling a movment to it'''
        nextState = copy.deepcopy(st)
        if action['move'] == 'place':
            to =action['to']
            nextState['board'][to[0]][to[1]][to[2]] = nextState['turn']
        elif action['move'] == 'move':
            to = action['to']
            from_ =action['from']
            nextState['board'][from_[0]][from_[1]][from_[2]] = None
            nextState['board'][to[0]][to[1]][to[2]] = nextState['turn']

        if 'remove' in action:
            for rem in action['remove']:
                nextState['board'][rem[0]][rem[1]][rem[2]] = None

        #cost can be added to change the value of the ball's reserve
        if cost:
            cst = 0
            if action['move'] == 'place':
                cst = -1
            elif action['move'] == 'move':
                cst = 0
            if 'remove' in action:
                cst += len (action['remove'])
            nextState['reserve'][nextState['turn']] += cst
        return nextState

    def printMove(self, mv):
        '''print movements in a nicer way'''
        output = ''
        for elem in mv:
            if elem['move'] == 'place':
                output = '+ ' + str(elem['to'])
            elif elem['move'] == 'move':
                output = str(elem['from']) + '-->' + str(elem['to'])
            if 'remove' in elem:
                output += ' - ' + str(elem['remove'])
            print(output)

    def treeMaker(self, st, action = None, i = None):
        '''recursive function that return the tree of the possible states.
            the values of the parents are given by th minMax method'''

        delta  = 0
        children = []
        mvs =[]

        #switch the player for every turn
        if st['turn'] == 1:
            st['turn'] = 0
        else:
            st['turn'] = 1

        mvs = self.allPlace(st)
        mvs += self.allMoves(st)

        #i given the depth of the tree
        #stop the tree when a player doesn't have any ball left
        if ((i < 1 and i != None) or
            st['reserve'][0] == 0 or
            st['reserve'][1] == 0):
            delta = st['reserve'][0]-st['reserve'][1]
            return Tree(delta, action)

        i -= 1
        for mv in mvs:
            #for every child create a new tree. Stop when no more movements
            child = self.treeMaker(self.applyAction(st, mv, True), mv, i)
            children.append(child)

        #minMax method. player 0 is max and player 1 is min
        if st['turn'] == 1:
            val = min(children).value
            mM  = "Min"
        else:
            val = max(children).value
            mM  = "Max"
        return Tree(val, action , children)
