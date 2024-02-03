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

---
layout: center
---

# Thanks for listening