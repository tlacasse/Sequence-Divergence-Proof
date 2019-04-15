from sympy import Symbol, Mul, Pow, Integer

n = Symbol('n')
N = Symbol('N')
M = Symbol('M')

class Proof:
    
    def __init__(self, problem):
        self.problem = problem
        self.steps = [problem]
    
    def proof_search(self):
        pass
    
    def descendant_nodes(self, expr):
        if (expr.func == Integer):
            return [Integer(0)]
        if (expr.func == Mul and expr.args[1].func == Pow):
            coeff = int(expr.args[0])
            expon = int(expr.args[1].args[1])
            results = [Integer(0), Integer(coeff)]
            for c in range(1, min(10, abs(coeff)) + 1):
                for e in range(1, expon + 1):
                    if not (c == coeff and e == expon):
                        results.append(Mul(c, Pow(n, e)))
            return results
        if (expr.func == Pow):
            expon = int(expr.args[1])
            results = [Integer(0)]
            for e in range(1, expon - 1):
                results.append(Pow(n, e))
            return results
        if (expr.func == Mul):
            coeff = int(expr.args[0])
            results = [Integer(0), Integer(coeff)]
            for c in range(1, min(10, abs(coeff))):
                results.append(Mul(c, n))
            return results
        return []
    
    def ascendant_nodes(self, expr):
        if (expr.func == Integer):
            return []
        
        if (expr.func == Mul):
            coeff = int(expr.args[0])
        else:
            coeff = 1
        
        if (expr.args[1].func == Pow):
            expon = int(expr.args[1].args[1])
        else:
            expon = 1
            
        results = []
        for c in range(coeff + 1, coeff + 2):
            for e in range(expon + 1, 6):
                results.append(Mul(c, Pow(n, e)))
        return results
