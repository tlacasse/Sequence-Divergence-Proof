from sympy import Add, sympify
from exprutils import get_term_parts

COEFF_BOUND = 10
EXPON_BOUND = 5
TERM_BOUND = 3

def exprmap_term(term_parts):
    sign, coeff, expon = term_parts[0], term_parts[1], term_parts[2]
    value = coeff + ((COEFF_BOUND + 1) * expon)
    return sign * value

def exprmap(expr):
    terms = [expr] if expr.func != Add else list(expr.args)
    terms = [get_term_parts(t) for t in terms]
    mapped = list(map((lambda t: exprmap_term(t)), terms))
    mapped.extend([0, 0, 0])
    mapped = mapped[:TERM_BOUND]
    mapped.sort()
    value = 0
    for i, v in enumerate(mapped):
        # * 2 to account for addition and subtraction
        value += v * ((EXPRMAP.TERM_VALUE * 2)**i)
    return value

class ExprMapValues:
    
    def __init__(self):
        self.TERM_VALUE = exprmap_term(
                (1, COEFF_BOUND, EXPON_BOUND + 1)) + 1

    def calc(self):
        self.EXPR_VALUE = exprmap(sympify(
                '{0}*n**{1} + {0}*n**{2} + {0}*n**{3}'.format(COEFF_BOUND, 
                     EXPON_BOUND, EXPON_BOUND - 1, EXPON_BOUND - 2)))

EXPRMAP = ExprMapValues()
EXPRMAP.calc()
