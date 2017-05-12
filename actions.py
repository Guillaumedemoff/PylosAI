import json
import copy
state = [[[0,1,0,1],[0,1,0,1],[0,1,None,None],[None,None,None,None]],[[None,1,0],[None,None,1],[None,None,None]],[[None,None],[None,None]],[[None]]]
def allPlace(state, layerRes = None):
    moves = []
    a = layerRes
    b = layerRes + 1
    if layerRes == None:
        a = 0
        b = 4
    for layer in range(a,b):
        #print("layer: ", layer)
        for row in range(4-layer):
            #print('row: ', row)
            for column in range(4-layer):
                #print('col: ', column)
                if state[layer][row][column] == None:

                    if not feelTheMagic(state, layer, row, column):
                        move = json.dumps({
                            'move': 'place',
                            'to': [layer, row, column],
                            'cost': -1
                        })
                        moves.append(move)
    return moves


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
    moves = []
    for layer in range(3):
        for row in range(4-layer):
            for column in range(4-layer):
                if state[layer][row][column] == turn:
                    st = copy.deepcopy(state)
                    st[layer][row][column] = None
                    mvs = allPlace(st, layer + 1)
                    for mv in mvs:
                        mv = json.loads(mv)
                        move = json.dumps({
                            'move': 'move',
                            'from': [layer, row, column],
                            'to': mv['to'],
                            'cost': 0
                        })
                        moves.append(move)
    return moves

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
