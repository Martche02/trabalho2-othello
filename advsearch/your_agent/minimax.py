import random, time
from typing import Tuple, Callable, Optional

class SearchTimeOut(Exception):
    "Erro por ultrapassar tempo"

class context:

    __slots__ = ("player","evaluate_func","deadline","order_key","nodes","cut")

    def __init__(self,player,evaluate_func,deadline,order_key):
        self.player = player

        self.evaluate_func = evaluate_func #funcao de avaliacao
        self.deadline = deadline #Tempo limitador, util para o competitivo
        self.order_key = order_key #ordenacao de jogadas, util para o competitivo
        self.nodes = 0
        self.cut = False


def successors(state,context):
    #Une o que já está implementada no gamestate com o contexto apenas para facilitar na funcao poda alfa-beta 
    succ = [(move,state.next_state(move)) for move in state.legal_moves()]
    if context.order_key is not None and len(succ) > 1:
        succ.sort(key = lambda movs: context.order_key(movs[0]), reverse= True)
    return succ


def alfabeta(state, depth, alpha, beta, context):

    context.nodes += 1
    if context.deadline is not None and (context.nodes & 31) == 0 and time.perf_counter() > context.deadline:
        raise SearchTimeOut()

    if state.is_terminal():
        return context.evaluate_func(state,context.player)

    if depth == 0:
        context.cut = True
        return context.evaluate_func(state,context.player)
        

    succ = successors(state,context)
    if not succ:
        return context.evaluate_func(state,context.player)

    if state.player == context.player:
        value = -float('inf')

        for move, nxt_stp in succ:
            value = max(value, alfabeta(nxt_stp,depth - 1,alpha,beta,context))
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value

    else:
        value = float('inf')
        for move,nxt_stp in succ:
            value = min(value,  alfabeta(nxt_stp,depth -1,alpha,beta,context))
            if value <= alpha:
                break
            beta = min(beta,value)
        return value        

def root_search(state,depth,context,first_move = None):
    succ = successors(state,context)
    if first_move is not None:
        succ.sort(key= lambda ms: ms[0] != first_move)

    best_move,best_val = None, -float('inf')
    alfa,beta= -float('inf'), float('inf')

    for move,nxt_stp in succ:
        val = alfabeta(nxt_stp,depth -1, alfa,beta,context)
        if best_move is None or val > best_val:
            best_move,best_val = move,val
            alfa = max(alfa,best_val)

    return best_move,best_val

def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate_func a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    ctx = context(state.player,eval_func,None,None)
    move, val = root_search(state,max_depth,ctx)

    return move

def iterative_deepening_move(state,eval_func,time_limit,order_key = None,max_depth = 64):
    
    deadline = time.perf_counter() + time_limit
    ctx= context(state.player,eval_func,deadline,order_key)
    succ = successors(state,ctx)
    if not succ:
        return None

    best_move = succ[0][0]
    if len(succ) == 1:
        return best_move

    for depth in range(1,max_depth + 1):
        ctx.cut = False
        try:
            best_move,val = root_search(state,depth,ctx,first_move = best_move)

        except SearchTimeOut:
            break
        if not ctx.cut:
            break

    return best_move 
