import fileinput
import mincemeat

data = (line for line in fileinput.input())

datasource = dict(enumerate(data))

def mapfn(k, v):
    words = v.split()
    if words is not None:
        words.sort()
        for w in words:
            yield w, 1

def reducefn(k, vs):
    result = sum(vs)
    return result

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server()

for k in sorted(results.keys()):
    print k, results[k]
