from sympy import sympify
from problems import SeqFraction
import exprutils

def do_assert(result, expected):
    print(str(result) + ' =?= ' + str(expected))
    assert result == expected

# exprutils.get_term_parts
    
result = exprutils.get_term_parts(sympify('0'))
expected = (0, 0, 0)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('5'))
expected = (1, 5, 0)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('n'))
expected = (1, 1, 1)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('3*n'))
expected = (1, 3, 1)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('n**2'))
expected = (1, 1, 2)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('n**5'))
expected = (1, 1, 5)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('4*n**2'))
expected = (1, 4, 2)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('7*n**6'))
expected = (1, 7, 6)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('-2'))
expected = (-1, 2, 0)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('-6*n'))
expected = (-1, 6, 1)
do_assert(result, expected)

result = exprutils.get_term_parts(sympify('-4*n**2'))
expected = (-1, 4, 2)
do_assert(result, expected)

# exprutils.replace_term

result = exprutils.replace_term(sympify('n'), 0, sympify('n**2'))
expected = sympify('n**2')
do_assert(result, expected)

result = exprutils.replace_term(sympify('2*n**2 + 3*n'), 1, sympify('5'))
expected = sympify('2*n**2 + 5')
do_assert(result, expected)

# exprutils.expr_denominator

for d in ['n', 'n**2']:
    result = exprutils.expr_denominator(sympify('(2*n + 3) / ' + d))
    expected = sympify(d)
    do_assert(result, expected)
    
    result = exprutils.expr_denominator(sympify('1 / ' + d))
    expected = sympify(d)
    do_assert(result, expected)
    
# exprutils.expr_compare
    
result = exprutils.expr_compare(sympify('2*n + 3'), sympify('2*n + 3'))
expected = 0
do_assert(result, expected)

result = exprutils.expr_compare(sympify('2*n + 3'), sympify('2*n'))
expected = -1
do_assert(result, expected)

result = exprutils.expr_compare(sympify('2*n'), sympify('2*n + 3'))
expected = 1
do_assert(result, expected)

result = exprutils.expr_compare(sympify('n + 5'), sympify('2*n'))
expected = 1
do_assert(result, expected)

# exprutils.factor_out

result = exprutils.factor_out(sympify('2*n + 3'), 'n')
expected = None
do_assert(result, expected)

result = exprutils.factor_out(sympify('2*n**2 + 3*n'), 'n')
expected = sympify('2*n + 3')
do_assert(result, expected)

result = exprutils.factor_out(sympify('2*n**3 + 3*n**2'), 'n')
expected = sympify('2*n**2 + 3*n')
do_assert(result, expected)

result = exprutils.factor_out(sympify('2*n**3 + 3*n**2'), 'n**2')
expected = sympify('2*n + 3')
do_assert(result, expected)

# problems.SeqFraction.is_valid

frac = SeqFraction('n**2 + 3','n + 5')
result = frac.is_valid()
expected = True
do_assert(result, expected)

frac = SeqFraction('n + 3','n**2 + 5')
result = frac.is_valid()
expected = False
do_assert(result, expected)

# problems.SeqFraction.is_valid_order

frac1 = SeqFraction('n**2 + 3','n + 5')
frac2 = SeqFraction('n**2 + 3','2*n')
result = frac1.is_valid_order(frac2)
expected = True
do_assert(result, expected)

frac1 = SeqFraction('n**2 + 3','n + 5')
frac2 = SeqFraction('n**2 + 3','n')
result = frac1.is_valid_order(frac2)
expected = False
do_assert(result, expected)

frac1 = SeqFraction('n**2 + 3','n + 5')
frac2 = SeqFraction('n','n + 5')
result = frac1.is_valid_order(frac2)
expected = True
do_assert(result, expected)

frac1 = SeqFraction('n**2 + 3','n + 5')
frac2 = SeqFraction('n**2 + 3*n','n + 5')
result = frac1.is_valid_order(frac2)
expected = False
do_assert(result, expected)

############

print('complete')
