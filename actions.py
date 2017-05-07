import json
state = [[[0,1,0,1],[0,1,0,1],[0,1,0,1],[0,1,0,1]],[[0,1,0],[1,0,1],[0,1,0]],[[1,None],[None,None]],[[None]]]
state = [[[0,1,0,1],[0,1,0,1],[0,1,None,None],[None,None,None,None]],[[None,None,None],[None,None,None],[None,None,None]],[[None,None],[None,None]],[[None]]]
def allPlace(state):
    moves = []
    for layer in range(4):
        for row in range(4-layer):
            for column in range(4-layer):
                if state[layer][row][column] == None:
                    feelTheMagic = False
                    for i in range(2):
                        for j in range(2):
                            if layer != 0:
                                if state[layer-1][row+i][column+j] == None and layer != 0:
                                    feelTheMagic = True
                    move = json.dumps({
                        'move': 'place',
                        'to': [layer, row, column]
                    })
                    if not feelTheMagic:
                        moves.append(move)
    print(moves)
allPlace(state)
