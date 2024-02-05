---
theme: default
class: text-center
highlighter: shikiji
lineNumbers: false
drawings:
  persist: false
transition: slide-left
title: Qibocal tutorial
mdc: true
layout: center
---

# Introducing Qibocal
Qubit calibration using Qibo

---

# Presentation of the program

<center>
<img src="/qq_qibocal.svg" alt="Qibocal scheme"   width="600">
</center>

---
clicks: 3
---

# Routine: data acquisition


<div h="full" flex="~ row" gap="lg" p="sm b-20">
<div flex="~ col" p="t-5">


```py{all|7-9|12-14|17-20}
from dataclasses import dataclass
from qibocal.auto.operation import Parameters, Data
from qibolab.platform import Platform
from qibolab.qubits import QubitId


@dataclass
class RoutineParameters(Parameters):
    """Input parameters for YAML runcard."""


@dataclass
class RoutineData(Data):
    """Data structure for acquisition data."""


def acquisition(params: RoutineParameters,
                platform: Platform,
                qubits: list[QubitId]) -> RoutineData:
    """Acquisition protocol."""

```
</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

`RoutineParameters` experiment configuration.

</p>

<p v-click="2">

`RoutineData` data acquired by the protocol

</p>

<p v-click="3">

`RoutineParameters` and `RoutineData` are connected through `acquisition` which
is the function which will presumably use `Qibolab` code to perform acquisition.
</p>

</div>
</div>

---
clicks: 3
---

# Routine: post-processing


<div h="full" flex="~ row" gap="lg" p="sm b-20">
<div flex="~ col" p="t-5">


```py{all|7-9|12-13|16-19}
from dataclasses import dataclass
from qibolab.platform import Platform
from qibolab.qubits import QubitId
from qibocal.auto.operation import Results


@dataclass
class RoutineResults(Results):
    """Post-processed results."""


def fit(data: RoutineData) -> RoutineResults:
    """Extracting features from data."""


def update(results: RoutineResults,
           qubit: QubitId,
           platform: Platform) -> None:
    """Updating platform parameters'."""

```
</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

`RoutineResults` class containing the analysis of the raw data

</p>

<p v-click="2">

`fit` optional function which performs the post-processing analysis

</p>

<p v-click="3">

`update` optional function which updates specific calibration parameters computed
in `Results`

</p>

</div>
</div>

---
clicks: 2
---

# Routine: reporting


<div h="full" flex="~ row" gap="lg" p="sm b-20">
<div flex="~ col" p="t-5">


```py{all|6-9|16-17}
import plotly.graph_objects as go
from qibolab.qubits import QubitId
from qibocal.auto.operation import Routine


def report(data: RoutineData,
           qubit: QubitId,
           results: RoutineResults) -> tuple[list[go.Figure], str]:
    """Updating platform parameters'."""






# define Routine object
routine = Routine(acquisition, fit, report, update)




```
</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

`report` is the function where you plot the data or results obtained.
[The](The) return type should include the following:


- list of `go.Figure`, which are figure realized with plotly

- a str, which is a generic HTML code that can be injected and it
  will be rendered correctly in the report

</p>

<p v-click="2">

We can create an instance of `Routine` by passing `acquisition`,
`fit`, `report` and `update`.

</p>
</div>
</div>

___

---

# How to add a new protocol?
##
Suppose that we want to code a protocol to perform a RX rotation for different angles.
<div h="full" flex="~ row" gap="lg">
<p v-click="1">
<div flex="~ col">
<b>Parameters</b>
<p>
First, we define the input parameters of our experiment 
inheriting the Qibocal <i>Parameters</i> class.
</p>
```py
from dataclasses import dataclass
from ...auto.operation import Parameters
@dataclass
class RotationParameters(Parameters):
    """Parameters for rotation protocol."""
    theta_start: float
    """Initial angle."""
    theta_end: float
    """Final angle."""
    theta_step: float
    """Angle step."""
    nshots: int
    """Number of shots."""
```
</div>
</p>
<p v-click="2">
<div flex="~ col">
<b>Data</b>
<p>
Secondly, we define a data structure that aims at storing both the angles and the probabilities measured for each qubit.
</p>
```py
import numpy as np
import numpy.typing as npt
from dataclasses import dataclass, field
from ...auto.operation import Data

RotationType = np.dtype([("theta", np.float64), ("prob", np.float64)])

@dataclass
class RotationData(Data):
    """Rotation data."""

    data: dict[QubitId, npt.NDArray[RotationType]] = 
        field(default_factory=dict)
    """Raw data acquired."""

```
</div>
</p>
</div>

---
clicks: 3
---

# Data acqusition

<div h="full" flex="~ row" gap="lg" p="sm b-20">
<div flex="~ col" p="t-5">
```py{all|1-9|10-12|13-22}
from qibolab.platform import Platform
from ...auto.operation import Qubits
def acquisition(
    params: RotationParameters,
    platform: Platform,
    qubits: Qubits,
) -> RotationData:
    
    angles = np.arange(params.theta_start, params.theta_end, params.theta_step)
    
    data = RotationData()
    
    for angle in angles:
    
        circuit = Circuit(platform.nqubits)
        
        for qubit in qubits:
            circuit.add(gates.RX(qubit, theta=angle))
            circuit.add(gates.M(qubit))
            
        result = circuit(nshots=params.nshots)

```
</div>

<div flex="~ col justify-center" v="full" p="t-2">

<p v-click="1">

In the acquisition function we are going to perform the experiment.


