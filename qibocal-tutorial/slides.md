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

# How can we start using Quantum Computing?

##
<p align="center">
<img src="/intro.png" alt="Intro" width="600" height="600">
<em> Is it possible to create <strong> from scratch </strong> a framework for all of this?</em>
</p>

---

# Are we re-inventing the wheel?

##

You *could* say so however, compared to our competitors we have different priorities

1. Full open-source approach

2. Academic driven

3. Solutions for self-hosted Quantum Computers

<p align="center">
<img src="/wheel.png" alt="Intro" width="400" height="400">
</p>

---
transition: slide-up

layout: center
class: text-center

---

# Introducing Qibo

Open-source full stack API for quantum simulation, hardware control and calibration

---
layout: image
image: ./Qibo.svg
backgroundSize: contain
---

---
layout: image-right
image: ./calibration.png
backgroundSize: contain
---

# How to calibrate superconducting devices?

##

In superconducting qubits gates are implemented
through microwave pulses with durations of the orders of **nanoseconds**.

Several protocols need to be executed to tune such **short pulses**
and to extract specific parameters.

After an initial calibration more advanced experiments
can be performed in order to:

- improve readout
- run benchmarking protocols
- reach optimal control


---
layout: image
image: ./qpu_characterization.svg
backgroundSize: contain
---


---

# Qibocal workflow

<center>
<img src="/qq_qibocal.svg" alt="Qibocal scheme"   width="600">
</center>


---
layout: section
---

# How to encode calibration protocols

---

# Protocol encoding through `Routine` object
##
All protocols in Qibocal are encoded through a `Routine` object which is responsible for
providing how to perform:

* **data acquisition**: connecting to a QPU to run specific circuits or pulse sequences
* **post-processing**: analyze data to extract relevant features related to calibration
* **reporting**: display data with plots and tables
* **updating QPU**: after calibration a new instance of Platform will be generated


```py{all}
@dataclass
class Routine(Generic[_ParametersT, _DataT, _ResultsT]):
    """A wrapped calibration routine."""

    acquisition: Callable[[_ParametersT], _DataT]
    """Data acquisition function."""
    fit: Callable[[_DataT], _ResultsT] = None
    """Post-processing function."""
    report: Callable[[_DataT, _ResultsT], None] = None
    """Plotting function."""
    update: Callable[[_ResultsT, Platform], None] = None
    """Update function platform."""
```



---
clicks: 3
---

# Routine: data acquisition


<div h="full" flex="~ row" gap="lg" p="sm b-20">
<div flex="~ col" p="t-5">


```py{all|7-9|12-14|17-20|all}
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
                targets: list[QubitId]) -> RoutineData:
    """Acquisition protocol."""

```
</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

`RoutineParameters` experiment configuration.

</p>

<p v-click="2">

`RoutineData` data acquired by the protocol.

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


```py{all|7-9|12-13|16-19|all}
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
           target: QubitId,
           platform: Platform) -> None:
    """Updating platform parameters'."""

```
</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

`RoutineResults` class containing the analysis of the raw data.

</p>

<p v-click="2">

`fit` optional function which performs the post-processing analysis.

</p>

<p v-click="3">

`update` optional function which updates specific calibration parameters computed
in `Results`.
</p>

</div>
</div>

---
clicks: 2
---

# Routine: reporting


<div h="full" flex="~ row" gap="lg" p="sm b-20">
<div flex="~ col" p="t-5">


```py{all|6-9|16-17|all}
import plotly.graph_objects as go
from qibolab.qubits import QubitId
from qibocal.auto.operation import Routine


def report(data: RoutineData,
           target: QubitId,
           results: RoutineResults) -> tuple[list[go.Figure], str]:
    """Updating platform parameters'."""






# define Routine object
routine = Routine(acquisition, fit, report, update)




```
</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

`report` is the function that plots the data or results obtained.
The return type should include the following:


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
```py{all|1-9|10-12|13-22|all}
from qibolab.platform import Platform
from qibolab.qubits import QubitId
from ...auto.operation import Qubits
def acquisition(
    params: RotationParameters,
    platform: Platform,
    targets: list[QubitId],
) -> RotationData:

    angles = np.arange(params.theta_start, params.theta_end, params.theta_step)

    data = RotationData()

    for angle in angles:

        circuit = Circuit(platform.nqubits)

        for qubit in targets:
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

        for qubit in targets:

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

<div h="full" flex="~ row" gap="lg">
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
<p v-click="1">
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


__all__ = [
    # other protocols....
    "rotation",
]
```
<em>
We are working on a
<a href="https://github.com/qiboteam/qibocal/pull/869">
 better way </a>
to expose external protocols.
</em>
</div>
</p>
<p v-click="2">

<b>Write a runcard</b>
<div flex="~ col">
```yml
platform: dummy

targets: [0,1]


actions:
    - id: rotate
      operation: rotation
      parameters:
        theta_start: 0
        theta_end: 7
        theta_step: 20
        nshots: 1024
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
import pathlib
from qibolab import create_platform
from qibocal.auto.execute import Executor
from qibocal.auto.mode import ExecutionMode
from qibocal.protocols import t1_signal

# allocate platform
platform = create_platform("....")
# creare executor
executor = Executor.create(
  platform=platform,
  output=pathlib.Path("experiment_data")
)
```

</p>
</div>
<p v-click="2">
<div flex="~ col">
In order to run a protocol the user needs to specify the parameters.
```py
t1_params = {
    "id": "t1_experiment",
    "targets": [0],  # we are defining here which qubits to analyze
    "operation": "t1_signal",
    "parameters": {
        "delay_before_readout_start": 0,
        "delay_before_readout_end": 20_000,
        "delay_before_readout_step": 50,
    },
}
```
The user can perform acquisition and fit in the following way
```py
executor.run_protocol(t1_signal, t1_params, ExecutionMode.ACQUIRE)
executor.run_protocol(t1_signal, t1_params, ExecutionMode.FIT)
```
</div>
</p>
</div>

---

# Qibocal as a library
##

The user can now use the raw data acquired by the quantum processor to perform an arbitrary post-processing analysis.
This is one of the main advantages of this API compared to the CLI execution.

The history, that contains both the raw data (added with [qibocal.auto.mode.ExecutionMode.ACQUIRE](https://qibo.science/qibocal/latest/api-reference/qibocal.auto.html#qibocal.auto.mode.ExecutionMode.ACQUIRE))
and the fit data ([added with qibocal.auto.mode.ExecutionMode.FIT](https://qibo.science/qibocal/latest/api-reference/qibocal.auto.html#qibocal.auto.mode.ExecutionMode.FIT)) can be accessed

```py
history = executor.history
t1_res = history["t1_experiment"]  # id of the protocol

data = t1_res.data  # raw data
results = t1_res.results  # fit data
```

In particular, the history object returns a dictionary that links the id of the experiments with the [qibocal.auto.task.Completed](https://qibo.science/qibocal/latest/api-reference/qibocal.auto.html#qibocal.auto.task.Completed) object
---
layout: section
---

# Latest developments

---

# Latest developments
##
We are currently working on the following:

* Syntax for calibration scripts
* Two qubit gates protocols with cross resonance
* Documentation for all experiments
* Two qubit RB and interleaved RB
* Two qubit state tomography
* Advanced fits for resonators (UNIMIB)


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
url: https://qibo.science/qibocal/latest/getting-started/runcard.html
---

---
layout: iframe

url: https://qibo.science/qibocal/latest/tutorials/advanced.html
---
