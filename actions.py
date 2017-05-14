import json
import copy
from Three import Tree
state = [[[0, 0, 0, 0],[None, 0, 0, 0],[1,0,1,1],[None,1,1,1]],[[None, 1, 1],[None,None,1],[None,None,None]],[[None,None],[None,None]],[[None]]]
action = {'move': 'place', 'to':[0,2,1]}
moves = []

def allPlace(st, turn, layerRes = None):
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
                if st[layer][row][column] == None:
                    if not feelTheMagic(st, layer, row, column):
                        move = {
                            'move': 'place',
                            'to': [layer, row, column],
                            'cost': -1
                        }

                        if layerRes == None:
                            nextState = applyAction(st, move, turn)
                            if (checkSquare(nextState, layer, row, column, turn) or
                                checkSquare(nextState, layer, row, column-1, turn) or
                                checkSquare(nextState, layer, row-1, column-1, turn) or
                                checkSquare(nextState, layer, row -1, column, turn)):
                                remove(allRemove(nextState, turn), move)
                            else:
                                moves.append(move)
                                pass
                        else:
                            mvs.append(move)
    return mvs

def feelTheMagic(st, layer, row, column):

    feelTheMagic = False
    for i in range(2):
        for j in range(2):
            if layer != 0:
                if st[layer-1][row+i][column+j] == None:
                    feelTheMagic = True

    return feelTheMagic


def feelThePressure(st, layer, row, column):
    feelThePressure = False
    for i in range(2):
        for j in range(2):
            if layer < 3 and 0 <= row-i < 3-layer and 0 <= column-j < 3-layer:
                if st[layer+1][row-i][column-j] != None:
                    feelThePressure = True

    return feelThePressure

def allMoves(st, turn):
    removes = allRemove(st, turn)
    for rmv in removes:
        layer = rmv[0]
        row = rmv[1]
        column = rmv[2]
        stcopy = copy.deepcopy(st)
        stcopy[layer][row][column] = None
        mvs = allPlace(stcopy, turn, layer + 1)
        for mv in mvs:
            move = {
                'move': 'move',
                'from': [layer, row, column],
                'to': mv['to'],
                'cost': 0
            }
            nextState = applyAction(st, move, turn)
            layer = mv['to'][0]
            row =  mv['to'][1]
            column =  mv['to'][2]
            if (checkSquare(nextState, layer, row, column, turn) or
                checkSquare(nextState, layer, row, column-1, turn) or
                checkSquare(nextState, layer, row-1, column-1, turn) or
                checkSquare(nextState, layer, row -1, column, turn)):
                remove(allRemove(nextState, turn), move)
            else:
                moves.append(move)

def allRemove(st, turn):
    remove = []
    for layer in range(3):
        for row in range(4-layer):
            for column in range(4-layer):
                if (
                    st[layer][row][column] == turn and
                    not feelThePressure(st, layer, row, column)
                ):
                    remove.append([layer, row, column])
    return remove

def checkSquare(st, layer, row, column, turn):
    for i in range(2):
        for j in range(2):
            if layer < 3 and 0 <= row+i <= 3-layer and 0 <= column+j <= 3-layer:
                if st[layer][row+i][column+j] != turn:
                    return False
            else:
                return False
    return True

def remove(freeMarble, move):
    for i in range(len(freeMarble)):
        for j in range(i+1,len(freeMarble)):
            move['remove'] = [freeMarble[i],freeMarble[j]]
            mv = copy.deepcopy(move)
            moves.append(mv)
    for rmv in freeMarble:
        move['remove'] = [rmv]
        mv = copy.deepcopy(move)
        moves.append(mv)


def applyAction(st, action, turn):
    nextState = copy.deepcopy(st)
    if action['move'] == 'place':
        to =action['to']
        nextState[to[0]][to[1]][to[2]] = turn
    elif action['move'] == 'move':
        to = action['to']
        from_ =action['from']
        nextState[from_[0]][from_[1]][from_[2]] = None
        nextState[to[0]][to[1]][to[2]] = turn

    return nextState

def printMove(mv):
    output = ''
    for elem in mv:
        if elem['move'] == 'place':
            output = '+ ' + str(elem['to'])
        elif elem['move'] == 'move':
            output = str(elem['from']) + '-->' + str(elem['to'])
        if 'remove' in elem:
            output += ' - ' + str(elem['remove'])
        print(output)
        
allPlace(state, 1)
allMoves(state, 1)
printMove(moves)

def treeMaker(parent):
    return Tree(parent, 3)
