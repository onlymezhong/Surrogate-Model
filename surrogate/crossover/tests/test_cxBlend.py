from surrogate.crossover.cxBlend import cxBlend

print '\nTest.crossover: cxBlend'
ind1 = range(0, 10)
ind2 = range(10, 20)
# ind2 = range(9,-1,-1)
print '\tInput:  ind1_desVar=\t' + '\t'.join(map(str, ind1)) + ''
print '\tInput:  ind2_desVar=\t' + '\t'.join(map(str, ind2)) + ''
[out1, out2] = cxBlend(ind1=list(ind1), ind2=list(ind2))
print '\tOutput: out1_desVar=\t' + '\t'.join(map(str, out1)) + ''
print '\tOutput: out2_desVar=\t' + '\t'.join(map(str, out2)) + ''
