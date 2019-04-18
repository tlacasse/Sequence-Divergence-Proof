from problems import SeqFraction

p = SeqFraction('n**2', 'n')

print(p)

print(p.factor_out_top('n'))
print(p.factor_out_bot('n'))

p = SeqFraction('n', '1')

print(p)

print(p.factor_out_top('n'))
print(p.factor_out_bot('n'))
