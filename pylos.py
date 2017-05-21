#!/usr/bin/env python3
# pylos.py
# Author: Quentin Lurkin
# Version: April 28, 2017
# -*- coding: utf-8 -*-

import argparse
import socket
import sys
import json
import random #This package realy shouldn't be in a AI code. Shame on me
from actions import Movement
from lib import game

class PylosState(game.GameState):
    '''Class representing a state for the Pylos game.'''
    def __init__(self, initialstate=None):

        if initialstate == None:
            # define a layer of the board
            def squareMatrix(size):
                matrix = []
                for i in range(size):
                    matrix.append([None]*size)
                return matrix

            board = []
            for i in range(4):
                board.append(squareMatrix(4-i))

            initialstate = {
                'board': board,
                'reserve': [15, 15],
                'turn': 0
            }

        super().__init__(initialstate)
    @property
    def st(self):
        return self._state['visible']

    def get(self, layer, row, column):
        if layer < 0 or row < 0 or column < 0:
            raise game.InvalidMoveException('The position ({}) is outside of the board'.format([layer, row, column]))
        try:
            return self._state['visible']['board'][layer][row][column]
        except:
            raise game.InvalidMoveException('The position ({}) is outside of the board'.format([layer, row, column]))

    def safeGet(self, layer, row, column):
        try:
            return self.get(layer, row, column)
        except game.InvalidMoveException:
            return None

    def validPosition(self, layer, row, column):
        if self.get(layer, row, column) != None:
            raise game.InvalidMoveException('The position ({}) is not free'.format([layer, row, column]))

        if layer > 0:
            if (
                self.get(layer-1, row, column) == None or
                self.get(layer-1, row+1, column) == None or
                self.get(layer-1, row+1, column+1) == None or
                self.get(layer-1, row, column+1) == None
            ):
                raise game.InvalidMoveException('The position ({}) is not stable'.format([layer, row, column]))

    def canMove(self, layer, row, column):
        if self.get(layer, row, column) == None:
            raise game.InvalidMoveException('The position ({}) is empty'.format([layer, row, column]))

        if layer < 3:
            if (
                self.safeGet(layer+1, row, column) != None or
                self.safeGet(layer+1, row-1, column) != None or
                self.safeGet(layer+1, row-1, column-1) != None or
                self.safeGet(layer+1, row, column-1) != None
            ):
                raise game.InvalidMoveException('The position ({}) is not movable'.format([layer, row, column]))

    def createSquare(self, coord):
        layer, row, column = tuple(coord)

        def isSquare(layer, row, column):
            if (
                self.safeGet(layer, row, column) != None and
                self.safeGet(layer, row+1, column) == self.safeGet(layer, row, column) and
                self.safeGet(layer, row+1, column+1) == self.safeGet(layer, row, column) and
                self.safeGet(layer, row, column+1) == self.safeGet(layer, row, column)
            ):
                return True
            return False

        if (
            isSquare(layer, row, column) or
            isSquare(layer, row-1, column) or
            isSquare(layer, row-1, column-1) or
            isSquare(layer, row, column-1)
        ):
            return True
        return False

    def set(self, coord, value):
        layer, row, column = tuple(coord)
        self.validPosition(layer, row, column)
        self._state['visible']['board'][layer][row][column] = value

    def remove(self, coord, player):
        layer, row, column = tuple(coord)
        self.canMove(layer, row, column)
        sphere = self.get(layer, row, column)
        if sphere != player:
            raise game.InvalidMoveException('not your sphere')
        self._state['visible']['board'][layer][row][column] = None

    # update the state with the move
    # raise game.InvalidMoveException
    def update(self, move, player):
        state = self._state['visible']
        if move['move'] == 'place':
            if state['reserve'][player] < 1:
                raise game.InvalidMoveException('no more sphere')
            self.set(move['to'], player)
            state['reserve'][player] -= 1
        elif move['move'] == 'move':
            if move['to'][0] <= move['from'][0]:
                raise game.InvalidMoveException('you can only move to upper layer')
            sphere = self.remove(move['from'], player)
            try:
                self.set(move['to'], player)
            except game.InvalidMoveException as e:
                self.set(move['from'], player)
                raise e
        else:
            raise game.InvalidMoveException('Invalid Move:\n{}'.format(move))

        if 'remove' in move:
            if not self.createSquare(move['to']):
                raise game.InvalidMoveException('You cannot remove spheres')
            if len(move['remove']) > 2:
                raise game.InvalidMoveException('Can\'t remove more than 2 spheres')
            for coord in move['remove']:
                sphere = self.remove(coord, player)
                state['reserve'][player] += 1

        state['turn'] = (state['turn'] + 1) % 2


    # return 0 or 1 if a winner, return None if draw, return -1 if game continue
    def winner(self):
        state = self._state['visible']
        if state['reserve'][0] < 1:
            return 1
        elif state['reserve'][1] < 1:
            return 0
        return -1

    def val2str(self, val):
        return '_' if val == None else '@' if val == 0 else 'O'

    def player2str(self, val):
        return 'Light' if val == 0 else 'Dark'

    def printSquare(self, matrix):
        print(' ' + '_'*(len(matrix)*2-1))
        print('\n'.join(map(lambda row : '|' + '|'.join(map(self.val2str, row)) + '|', matrix)))

    # print the state
    def prettyprint(self):
        state = self._state['visible']
        for layer in range(4):
            self.printSquare(state['board'][layer])
            print()

        for player, reserve in enumerate(state['reserve']):
            print('Reserve of {}:'.format(self.player2str(player)))
            print((self.val2str(player)+' ')*reserve)
            print()

        print('{} to play !'.format(self.player2str(state['turn'])))
        #print(json.dumps(self._state['visible'], indent=4))

