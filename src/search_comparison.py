import csv
import random

from prove_diverge import build_prover, run_proof

lines = None
with open('data/txt/proof_ex.txt', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    lines = [row for row in reader]

problems = [row[0] for row in lines]
random.shuffle(problems)
problems = problems[:20]
    
dfs_prover = build_prover('dfs', printsearch=True)
nn_prover = build_prover('nn', printsearch=True)
dfs_prover.search_limit = 100
nn_prover.search_limit = 100

provers = [dfs_prover, nn_prover]

count_all = [0, 0]
count_valid = [0, 0]
proof_len = [0, 0]

count = [0, 0]

for i, p in enumerate(problems):
    print('problem', i)
    for j, prover in enumerate(provers):
        frac = p.split('/')
        proof = run_proof(prover, frac[0], frac[1], nopdf=True)
        if (proof is not None):
            count[j] += 1
            count_all[j] += prover.count_all
            count_valid[j] += prover.count_valid
            proof_len[j] += proof.get_step_count()

print(count_all)
print(count_valid)
print(proof_len)
