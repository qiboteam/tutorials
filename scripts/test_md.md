#### Test file to be opened with `md2md.py` script

This is normal text in markdown mode.
The following is LaTeX in markdown mode:

$$ y = f(x) $$

```python
import qibo
from qibo import models, gates 
qibo.set_backend('numpy')
```

Now we will write a code block defining a circuit.

```python
c = models.Circuit(1)
c.add(gates.H(0))
c.add(gates.M(0))
```

Finally we perform a circuit execution and calculate final state probabilities.

```python
probs = c.execute(nshots=1000).probabilities(qubits=[0])
print(probs)
```

This is the last line of this test markdown.
