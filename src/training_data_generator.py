import random

from sympy import sympify
from util import it_combinations
from exprmap import COEFF_BOUND, EXPON_BOUND, TERM_BOUND, exprmap_term

import exprutils
import numpy as np

def main():
    problem_set = generate_problem_set()
    training_data = generate_training_data(problem_set)
    save_training_data_to_binary_file(training_data)
    
def save_to_file(lines, file_name):
    with open(file_name, 'w+') as file:
        for line in lines:
            file.write("{0}\n".format(line))

def generate_problem_set():
    
    def step():
        data = gen_top_down_and_bot_up_to_factor_out_n()
        for i in gen_denominator_up_to_factor_out_n():
            data.add(i)
        print('PROBLEM SET LENGTH: ' + str(len(data)))
        save_to_file(data, 'data/txt/proof_ex.txt')
        return data
    
    COEFF_SET = [i + 1 for i in range(COEFF_BOUND - 1)]
    EXPON_SET = [i + 1 for i in range(EXPON_BOUND)]
    
    def selection_n(opts, *pct_array):
        counts = map((lambda p : round(p * len(opts))), pct_array)
        subsets = list(map((lambda c : random.sample(opts, c)), counts))
        def append_tuple(x, value):
            if (type(x) == int):
                x = [x]
            else:
                x = list(x)
            x.append(value)
            return tuple(x)
        return it_combinations(subsets, append_tuple)
        
    def gen_constant_denominator():
        results = set()
        # these mess up training the neural network
#        for e in range(2, EXPON_BOUND + 1):
#            top = 'n**{}'.format(e)
#            for d in range(COEFF_BOUND + 1):
#                seq = '{}/{}'.format(top, d)
#                seq2 = '{}/{}'.format('n', d)
#                results.add(seq + ',' + seq2)
        for e1, e2 in selection_n(EXPON_SET, 0.8, 0.8):
            if (e1 != e2):
                if (e2 > e1):
                    e1, e2 = e2, e1
                for c1, c2 in selection_n(COEFF_SET, 0.6, 0.6):
                    t1 = '{}*n**{}'.format(c1, e1)
                    t2 = '{}*n**{}'.format(c2, e2)
                    top = t1 + '+' + t2
                    for d in range(1, COEFF_BOUND + 1):
                        seq = '({})/{}'.format(top, d)
                        step1 = '({})/{}'.format(t1, d)
                        step2 = '{}/{}'.format('n', d)
                        results.add(','.join([seq, step1, step2]))
        return results
    
    def gen_top_down_and_bot_up_to_factor_out_n():
        results = set()
        for c1, c2, c3, c4 in selection_n(COEFF_SET, 0.3, 0.3, 0.6, 0.6):
            for e1, e2, e3, e4 in selection_n(EXPON_SET, 0.6, 0.3, 0.6, 0.3):
                if (e1 != e2 and e3 != e4):
                    if (e2 > e1):
                        e1, e2 = e2, e1
                    if (e4 > e3):
                        e3, e4 = e4, e3
                    top = Numerator(c1, e1, c2, e2)
                    bot = Denominator(c3, e3, c4, e4)
                    results.add(get_steps_topfirst(top, bot, e3))
        return results
                
    def get_steps_topfirst(top, bot, factor_out):
        steps = []
        steps.append('({})/({})'.format(top.start(), bot.start()))
        for i in top.steps():
            steps.append('({})/({})'.format(i, bot.start()))
        top_end = top.steps()[-1]
        for i in bot.steps():
            steps.append('({})/({})'.format(top_end, i))
        steps.append('({})/({})'.format(top.factor_out(factor_out), bot.factor_out()))
        return ','.join(steps)
    
    class Numerator:
        
        def __init__(self, c1, e1, c2, e2):
            self.c1 = c1
            self.c2 = c2
            self.e1 = e1
            self.e2 = e2 if random.choice([True, False, False, False]) else 0
            
        def start(self):
            return '{}*n**{}+{}*n**{}'.format(self.c1, self.e1, self.c2, self.e2)
        
        def steps(self):
            return ['{}*n**{}'.format(self.c1, self.e1), 
                    'n**{}'.format(self.e1)]
        
        def factor_out(self, e):
            return 'n**{}'.format(self.e1 - e)
    
    class Denominator:
        
        def __init__(self, c1, e1, c2, e2):
            self.c1 = c1
            self.c2 = c2
            self.e1 = e1
            self.e2 = e2 if random.choice([True, False, False, False]) else 0
            
        def start(self):
            return '{}*n**{}+{}*n**{}'.format(self.c1, self.e1, self.c2, self.e2)
            
        def steps(self):
            return ['{}*n**{}'.format(self.c1 + 1, self.e1)]
        
        def factor_out(self):
            return str(self.c1 + 1)
    
    return step()

###############################################################################
 
def generate_training_data(problem_set):
    
    def step():
        data = [row.split(',') for row in problem_set]
            
        frac_pairs = []
        for row in data:
            for i, j in zip(row, row[1:]):
                frac_pairs.append([i, j])

        """
        '(6*n**2+3*n)/(2*n)'
        => [6*n**2 + 3*n, 2*n]
        => [ [(1, 6, 2), (1, 3, 1), (0, 0, 0)], [(1, 2, 1), (0, 0, 0), (0, 0, 0)] ]
        => [ [28, 14, 0], [13, 0, 0] ]
        => [28, 14, 0, 13, 0, 0]
        => ['28', '14', '0', '13', '0', '0']
        """
        lines = []
        for frac_pair in frac_pairs:
            for func in [_split_sympify, _get_term_parts, 
                         _exprmap_terms, _flatten, _stringify]:
                frac_pair = list(map((lambda x: func(x)), frac_pair))
            lines.append(','.join(frac_pair[0]) + '|' + ','.join(frac_pair[1]))
            
        save_to_file(lines, 'data/txt/nn_data.txt')
        print('TRAINING DATA LENGTH: ' + str(len(lines)))
        return lines
    
    def _append_empty_term_parts(term_parts_list):
        while(len(term_parts_list) < TERM_BOUND):
            term_parts_list.append((0, 0, 0))
        return term_parts_list
    
    def _split_sympify(frac):
        return [sympify(expr) for expr in frac.split('/')]
    
    def _get_term_parts(pair):
        return [_append_empty_term_parts(exprutils.get_all_term_parts(expr)) 
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
                
    return step()

###############################################################################
    
def save_training_data_to_binary_file(training_data):
    arr_x = np.empty((len(training_data), TERM_BOUND * 2), dtype='int16')
    arr_y  = np.empty((len(training_data), TERM_BOUND * 2), dtype='int16')
    for i, line in enumerate(training_data):
        split = line.split('|')
        for j, x in enumerate(split[0].split(',')):
            arr_x[i][j] = int(x)
        for j, x in enumerate(split[1].split(',')):
            arr_y[i][j] = int(x)
    print(arr_x)
    np.save('data/nn_x.npy', arr_x)
    np.save('data/nn_y.npy', arr_y)

###############################################################################

main()
