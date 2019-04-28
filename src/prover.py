from sympy import Add, Mul, Pow, Integer, sympify
from sympy.abc import n

from proof import Proof
from problems import SeqFraction

import exprutils

FACTOR_OUT_OPTIONS = [sympify(e) for e in ['n', 'n**2', 'n**3']]

# TODO: consider negative coefficients
class Prover:
    
    def __init__(self, problem):
        self.steps = [[problem]]
        self.current = None
        self.path = None
        self.COEFFICIENT_BOUND = 10
        self.EXPONENT_BOUND = 5
    
    def proof_search(self):
        # DFS
        self.unique = {self.steps[0][0]}
        result = None
        while(len(self.steps) > 0):
            path = self.steps.pop()
            current = path[-1]
            if (current.is_valid()):
                if (current.is_done()):
                    result = path
                    break
                self.current = current
                self.path = path
                self._find_frontier_nodes()
        self.unique = None
        return None if result == None else Proof(result)
    
    def _find_frontier_nodes(self):
        new_nodes = []
        for i, t in enumerate(self.current.top_split()):
            new_nodes.extend(self._get_top_replaced_with_descendants(i, t))
            
        bot_term_matrix = self._build_term_matrix(self.current.bot_split())
        for i in self._get_expr_combinations(bot_term_matrix):
            new_nodes.append(SeqFraction(self.current.top, i))
            
        for i, t in enumerate(self.current.bot_split()):
            new_nodes.extend(self._get_bot_replaced_with_ascendants(i, t))
           
        for node in new_nodes:
            #print(node)
            self._add_to_frontier(node)  
            
        for foo in FACTOR_OUT_OPTIONS:
            factor_out_top = self.current.factor_out_top(foo)
            factor_out_bot = self.current.factor_out_bot(foo)
            if (factor_out_top != None and factor_out_bot != None):
                new = SeqFraction(factor_out_top, factor_out_bot)
                self._add_to_frontier(new, skip_order_check = True)
                
    def _build_term_matrix(self, terms):
        result = []
        for t in terms:
            term_opts = []
            term_opts.extend(self.descendant_nodes(t))
            term_opts.extend(self.ascendant_nodes(t))
            result.append(term_opts)
        return result
    
    def _get_expr_combinations(self, term_matrix):
        if (len(term_matrix) == 1):
            return term_matrix[0]
        prev = self._get_expr_combinations(term_matrix[:-1])
        result = []
        for i in prev:
            for j in term_matrix[-1]:
                result.append(Add(i, j))
        return result
                
    def _get_top_replaced_with_descendants(self, term_index, term):
        for d in self.descendant_nodes(term):
            new_top = exprutils.replace_term(self.current.top, term_index, d)
            yield SeqFraction(new_top, self.current.bot)
            
    def _get_bot_replaced_with_ascendants(self, term_index, term):
        for a in self.ascendant_nodes(term):
            new_bot = exprutils.replace_term(self.current.bot, term_index, a)
            yield SeqFraction(self.current.top, new_bot)

    def _add_to_frontier(self, new, skip_order_check = False):
        if (new not in self.unique):
            self.unique.add(new)
            if (skip_order_check or self.current.is_valid_order(new)):
                new_path = self._copy_and_append(self.path, new)
                self.steps.append(new_path)

    def _copy_and_append(self, l, e):
        new_l = [i for i in l]
        new_l.append(e)
        return new_l
    
    def descendant_nodes(self, expr, sign_override=1):
        sign, coeff, expon = exprutils.get_term_parts(expr)
        if (sign == -1):
            return self.ascendant_nodes(
                    exprutils.build_term(coeff, expon), sign_override=-1)
        if (expon == 0):
            # constant
            return [Integer(0)] if coeff > 0 else []
        
        crange = range(1, min(coeff + 1, self.COEFFICIENT_BOUND))
        erange = range(0, min(expon + 1, self.EXPONENT_BOUND))
        results = [Integer(0)]
        results.extend(self._build_terms(sign*sign_override, 
                                         crange, erange, coeff, expon))
        return results
    
    def ascendant_nodes(self, expr, sign_override=1):
        sign, coeff, expon = exprutils.get_term_parts(expr)
        if (sign == -1):
            return self.descendant_nodes(
                    exprutils.build_term(coeff, expon), sign_override=-1)
        
        crange = range(coeff, self.COEFFICIENT_BOUND + 1)
        erange = range(expon, self.EXPONENT_BOUND + 1)
        return set(self._build_terms(sign*sign_override, 
                                     crange, erange, coeff, expon)) # why is set
    
    def _build_terms(self, sign, coeff_opts, expon_opts, coeff_start, expon_start):
        for c in coeff_opts:
            sign_c = Mul(Integer(sign), c)
            for e in expon_opts:
                if (c != coeff_start or e != expon_start):
                    yield Mul(sign_c, Pow(n, e))