- We define the angle range according to the input parameters,
</p>
<p v-click="2">

- allocate the data structure <em>RotationData</em>
</p>
<p v-click="3">

- We build the circuit with an <em>RX</em> gate and execute it on hardware.
</p>
</div>
</div>

---
clicks: 3
---

# Data acquisition

```py{5-13|7-9|10-12|13}
        for qubit in qubits:
            circuit.add(gates.RX(qubit, theta=angle))
            circuit.add(gates.M(qubit))

        result = circuit(nshots=params.nshots)

        for qubit in qubits:
            
            prob = result.probabilities(qubits=[qubit])[0]
            
            data.register_qubit(qubit, theta=angle, prob=prob)

    return data
```

<p v-click="1">

- Extract probability of 0,
</p>
<p v-click="2">

- save the angles and the probabilities in the data structure,
</p>
<p v-click="3">

- return the data.
</p>

---
layout: center
---

# Result class
##
Here we decided to code a generic Result that contains the fitted parameters for each quibt.
```py{all}
from qibolab.qubits import QubitId

@dataclass
class RotationResults(Results):
    """Results object for data"""
    fitted_parameters: dict[QubitId, list] = field(default_factory=dict)
```

---
---
<div h="full" flex="~ row" gap="lg">
<p v-click="1">
<div flex="~ col">
<b>Fit function</b>
<p>
The following function performs a sinusoidal fit for each qubit.
</p>

```py
def fit(data: RotationData) -> RotationResults:
    qubits = data.qubits
    freqs = {}
    fitted_parameters = {}

    def cos_fit(x, offset, amplitude, omega):
        return offset + amplitude * np.cos(omega*x)

    for qubit in qubits:
        qubit_data = data[qubit]
        thetas = qubit_data.theta
        popt, _ = curve_fit(cos_fit, thetas, qubit_data.prob)
        freqs[qubit] = popt[2] / 2*np.pi
        fitted_parameters[qubit]=popt.tolist()
    return RotationResults(
        fitted_parameters=fitted_parameters,
    )
```
</div>
</p>
<p v-click="2">
<div flex="~ col">
<b>Plot function</b>
<p>
The report function generates a list of figures and an optional table to be 
shown in the html report.
</p>
```py
def plot(data: RotationData, fit: RotationResults, qubit):
"""Plotting function for rotation."""
    figures = []
    fig = go.Figure()
    fitting_report = ""
    qubit_data = data[qubit]
    fig.add_trace(
        go.Scatter(
            x=qubit_data.theta,
            y=qubit_data.prob,
    ... 
    
    return figures, fitting_report
```
<p>
For more details about this function look at the
<a href="https://qibo.science/qibocal/stable/tutorials/advanced.html#report-function">
doc</a>.
</p>
</div>
</p>
</div>

---
clicks: 3
---

## Create Routine object

```py
rotation = Routine(acquisition, fit, plot)
"""Rotation Routine  object."""
```

<div h="full" flex="~ row" gap="lg">
<p v-click="1">
<div flex="~ col">

<b>Add routine to Operation Enum</b>
```py
# other imports...
from rotate import rotation

class Operation(Enum):
## other protocols...
rotation = rotation
```

</div>
</p>
<p v-click="2">

<b>Write a runcard</b>
<div flex="~ col">
```yml
platform: dummy

qubits: [0,1]


actions:
    - id: rotate
      priority: 0
      operation: rotation
      parameters:
        theta_start: 0
        theta_end: 7
        theta_step: 20
        nshots: 1024</p>
```

</div>
</p>
<p v-click="3">

<b>Run the routine</b>

After running `qq auto` a report is generated.
<div flex="~ col">
<img src="https://qibo.science/qibocal/stable/_images/output.png" alt="Routine plot">
</div>
</p>
</div>

---
---
# Qibocal as a library
##
Qibocal also allows executing protocols without the standard interface.
<div h="full" flex="~ row" gap="lg">
<div flex="~ col">
<p v-click="1">
We show how to run a single protocol using Qibocal as a library
```py
from qibocal.protocols.characterization import Operation
from qibolab import create_platform

# allocate platform
platform = create_platform("....")
# get qubits from platform
qubits = platform.qubits

# we select the protocol
protocol = Operation.single_shot_classification.value
```
In order to run a protocol the user needs to specify the parameters.
```py
parameters = experiment.parameters_type.load(dict(nshots=1024))
```
</p>
</div>
<p v-click="2">
<div flex="~ col">
The user can perform the acquisition using <em>experiment.acquisition</em>
```py
data, acquisition_time = experiment.acquisition(
    params=parameters, platform=platform, qubits=qubits)
```
The fitting corresponding to the experiment can be launched in the following way:
```py
fit, fit_time = experiment.fit(data)
```
It is also possible to access the plots and the tables with the following lines
```py
# Plot for qubit 0
qubit = 0
figs, html_content = experiment.report(
    data=data, qubit=0, fit=fit)
```
</div>
</p>
</div>


---
layout: center
---

# Thanks for listening



---
layout: center
---

# Useful pages in documentation
---
layout: iframe
# the web page source
url: https://qibo.science/qibocal/stable/getting-started/runcard.html
---

---
layout: iframe

url: https://qibo.science/qibocal/stable/tutorials/advanced.html#how-to-use-qibocal-as-a-library
---

---
layout: iframe

url: https://qibo.science/qibocal/stable/tutorials/advanced.html#how-to-add-a-new-protocol
---
