all_goods = []
for i, name in enumerate(range(10, 0, -1)):
    all_goods.append(tuple([i, name]))

st = ', '.join([str(x) for x in all_goods])
print(st)