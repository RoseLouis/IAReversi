# -*- coding: utf-8 -*-

import time
import src.Reversi as Reversi
import math
import time
from random import randint

from src.playerInterface import *


class myPlayer(PlayerInterface):
    _depthMax = 3
    currentDepth = 0
    runDepth = 0
    lastTime = 0
    timeperturn = 5
    # at maximum we can play 50 plays so in 5 minutes a play can take maximum 6 second

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Someone"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)
        moves = [m for m in self._board.legal_moves()]
        move = moves[randint(0, len(moves) - 1)]
        runBestmove = move
        self.runDepth = 1
        while self.runDepth <= self._depthMax:
            meilleur = -math.inf
            self.lastTime = time.time()
            for m in self._board.legal_moves():
                self._board.push(m)
                valeur = self._MinMax()
                if valeur > meilleur:
                    meilleur = valeur
                    runBestmove = m
                self._board.pop()
                if time.time() - self.lastTime >= self.timeperturn:
                    self.runDepth=(self._depthMax+1)
                    move = runBestmove
                    break
            move = runBestmove
            self.runDepth+=1
        #move = moves[randint(0,len(moves)-1)]
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y)

    def playOpponentMove(self, x, y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def _MaxMin(self):
        self.currentDepth += 1
        if not(self._board.at_least_one_legal_move((self._mycolor%2)+1)) or self.currentDepth >= self.runDepth:
            self.currentDepth -= 1
            return self._board.heuristiqueCoin((self._mycolor%2)+1)
        meilleur = -math.inf
        for m in self._board.legal_moves():
            self._board.push(m)
            meilleur = max(meilleur, self._MinMax())
            self._board.pop()
        self.currentDepth -= 1
        return meilleur

    def _MinMax(self):
        self.currentDepth += 1
        if not self._board.at_least_one_legal_move(self._mycolor) or self.currentDepth >= self.runDepth:
            self.currentDepth -= 1
            return self._board.heuristiqueCoin(self._mycolor)
        pire = math.inf
        for m in self._board.legal_moves():
            self._board.push(m)
            pire = min(pire, self._MaxMin())
            self._board.pop()
        self.currentDepth -= 1
        return pire

    def _MaxValue(self, alpha, beta):
        self.currentDepth += 1
        if not self._board.at_least_one_legal_move((self._mycolor%2)+1) or self.currentDepth >= self.runDepth:
            self.currentDepth -= 1
            return self._board.heuristiqueCoin((self._mycolor%2)+1)
        for m in self._board.legal_moves():
            self._board.push(m)
            alpha = max(alpha, self._MinValue(alpha, beta))
            self._board.pop()
            if alpha >= beta:
                self.currentDepth -= 1
                return beta
        self.currentDepth -= 1
        return alpha

    def _MinValue(self, alpha, beta):
        self.currentDepth += 1
        if not self._board.at_least_one_legal_move(self._mycolor) or self.currentDepth > self.runDepth:
            self.currentDepth -= 1
            return self._board.heuristiqueCoin(self._mycolor)
        for m in self._board.legal_moves():
            self._board.push(m)
            beta = min(beta, self._MaxValue(alpha, beta))
            self._board.pop()
            if alpha >= beta:
                self.currentDepth -= 1
                return alpha
        self.currentDepth -= 1
        return beta
