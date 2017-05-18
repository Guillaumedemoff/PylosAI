import json
import copy
from Three import Tree
board = [[[None, None, None, None],[None, None, None, None],[None,None,None,None],[None,None,None,None]],[[None, None, None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]
#board = [[[1, 1, None, None],[1, None, None, None],[None,None,None,None],[None,None,None,None]],[[None, None, None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]
state = {'reserve' : [15, 15], 'turn': 1, 'board' : board}
action = {'move': 'place', 'to':[0,2,1]}
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
                                'to': [layer, row, column],
                                'cost': -1
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
                    'to': mv['to'],
                    'cost': 0
                }
                nextState = self.applyAction(st, move)
                layer = mv['to'][0]
                row =  mv['to'][1]
                column =  mv['to'][2]
                if (self.checkSquare(nextState, layer, row, column) or
                    self.checkSquare(nextState, layer, row, column-1) or
                    self.checkSquare(nextState, layer, row-1, column-1) or
                    self.checkSquare(nextState, layer, row -1, column)):
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
                move['cost'] = 2
                mv = copy.deepcopy(move)
                mvs.append(mv)
        for rmv in freeMarble:
            move['remove'] = [rmv]
            move['cost'] = 1
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

        if cost:
            nextState['reserve'][nextState['turn']] += action['cost']
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
            output += '$' + str(elem['cost'])
            print(output)

    def treeMaker(self, st, i = None):
        mvs =[]
        mvs = self.allPlace(st)
        mvs += self.allMoves(st)

        if ((i < 1 and i != None) or
            st['reserve'][0] == 0 or
            st['reserve'][1] == 0):
            return Tree(mvs)
        i -= 1
        if st['turn'] == 1:
            st['turn'] = 0
        else:
            st['turn'] = 1
        return Tree(mvs, [self.treeMaker(self.applyAction(st, mv, True), i) for mv in mvs ] )

MV = Movement()
tree = MV.treeMaker(state, 4)
print(tree)
