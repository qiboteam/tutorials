import qibo
from qibo import models, gates 
qibo.set_backend('numpy')
c = models.Circuit(1)
c.add(gates.H(0))
c.add(gates.M(0))
probs = c.execute(nshots=1000).probabilities(qubits=[0])
print(probs)
