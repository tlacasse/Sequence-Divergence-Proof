from argparse import ArgumentParser

from problems import SeqFraction
from prover import Prover
from search import DFSSearch, NeuralNetworkSearch

def run_proof(prover, top, bot, nopdf=False, proofname='proof'):
    problem = SeqFraction(top, bot)
    proof = prover.proof_search(problem)
    if (not nopdf):
        proof.write_proof_file(proofname)
    return proof
    
def build_prover(search_method, printsearch):
    search_obj = None
    if (search_method == 'dfs'):
        search_obj = DFSSearch()
    if (search_method == 'nn'):
        search_obj = NeuralNetworkSearch() 
    prover = Prover(search_obj)
    prover.print = printsearch
    return prover

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('top')
    parser.add_argument('bot')
    parser.add_argument('--search')
    parser.add_argument('--nopdf', action='store_true')
    parser.add_argument('--printsearch', action='store_true')
    args = parser.parse_args()
    
    p = build_prover(args.search, args.printsearch)
    _ = run_proof(p, args.top, args.bot, nopdf=args.nopdf)
