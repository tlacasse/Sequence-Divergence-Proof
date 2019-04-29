   
def it_combinations(arrs, join_op):
    if (len(arrs) == 1):
        return arrs[0]
    prev = it_combinations(arrs[:-1], join_op)
    result = []
    for i in prev:
        for j in arrs[-1]:
            result.append(join_op(i, j))
    return result
