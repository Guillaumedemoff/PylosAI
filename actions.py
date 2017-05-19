import json
import copy
from Three import Tree
#This package realy shouldn't be in a AI code. Shame on me
import random

board = [[[1, 0, 1, 0], [None, 1, None, 1], [1, 1, 0, None], [0, None, 0, 0]], [[None, None, None], [None, None, None], [None, None, None]],[[None, None], [None, None]], [[None]]]
#board = [[[None, None, None, None],[None, None, None, None],[None,None,None,None],[None,None,None,None]],[[None, None, None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]

state = {'reserve' : [9, 9], 'turn': 1, 'board' : board}


#action = {'move': 'place', 'to':[0,2,1]}
moves = []

class Movement():

    def allPlace(self, st, layerRes = None):
        mvs = []
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

        feelTheMagic = False
        for i in range(2):
            for j in range(2):
                if layer != 0:
                    if st[layer-1][row+i][column+j] == None:
                        feelTheMagic = True

        return feelTheMagic


    def feelThePressure(self, st, layer, row, column):
        feelThePressure = False
        for i in range(2):
            for j in range(2):
                if layer < 3 and 0 <= row-i < 3-layer and 0 <= column-j < 3-layer:
                    if st[layer+1][row-i][column-j] != None:
                        feelThePressure = True

        return feelThePressure

    def allMoves(self, st):
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
                if (self.checkSquare(nextState, l, r, c) or
                    self.checkSquare(nextState, l, r, c-1) or
                    self.checkSquare(nextState, l, r-1, c-1) or
                    self.checkSquare(nextState, l, r -1, c)):
                    mvs += self.remove(self.allRemove(nextState), move)
                else:
                    mvs.append(move)
        return mvs

    def allRemove(self, st):
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
        for i in range(2):
            for j in range(2):
                if layer < 3 and 0 <= row+i <= 3-layer and 0 <= column+j <= 3-layer:
                    if st['board'][layer][row+i][column+j] != st['turn']:
                        return False
                else:
                    return False
        return True

    def remove(self, freeMarble, move):
        mvs = []
        for i in range(len(freeMarble)):
            for j in range(i+1,len(freeMarble)):
                move['remove'] = [freeMarble[i],freeMarble[j]]
                mv = copy.deepcopy(move)
                mvs.append(mv)
        for rmv in freeMarble:
            move['remove'] = [rmv]
            mv = copy.deepcopy(move)
            mvs.append(mv)
        return mvs

    def applyAction(self, st, action, cost = False):
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
        output = ''
        for elem in mv:
            if elem['move'] == 'place':
                output = '+ ' + str(elem['to'])
            elif elem['move'] == 'move':
                output = str(elem['from']) + '-->' + str(elem['to'])
            if 'remove' in elem:
                output += ' - ' + str(elem['remove'])
            print(output)

    def treeMaker(self, st, action = None, i = None, nbrParents = 1):
        delta  = 0
        children = []
        mvs =[]
        if st['turn'] == 1:
            st['turn'] = 0
        else:
            st['turn'] = 1

        mvs = self.allPlace(st)
        mvs += self.allMoves(st)

        if ((i < 1 and i != None) or
            st['reserve'][0] == 0 or
            st['reserve'][1] == 0):
            delta = st['reserve'][0]-st['reserve'][1]
            return Tree(delta, action)


        i -= nbrParents*len(mvs)
        nbrParents = len(mvs)


        for mv in mvs:
            child = self.treeMaker(self.applyAction(st, mv, True), mv, i, nbrParents)
            children.append(child)
        if st['turn'] == 1:
            val = min(children).value
            mM  = "Min"
        else:
            val = max(children).value
            mM  = "Max"
        return Tree(val, action , children)

MV = Movement()

while True:

    tree = MV.treeMaker(state, i=600)
    bestChoice = [i for i, x in enumerate(tree.childrenVal) if x == tree.value]
    nextMove = tree.children[random.choice(bestChoice)].action
    state = MV.applyAction(state, nextMove, True)
    MV.printMove([nextMove])
    print(state)
    if state['turn'] == 1:
        state['turn'] = 0
    else:
        state['turn'] = 1

    move = input("movement?")
    move = json.loads(move)
    state = MV.applyAction(state, move, True)
    print(state)
