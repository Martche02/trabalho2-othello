import random
from typing import Tuple
from ..tttm.gamestate import GameState
from ..tttm.board import Board
from .minimax import minimax_move

def make_move(state: GameState) -> Tuple[int, int]:
    return minimax_move(state, -1, utility)

def utility(state: GameState, player: str) -> float:
    w = state.winner()
    if w == player:
        return 1.0
    elif w is not None:
        return -1.0
    return 0.0