class PylosServer(game.GameServer):
    '''Class representing a server for the Pylos game.'''
    def __init__(self, verbose=False):
        super().__init__('Pylos', 2, PylosState(), verbose=verbose)

    def applymove(self, move):
        try:
            self._state.update(json.loads(move), self.currentplayer)
        except json.JSONDecodeError:
            raise game.InvalidMoveException('move must be valid JSON string: {}'.format(move))


class PylosClient(game.GameClient):
    '''Class representing a client for the Pylos game.'''
    def __init__(self, name, server, verbose=False):
        super().__init__(server, PylosState, verbose=verbose)
        self.__name = name

    def _handle(self, message):
        pass

    #return move as string
    def _nextmove(self, state):
        '''
        example of moves
        coordinates are like [layer, row, colums]
        move = {
            'move': 'place',
            'to': [0,1,1]
        }

        move = {
            'move': 'move',
            'from': [0,1,1],
            'to': [1,1,1]
        }

        move = {
            'move': 'move',
            'from': [0,1,1],
            'to': [1,1,1]
            'remove': [
                [1,1,1],
                [1,1,2]
            ]
        }

        return it in JSON
        '''
        st = state.st

        if st['turn'] == 1:
            st['turn'] = 0
        else:
            st['turn'] = 1
        MV = Movement()
        mvs = []
        mvs = MV.allPlace(st)
        mvs += MV.allMoves(st)

        #change depth according to number of child from initial state
        if len(mvs) < 3:
            itr = 6
        elif len(mvs) <= 5:
            itr = 5
        elif len(mvs) <= 6:
            itr = 4
        else:
            itr = 3

        tree = MV.treeMaker(st, i=3)

        bestChoice = [i for i, x in enumerate(tree.childrenVal) if x == tree.value]
        bst = []
        if len(bestChoice) > 1
            for choice in bestChoice:
                nextMove = tree.children[choice].action
                nstate = MV.applyAction(st, nextMove)
                tr = MV.treeMaker(nstate,i=1)
                bst.append((choice, tr.value))
            if st["turn"] == 0:
                bestChoice = [x[0] for i,  x in enumerate(bst) if x[1] == max(bst, key = lambda x: x[1])[1]]
            else:
                bestChoice = [x[0] for i,  x in enumerate(bst) if x[1] == min(bst, key = lambda x: x[1])[1]]
            print("2", bestChoice)
        nextMove = tree.children[random.choice(bestChoice)].action

        return json.dumps(nextMove)


