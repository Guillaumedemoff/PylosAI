import json
import copy
state = [[[0, None, 0, 0],[None, 0, None, 0],[1,None,1,1],[None,1,None,1]],[[None, None, None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]
action = {'move': 'place', 'to':[0,2,1]}
moves = []

def allPlace(turn, layerRes = None):
    if layerRes == None:
        a = 0
        b = 4
    else:
        a = layerRes
        b = layerRes + 1

    for layer in range(a,b):
        #print("layer: ", layer)
        for row in range(4-layer):
            #print('row: ', row)
            for column in range(4-layer):
                #print('col: ', column)
                if state[layer][row][column] == None:

                    if not feelTheMagic(state, layer, row, column):
                        move = {
                            'move': 'place',
                            'to': [layer, row, column],
                            'cost': -1
                        }
                        nextState = applyAction(move, turn)
                        if (checkSquare(nextState, layer, row, column, turn) or
                            checkSquare(nextState, layer, row, column-1, turn) or
                            checkSquare(nextState, layer, row-1, column-1, turn) or
                            checkSquare(nextState, layer, row -1, column, turn)):
                            remove(state, allRemove(state, turn), move)
                        else:
                            moves.append(move)


def feelTheMagic(state, layer, row, column):

    feelTheMagic = False
    for i in range(2):
        for j in range(2):
            if layer != 0:
                if state[layer-1][row+i][column+j] == None:
                    feelTheMagic = True

    return feelTheMagic


def feelThePressure(state, layer, row, column):
    feelThePressure = False
    for i in range(2):
        for j in range(2):
            if layer < 3 and 0 <= row-i < 3-layer and 0 <= column-j < 3-layer:
                if state[layer+1][row-i][column-j] != None:
                    feelThePressure = True
    return feelThePressure

def allMoves(state, turn):
    for layer in range(3):
        for row in range(4-layer):
            for column in range(4-layer):
                if state[layer][row][column] == turn:
                    st = copy.deepcopy(state)
                    st[layer][row][column] = None
                    mvs = allPlace(st, layer + 1)
                    for mv in mvs:
                        mv = json.loads(mv)
                        move = {
                            'move': 'move',
                            'from': [layer, row, column],
                            'to': mv['to'],
                            'cost': 0
                        }
                        moves.append(move)

def allRemove(state, turn):
    remove = []
    for layer in range(3):
        for row in range(4-layer):
            for column in range(4-layer):
                if (
                    state[layer][row][column] == turn and
                    not feelThePressure(state, layer, row, column)
                ):
                    remove.append([layer, row, column])
    return remove

def checkSquare(state, layer, row, column, turn):
    for i in range(2):
        for j in range(2):
            if state[layer][row+i][column+j] != turn:
                return False
    return True

def remove(state, freeMarble, move):
    for i in range(len(freeMarble)):
        for j in range(i+1,len(freeMarble)):
            move['remove'] = [freeMarble[i],freeMarble[j]]
            moves.append(move)
    for rmv in freeMarble:
        move['remove'] = [rmv]
        moves.append(move)


def applyAction(action, turn):
    nextState = copy.deepcopy(state)
    if action['move'] == 'place':
        to =action['to']
        nextState[to[0]][to[1]][to[2]] = turn
    elif action['move'] == 'move':
        to =action['to']
        from_ = to =action['from']
        nextState[from_[0]][from_[1]][from_[2]] = None
        nextState[to[0]][to[1]][to[2]] = turn
    return nextState

allPlace(1)
#print(moves)
