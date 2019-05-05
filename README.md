# Sequence-Divergence-Proof

Generating proofs of divergence of fractional-polynomial sequences as in your "Calculus with Proofs" course.

Requires the python modules in `setup.sh` and also `pdflatex`.

`prove_diverge.py` is the command-line script to generate the proof. Example:

> python prove_diverge.py 'n**2+3*n' 'n+5' --search nn --printsearch

Binary datasets and trained model are in `/src/data`, and text versions are in `/src/data/txt`.
- `proof_ex.txt` is a list of generated proofs, comma separated steps.
- `nn_data.txt` is a text version of the neural network training data, formatted as `input|output`.