class PylosHuman(game.GameClient):
    '''represent a human player for Pylos Game'''
    def __init__(self, name, server, verbose=False):
        super().__init__(server, PylosState, verbose=verbose)
        self.__name = name

    def _handle(self, message):
        pass

    def _nextmove(self, state):

        valid = False

        while not valid:
            #create parser for human play
            parser = argparse.ArgumentParser(description='Pylos Game')
            parser.add_argument('--place', help='place ball')
            parser.add_argument('--frm', help='move ball from')
            parser.add_argument('--to', help='move ball to')
            parser.add_argument('--rem1', help='remove ball 1')
            parser.add_argument('--rem2', help='remove ball 2')

            s = input('inscriver votre mouvement')

            try:
                args = parser.parse_args(s.split(' '))
            except:
                print("commande non valide")
            else:
                move = {}
                if args.place is not None :
                    place = [int(x) for x in args.place]
                    try:
                        state.validPosition(place[0], place[1], place[2])
                    except Exception as e:
                        print("1",e)
                    else:
                        valid = True
                        move['move'] = 'place'
                        move['to'] = place

                elif args.frm is not None and args.to is not None:
                    frm = [int(x) for x in args.frm]
                    to = [int(x) for x in args.to]
                    try:
                        state.validPosition(to[0], to[1], to[2])
                        state.canMove(frm[0], frm[1], frm[2])
                    except Exception as e:
                        print('2',e)
                    else:
                        valid = True
                        move['move'] = 'move'
                        move['from'] = frm
                        move['to'] = to

                if args.rem1 is not None:
                    rem1 = [int(x) for x in args.rem1]
                    try:
                        state.canMove(rem1[0], rem1[1], rem1[2])
                    except Exception as e:
                        valid = False
                        print('3',e)
                    else:
                        if args.rem2 is not None:
                            rem2 = [int(x) for x in args.rem2]
                            try:
                                state.canMove(rem2[0], rem2[1], rem2[2])
                            except Exception as e:
                                valid = False
                                print('4',e)
                            else:

                                move['remove'] = [rem1, rem2]
                        else:
                                move['remove'] = [rem1]
        return json.dumps(move)

if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Pylos game')
    subparsers = parser.add_subparsers(description='server client', help='Pylos game components', dest='component')
    # Create the parser for the 'server' subcommand
    server_parser = subparsers.add_parser('server', help='launch a server')
    server_parser.add_argument('--host', help='hostname (default: localhost)', default='localhost')
    server_parser.add_argument('--port', help='port to listen on (default: 5000)', default=5000)
    server_parser.add_argument('--verbose', action='store_true')
    # Create the parser for the 'client' subcommand
    client_parser = subparsers.add_parser('client', help='launch a client')
    client_parser.add_argument('name', help='name of the player')
    client_parser.add_argument('--host', help='hostname of the server (default: localhost)', default='localhost')
    client_parser.add_argument('--port', help='port of the server (default: 5000)', default=5000)
    client_parser.add_argument('--verbose', action='store_true')
    # Create the parser for the 'human' subcommand
    client_parser = subparsers.add_parser('human', help='launch a human client')
    client_parser.add_argument('name', help='name of the player')
    client_parser.add_argument('--host', help='hostname of the server (default: localhost)', default='localhost')
    client_parser.add_argument('--port', help='port of the server (default: 5000)', default=5000)
    client_parser.add_argument('--verbose', action='store_true')
    # Parse the arguments of sys.args
    args = parser.parse_args()
    if args.component == 'server':
        PylosServer(verbose=args.verbose).run()
    elif args.component == 'client':
        PylosClient(args.name, (args.host, args.port), verbose=args.verbose)
    elif args.component == 'human':
        PylosHuman(args.name, (args.host, args.port), verbose=args.verbose)
