# derived from:
# https://qiskit.org/textbook/ch-algorithms/quantum-key-distribution.html

import numpy as np
from qiskit import QuantumCircuit,Aer
from numpy.random import randint,choice

simulator = Aer.get_backend('aer_simulator')

# Alice sends
n,k = 128,32
qc = QuantumCircuit(n,n)
a,c = randint(2, size=(2,n))

for i in range(n):
    if c[i]: qc.x(i)
    if a[i]: qc.h(i)

# Charlie intercepts
if True:
    b = randint(2, size=n)
    for i in range(n):
        if b[i]: qc.h(i)
        qc.measure(i,i)

    job = simulator.run(qc, shots=1, memory=True)
    result = job.result().get_memory()[0]

    for i in range(n):
        if b[i]: qc.h(i)

# Bob receives
b = randint(2, size=n)
for i in range(n):
    if b[i]: qc.h(i)
    qc.measure(i,i)

job = simulator.run(qc, shots=1, memory=True)
result = job.result().get_memory()[0]
d = np.flipud([int(d) for d in result])

# Alice and Bob check
e,f = c[a==b], d[a==b]
m = len(e)
sample = choice(m, m-k, replace=False)
if np.all(e[sample]==f[sample])): print('secure')
else: print('insecure')

# make keys
key = np.setdiff1d(np.arange(m), sample)
A_key, B_key = e[key], f[key]
print('Alice key', A_key)
print('Bob key  ', B_key)
