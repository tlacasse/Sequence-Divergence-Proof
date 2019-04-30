from sympy import sympify
from exprmap import EXPRMAP, TERM_BOUND, exprmap_term, exprmap_join
import exprutils as eu
import numpy as np

def _append_empty_term_parts(term_parts_list):
    while(len(term_parts_list) < TERM_BOUND):
        term_parts_list.append((0, 0, 0))
    return term_parts_list

def _split_sympify(frac):
    return [sympify(expr) for expr in frac.split('/')]

def _get_term_parts(pair):
    return [_append_empty_term_parts(eu.get_all_term_parts(expr)) 
            for expr in pair]
    
def _exprmap_terms(tuple_list_pair):
    return [[exprmap_term(t) for t in tl] for tl in tuple_list_pair]
    
def _flatten(arr):
    result = []
    for i in arr:
        for j in i:
            result.append(j)
    return result

def _stringify(arr):
    return [str(i) for i in arr]

def map_expr_to_data_point(expr):
    """
    '(6*n**2+3*n)/(2*n)'
    => [6*n**2 + 3*n, 2*n]
    => [ [(1, 6, 2), (1, 3, 1), (0, 0, 0)], [(1, 2, 1), (0, 0, 0), (0, 0, 0)] ]
    => [ [28, 14, 0], [13, 0, 0] ]
    => [28, 14, 0, 13, 0, 0]
    """
    expr = str(expr)
    for func in [_split_sympify, _get_term_parts, _exprmap_terms, _flatten]:
        expr = func(expr)
    return expr

def map_exprs_to_array(exprs):
    arr = np.empty((len(exprs), TERM_BOUND * 2), dtype='float64')
    for i, expr in enumerate(exprs):
        for j, t in enumerate(map_expr_to_data_point(expr)):
            arr[i][j] = t / EXPRMAP.TERM_VALUE 
    return arr

vround = np.vectorize(round)

def map_array_to_real(arr):
    arr *= EXPRMAP.TERM_VALUE
    arr[:] = vround(arr[:])
    arr = arr.astype(dtype='int32')
    top = arr[:TERM_BOUND]
    bot = arr[TERM_BOUND:]
    return exprmap_join(top), exprmap_join(bot)
