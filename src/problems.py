from sympy import (sympify, cancel, oo, limit, 
                   Add, Pow, Mul, Integer)
import random

class SeqFraction:
    
    def __init__(self, top, bot):
        self.top = sympify(top)
        self.bot = sympify(bot)
    
    def __str__(self):
        return '(' + str(self.top) + ') / (' + str(self.bot) + ')'
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return other != None and self.top == other.top and self.bot == other.bot
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return 51 * hash(self.top) * hash(self.bot)
    
    def is_valid(self):
        return limit(str(self), 'n', oo) == oo
    
    def to_frac_expr(self):
        return sympify(str(self), evaluate = False)
    
    def top_split(self):
        return self.top.args if self.top.func == Add else (self.top, )
    
    def bot_split(self):
        return self.bot.args if self.bot.func == Add else (self.bot, )
    
    def factor_out_top(self, factor):
        return self.__factor_out(self.top, factor)
    
    def factor_out_bot(self, factor):
        return self.__factor_out(self.bot, factor)
    
    def is_done(self):
        return self.bot.is_constant()
    
    # TODO: work with sqrt(n)
    def __factor_out(self, expr, factor):
        factor = sympify(factor)
        divide_out = Mul(expr, Pow(factor, Integer(-1)))
        divide_out = cancel(sympify(divide_out))
        if (self.__get_expr_denominator(divide_out) != None):
            return None
        else:
            return divide_out
    
    def __get_expr_denominator(self, expr):
        if (expr.func == Mul):
            for t in expr.args:
                if (t.func == Pow 
                        and t.args[1].is_integer
                        and t.args[1].is_negative):
                    return t.args[0]
        if (expr.func == Pow):
            if (expr.args[1] == Integer(-1)):
                return expr.args[0]
        return None

class ProblemGenerator:
    
    def __init__(self, 
                 constant_bounds = [1, 100], 
                 exponent_bounds = [1, 3],
                 coeff_bounds = [-15, 15],
                 term_bounds = [1, 4]):
        self.constant_bounds = constant_bounds
        self.exponent_bounds = exponent_bounds
        self.coeff_bounds = coeff_bounds
        self.term_bounds = term_bounds

    def random_boolean(self):
        return random.choice([True, False])
    
    def random_in_bounds(self, bounds):
        return random.randint(bounds[0], bounds[1])

    def generate_term(self):
        if (self.random_boolean()):
            # constant
            return str(self.random_in_bounds(self.constant_bounds))
        # poly
        coeff = str(self.random_in_bounds(self.coeff_bounds))
        power = str(self.random_in_bounds(self.exponent_bounds))
        return coeff + '*n**' + power

    def generate_expression(self):
        return ' + '.join([
                self.generate_term() for t in range(self.term_bounds[0], 
                                                    self.term_bounds[1])])

    def generate_random_problems(self, count = 1):
        results = []
        for i in range(count):
            seq = '0'
            numerator = '0'
            denominator = '0'
            # force divergent sequences
            while (limit(seq, 'n', oo) != oo):
                # sympify to simplifiy
                numerator = str(sympify(self.generate_expression()))
                denominator = str(sympify(self.generate_expression()))
                seq = '(' + numerator + ') / (' + denominator + ')'
            results.append(SeqFraction(numerator, denominator))     
        return results if len(results) > 1 else results[0]
