import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.
DEPTH = 5
WIN_SCORE = 1000

CORNERS = ((0,0), (7,7),(7,0),(0,7))

NEAR = {
    (0,0): ((1,0),(0,1),(1,1)),
    (7,0): ((6,0),(7,1),(6,1)),
    (0,7): ((0,6),(1,7),(1,6)),
    (7,7): ((7,6),(6,7),(6,6)),
    }
BASE = [
    [0,0,6,2,2,6,0,0],
    [0,0,1,1,1,1,0,0],
    [6,1,1,1,1,1,1,6],
    [2,1,1,3,3,1,1,2],
    [2,1,1,3,3,1,1,2],
    [6,1,1,1,1,1,1,6],
    [0,0,1,1,1,1,0,0],
    [0,0,6,2,2,6,0,0],    
]

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    return minimax_move(state,DEPTH,evaluate_custom)


def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    
    board = state.board
    opponent = 'W' if player == 'B' else 'B'

    player_pieces = board.piece_count[player]
    opponent_pieces = board.piece_count[opponent]

    dif = player_pieces - opponent_pieces

    if state.is_terminal():
        if dif > 0:
            return WIN_SCORE + dif
        if dif < 0:
            return -WIN_SCORE + dif

        return 0 

    tiles = board.tiles

    empty = board.piece_count['.']

    pos = 0
    for corner in CORNERS:
        character = tiles[corner[0]][corner[1]]
        if character == player:
            pos+=100
        elif character == opponent:
            pos-=100

        else:
            for (r,k) in NEAR[corner]:
                t = tiles[r][k]
                w = -50 if (abs(r - corner[0]) == 1 and abs(k - corner[1])== 1) else -25

                if t == player:
                    pos += w
                elif t== opponent:
                    pos-= w

        if character != '.':
            for (r,k) in NEAR[corner]:
                t = tiles[r][k]
                if t == character:
                    pos += 5 if character == player else -5

    for x in range(8):
        row = tiles[x]
        base = BASE[x]

        for y in range(8):
            character = row[y]
            if character == player:
                pos += base[y]
            elif character == opponent:
                pos -=  base[y]

    player_movs = len(board.legal_moves(player))
    opp_movs = len(board.legal_moves(opponent))
    mobility = 100 * (player_movs - opp_movs) / (player_movs + opp_movs) if (player_movs + opp_movs) else 0

    if empty > 40:
        diff_weight = -0.5
    elif empty > 16:
        diff_weight = 0.5
    else:
        diff_weight = 4

    mobility_weight = 1.5 if empty > 16 else 0.7

    return pos + mobility_weight * mobility + diff_weight * dif

