from sympy import Symbol, Mul, Pow, Add, Integer
from problems import SeqFraction

n = Symbol('n')
N = Symbol('N')
M = Symbol('M')

class Proof:
    
    def __init__(self, problem):
        self.steps = [problem]
    
    def proof_search(self):
        # DFS
        while(len(self.steps) > 0):
            on = self.steps.pop()
            if (on.is_valid()):
                print(len(self.steps))
                print(on)
                for i, t in enumerate(on.numerator_split()):
                    for d in self.descendant_nodes(t):
                        new_top = self.replace_term(on.top, i, d)
                        self.steps.append(SeqFraction(new_top, on.bot))
    
    def replace_term(self, expr, i, new_term):
        if (expr.func != Add):
            return new_term
        else:
            new_expr = list(expr.args)
            new_expr[i] = new_term
            return Add(*new_expr) # unpack list
    
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
