from sympy import Add, Mul, Pow, Integer, lambdify, sympify, cancel
from sympy.abc import n

def is_neg_int(expr):
    return expr.is_integer and expr.is_negative

def is_single_term(expr):
    return expr.func != Add 

def replace_term(expr, i, new_term):
    if (expr.func != Add):
        return new_term
    else:
        new_expr = list(expr.args)
        new_expr[i] = new_term
        return Add(*new_expr) # unpack list
    
def expr_denominator(expr):
    if (expr.func == Pow or expr.func == Mul):
        search = [expr] if expr.func == Pow else expr.args
        for t in search:
            if (t.func == Pow and is_neg_int(t.args[1])):
                exp = abs(int(t.args[1]))
                if (exp > 1):
                    return t.args[0]**exp
                else:
                    return t.args[0]
    return None

def expr_compare(expr1, expr2):
    test_value = 10000 # sufficiently large, for most comparisons
    expr1_f = lambdify(n, expr1)
    expr2_f = lambdify(n, expr2)
    val1 = expr1_f(test_value)
    val2 = expr2_f(test_value)
    if (val1 < val2):
        return 1
    elif (val1 > val2):
        return -1
    else:
        return 0
    
# TODO: work with sqrt(n)
def factor_out(expr, factor):
    factor = sympify(factor)
    divide_out = Mul(expr, Pow(factor, Integer(-1)))
    divide_out = cancel(sympify(divide_out))
    if (expr_denominator(divide_out) != None):
        return None
    else:
        return divide_out
