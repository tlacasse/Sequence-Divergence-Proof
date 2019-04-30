from sympy import Mul, Add, Integer
from sympy.printing import latex
from sympy.solvers import solve
from sympy.abc import n, M

import subprocess

PROOF_INSERT_MARKER = '%%%proof%%%'

TEX_TEMPLATE = '''
\\documentclass[12pt]{article}
\\usepackage{amsmath}
\\usepackage{geometry}
\\geometry{
    a4paper,
    left = 1in,
    right = 1in,
    top = 1in,
    textheight = 9.5in,
    footskip = 1in,
}
\\begin{document}
\\noindent
\\begin{align*}
    %%%proof%%%
\\end{align*}
\\end{document}
'''

class Proof:
    
    def __init__(self, steps):
        self.steps = steps
        self.N = None
        
    def get_step_count(self):
        return len(self.steps)
        
    def solve_for_N(self):
        self.N = solve(Add(self.steps[-1].to_frac_expr(), Mul(Integer(-1), M)), n)
        return self.N
    
    def latex_gt_chain(self):
        return ' \geq '.join([latex(f.to_frac_expr()) for f in self.steps]) + ' \geq M'

    def write_proof_file(self, file_name = 'proof'):
        tex = TEX_TEMPLATE.replace(PROOF_INSERT_MARKER, self.latex_gt_chain())
        with open(file_name + '.tex', 'w+') as file:
            file.write(tex)
        subprocess.run(['pdflatex', file_name + '.tex'])
