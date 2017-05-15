import json
import copy
from Three import Tree
state = [[[None, None, None, None],[None, None, None, None],[None,None,None,None],[None,None,None,None]],[[None, None, None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]
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
                                mvs += remove(allRemove(nextState, turn), move)
                            else:
                                mvs.append(move)
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
    mvs = []
    removes = allRemove(st, turn)
    for rmv in removes:
        layer = rmv[0]
        row = rmv[1]
        column = rmv[2]
        stcopy = copy.deepcopy(st)
        stcopy[layer][row][column] = None
        movs = allPlace(stcopy, turn, layer + 1)
        for mv in movs:

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
                mvs += remove(allRemove(nextState, turn), move)
            else:
                mvs.append(move)
    return mvs

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

#moves = allPlace(state, 1)
#allMoves(state, 1)
#printMove(moves)

def treeMaker(parent, turn, i = None):
    mvs =[]
    mvs = allPlace(parent, turn)
    mvs += allMoves(parent, turn)
    if i < 1 and i != None:
        return Tree(mvs)
    i -= 1
    if turn == 1:
        turn = 0
    else:
        turn = 1
    return Tree(mvs, [treeMaker(applyAction(parent, mv, turn),turn, i) for mv in mvs ] )

tree = treeMaker(state, 1, 2)
print(tree)
