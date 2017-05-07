import json
state =[[[0,1,0,1],[0,1,0,1],[0,1,0,1],[0,1,0,1]],[[0,1,0],[1,0,1],[0,1,0]],[[1,None],[None,None]],[[None]]]
def allPlace(state):
    moves = []
    for layer in range(4):
        for row in range(4-layer):
            for column in range(4-layer):
                if state[layer][row][column] == None:
                    move = json.dumps({
                        'move': 'place',
                        'to': [layer, row, column]
                    })
                    moves.append(move)
    print(moves)
allPlace(state)
