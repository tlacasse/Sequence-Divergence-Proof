from sympy import Mul, Pow, Integer, sympify
from sympy.abc import n

from proof import Proof
from problems import SeqFraction

import exprutils

FACTOR_OUT_OPTIONS = [sympify(e) for e in ['n', 'n**2', 'n**3']]

class Prover:
    
    def __init__(self, problem):
        self.steps = [[problem]]
    
    def proof_search(self):
        # DFS
        unique = set()
        result = None
        while(len(self.steps) > 0):
            so_far = self.steps.pop()
            on = so_far[-1]
            if (on not in unique):
                unique.add(on)
                if (on.is_valid()):
                    if (on.is_done()):
                        result = so_far
                        break
                    for i, t in enumerate(on.top_split()):
                        for d in self.descendant_nodes(t):
                            new_top = exprutils.replace_term(on.top, i, d)
                            self.__add_to_frontier(so_far, on, new_top, on.bot)
                    for i, t in enumerate(on.bot_split()):
                        for a in self.ascendant_nodes(t):
                            new_bot = exprutils.replace_term(on.bot, i, a)
                            self.__add_to_frontier(so_far, on, on.top, new_bot)
                        new_bot = exprutils.replace_term(on.bot, i, Integer(0))
                        self.__add_to_frontier(so_far, on, on.top, new_bot)
                        for j, z in enumerate(on.bot_split()):
                            if (i != j):
                                for a in self.ascendant_nodes(t):
                                    new_bot = exprutils.replace_term(on.bot, i, a)
                                    new_bot = exprutils.replace_term(new_bot, j, Integer(0))
                                    self.__add_to_frontier(so_far, on, on.top, new_bot)
                    for foo in FACTOR_OUT_OPTIONS:
                        factor_out_top = on.factor_out_top(foo)
                        factor_out_bot = on.factor_out_bot(foo)
                        if (factor_out_top != None and factor_out_bot != None):
                            self.__add_to_frontier(so_far, on, 
                                                   factor_out_top, factor_out_bot)
        return None if result == None else Proof(result)
    
    def __add_to_frontier(self, so_far, on, top, bot):
        next_frac = SeqFraction(top, bot)
        if (True or on.is_valid_order(next_frac) > 1):
            new_path = self.copy_and_append(so_far, next_frac)
            self.steps.append(new_path)
    
    def copy_and_append(self, l, e):
        new_l = [i for i in l]
        new_l.append(e)
        return new_l
    
    def descendant_nodes(self, expr):
        if (expr.func == Integer):
            if (int(expr) > 0):
                return [Integer(0)]
            else:
                return []
        if (expr.func == Mul and expr.args[1].func == Pow):
            coeff = int(expr.args[0])
            expon = int(expr.args[1].args[1])
            results = [Integer(0), Integer(coeff)]
            for c in range(1, min(10, abs(coeff)) + 1):
                for e in range(1, expon + 1):
                    if not (c == coeff and e == expon):
                        results.append(Mul(c, Pow(n, e)))
            return results
        if (expr.func == Mul):
            coeff = int(expr.args[0])
            results = [Integer(0), Integer(coeff)]
            for c in range(1, min(10, abs(coeff))):
                results.append(Mul(c, n))
            return results
        if (expr.func == Pow):
            expon = int(expr.args[1])
            results = [Integer(0)]
            for e in range(1, expon - 1):
                results.append(Pow(n, e))
            return results
        return []
    
    def ascendant_nodes(self, expr):
        if (expr.func == Integer):
            return []
        
        if (expr.func == Mul):
            coeff = int(expr.args[0])
        else:
            coeff = 1
        
        if (len(expr.args) > 1 and expr.args[1].func == Pow):
            expon = int(expr.args[1].args[1])
        else:
            expon = 1
            
        results = []
        for c in range(coeff + 1, coeff + 2):
            for e in range(expon + 1, 6):
                results.append(Mul(c, Pow(n, e)))
        return results
