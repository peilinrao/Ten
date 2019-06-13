# -*- coding: utf-8 -*-

import numpy as np
import Pentomino
import instances

def equal(a, b):
    if len(a) != len(b):
        return False
    elif len(a[0]) != len(b[0]):
        return False
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j] != b[i][j]:
                return False
    return True

def inside(board, pet):
    r0 = -1
    r1 = -1
    ret = list()
    for i in range(len(board) - len(pet) + 1):
        for j in range(len(board[0]) - len(pet[0]) + 1):
            count = 0
            for a in range(len(pet)):
                for b in range(len(pet[0])):
                    if board[i + a][j + b] == 0 and pet[a][b] != 0:
                        count = 1
                        break
            if count == 0:
                ret.append((i, j))

    return ret

def board_mis(board, bsol):
    bd = np.zeros((len(board), len(board[0])), int)
    for i in range(len(bsol)):
        for j in range(len(board[0])):
            if bsol[i][j] > 0:
                bd[i][j] = 0;
            else:
                bd[i][j] = board[i][j]
    return bd

def solution(board, petnominos, record_board):
#    return [(p1, (row1, col1))...(pn,  (rown, coln))]
    pents = list()
    pents.append(petnominos)
    pos = list()
    pos.append(petnominos.T)
    pos.append(petnominos[::-1])
    pos.append(petnominos.T[::-1])
    pos.append(np.flip(petnominos))
    pos.append(np.flip(petnominos)[::-1])
    pos.append(np.flip(petnominos.T))
    pos.append(np.flip(petnominos.T)[::-1])
    for elem in pos:
        count = 0
        for i in range(len(pents)):
            if equal(pents[i], elem):
                count = 1
        if count == 0:
            pents.append(elem)

#    if equal(petnominos, petnominos[::-1]) == True and equal(petnominos, np.flip(petnominos)[::-1]) == True:
#        if len(petnominos) != len(petnominos[0]):
#            pents.append(petnominos.T)
#    elif equal(petnominos, petnominos[::-1]) == True:
#        #up and down are the same
#        pents.append(petnominos.T)
#        pents.append(petnominos.T[::-1])
#        pents.append(np.flip(petnominos))
#    elif equal(petnominos, np.flip(petnominos)[::-1]) == True:
#        pents.append(petnominos.T)
#        pents.append(petnominos[::-1])
#        pents.append(np.flip(petnominos.T))
#    else:
#        pents.append(petnominos.T)
#        pents.append(petnominos[::-1])
#        pents.append(petnominos.T[::-1])
#        pents.append(np.flip(petnominos))
#        pents.append(np.flip(petnominos)[::-1])
#        pents.append(np.flip(petnominos.T))
#        pents.append(np.flip(petnominos.T)[::-1])

    sol = list()
    for elem in pents:
        temp = inside(board, elem)
        if (len(temp) == 0):
            continue
        for el in temp:
            sol.append((elem, el))
            for i in range(len(elem)):
                for j in range(len(elem[0])):
                    record_board[el[0] + i][el[1] + j] = 0

    return sol

def find_the_spots(pents, sol_board):
    ctlist = list()
    for elem in pents:
#        print("elem: ", elem)
        pet = elem[0]
        spot = elem[1]
        count = 0
        record = np.zeros((len(sol_board), len(sol_board[0])), int)
#        print(elem, pents)
        Pentomino.add_pentomino(sol_board, pet, spot, check_pent=False, valid_pents=None)
#        print(sol_board)
        for i in range(len(pet)):
            for j in range(len(pet[0])):
                if pet[i][j] == 0:
                    continue
                o = spot[0] + i
                t = spot[1] + j
                so = max(0, o - 1)
                lo = min(len(sol_board) - 1, o + 1)
                st = max(0, t - 1)
                lt = min(len(sol_board[0]) - 1, t + 1)
                for a in range(so, lo + 1):
                    for b in range(st, lt + 1):
                        o_in_pent = a - spot[0]
                        t_in_pent = b - spot[1]
                        if o_in_pent >= 0 and o_in_pent < len(pet) and t_in_pent >= 0 and t_in_pent < len(pet[0]) and pet[o_in_pent][t_in_pent] > 0:
#                            print("not counted", "i: ", i, ", j: ", j, ", a: ", a, ", b:", b)
                            continue
                        if sol_board[a][b] > 0 and record[a][b] == 0:
#                            print("i: ", i, ", j: ", j, ", a: ", a, ", b:", b)
                            record[a][b] = 1
                            count = count + 1
                        if sol_board[a][b] == 0 and record[a][b] == 0:
#                            print("i: ", i, ", j: ", j, ", a: ", a, ", b:", b)
                            record[a][b] = 1
#                            if (a == 0 or a == len(sol_board) - 1) and (b == 0 or b == len(sol_board[0]) - 1):
#                                count = count - 3
#                            elif a == 0 or a == len(sol_board) - 1:
#                                count = count - 2
#                            elif b == 0 or b == len(sol_board[0]) - 1:
#                                count = count - 2
#                            else:
                            count = count - 1
        Pentomino.remove_pentomino(sol_board, Pentomino.get_pent_idx(pet))
        ctlist.append(count)

    retlist = list()
    for i in range(len(ctlist)):
        largest = -10000000
        pos = 0
        for j in range(len(ctlist)):
            if ctlist[j] > largest:
                largest = ctlist[j]
                pos = j
        ctlist[pos] = -10000000
        retlist.append(pents[pos])
    return retlist

def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is
    the coordinate of the upper left corner of pi in the board (lowest row and column index
    that the tile covers).

    -Use np.flip and np.rot90 to manipulate pentominos.

    -You can assume there will always be a solution.
    """
    solution = list()
    real_board = np.ones((len(board), len(board[0])), int)
    for i in range(len(real_board)):
        for j in range(len(real_board[0])):
            real_board[i][j] = board[i][j]
    return main_recur(solution, len(pents), pents, real_board, np.zeros((len(board), len(board[0])), int))

def main_recur(sol, length, restpents, board, sol_board):
    if len(sol) == length:
        return sol

    pentgroup = 0
    pentnum = 1000
    position = 0
    count = 0
    record_board = board.copy()
    for i in range(len(restpents)):
        temp = solution(board, restpents[i], record_board)
        if len(temp) < pentnum:
            pentnum = len(temp)
            pentgroup = temp
            position = count
        count = count + 1

    if equal(record_board, np.zeros((len(record_board), len(record_board[0])), int)) == False:
        return sol

    if pentgroup == []:
        return sol

    pentgroup = find_the_spots(pentgroup, sol_board)

    for value in pentgroup:
#        print("solution board: ", sol_board)
        temp = Pentomino.add_pentomino(sol_board, value[0], value[1], check_pent=False, valid_pents=None)
        sol.append(value)
        boardtmp = board_mis(board, sol_board)
        rpcopy = restpents.copy()
        pt = rpcopy.pop(position)
        re = main_recur(sol, length, rpcopy, boardtmp, sol_board)
        if len(re) == length:
            return re

        tep = Pentomino.remove_pentomino(sol_board, Pentomino.get_pent_idx(pt))
        sol.pop(-1)

    return sol
