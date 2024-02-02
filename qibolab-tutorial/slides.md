---
theme: default
class: text-center
highlighter: shikiji
lineNumbers: false
drawings:
  persist: false
transition: slide-left
title: Towards Qibolab 0.2.0
mdc: true
layout: center
---

# Control and Calibration using Qibo
Introduction to Qibolab and Qibocal

---

# `qibolab_hello_world.py`

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {all|5|7-9|11-12}
from qibolab import create_platform
from qibolab.pulses import PulseSequence
from qibolab.execution_parameters import ExecutionParameters

platform = create_platform("dummy")

equence = PulseSequence()
ro_pulse = platform.create_MZ_pulse(qubit=0, start=0)
sequence.add(ro_pulse)

options = ExecutionParameters(nshots=1000)
results = platform.execute_pulse_sequence(sequence, options)
```

</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

`Platform` represents the lab configuration, containing all information about the available qubits and orchestrating the instruments.

</p>

<p v-click="2">

`PulseSequence` contains the pulses to be executed.
Pulses can be constructed manually through the pulse API,
or via the `platform`.

</p>

<p>

The experiment is deployed using the `Platform`.

</p>

</div>

</div>

---

# Pulse API

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {all|9|10|1}
from qibolab.pulses import Pulse, PulseType, Rectangular

pulse = Pulse(
    start=0,          # Timing in nanoseconds (ns)
    duration=40,      # Pulse duration in ns
    amplitude=0.5,    # Amplitude of the waveform
    frequency=1e8,    # Frequency in Hz
    relative_phase=0, # Phase in radians
    shape=Rectangular(),
    type=PulseType.DRIVE,
    qubit=0,
)
```

<div v-click="3">

`PulseSequence` is a list of pulses

```py
sequence = PulseSequence()
sequence.add(Pulse(...))
```

</div>

</div>

<div flex="~ col justify-center" v="full" p="t-10">

<p v-click="1">

Pulse waveforms can have different shapes

- `Rectangular`
- `Exponential`
- `Gaussian`
- `Drag`

</p>

<p v-click="2">

Pulses can have different types

- `PulseType.READOUT`
- `PulseType.DRIVE`
- `PulseType.FLUX`

</p>

</div>

</div>

---

# Code

Use code snippets and get the highlighting directly, and even types hover![^1]

```py {all|5|1-6|9|all}
def create():
    # Create a controller instrument
    instrument = DummyInstrument("my_instrument", "0.0.0.0:0")

    # Create channel objects and assign to them the controller ports
    channels = ChannelMap()
    channels |= Channel("ch1out", port=instrument["o1"])
    channels |= Channel("ch2", port=instrument["o2"])
    channels |= Channel("ch1in", port=instrument["i1"])

    # create the qubit object
    qubit = Qubit(0)

    # assign native gates to the qubit
    qubit.native_gates = SingleQubitNatives(
        RX=NativePulse(
            name="RX",
            duration=40,
            amplitude=0.05,
            shape="Gaussian(5)",
            pulse_type=PulseType.DRIVE,
            qubit=qubit,
            frequency=int(4.5e9),
        ),
        MZ=NativePulse(
            name="MZ",
            duration=1000,
            amplitude=0.005,
            shape="Rectangular()",
            pulse_type=PulseType.READOUT,
            qubit=qubit,
            frequency=int(7e9),
        ),
    )

    # assign channels to the qubit
    qubit.readout = channels["ch1out"]
    qubit.feedback = channels["ch1in"]
    qubit.drive = channels["ch2"]

    # create dictionaries of the different objects
    qubits = {qubit.name: qubit}
    pairs = {}  # empty as for single qubit we have no qubit pairs
    instruments = {instrument.name: instrument}

    # allocate and return Platform object
    return Platform("my_platform", qubits, pairs, instruments, resonator_type="3D")
```

<arrow v-click="[3, 4]" x1="400" y1="420" x2="230" y2="330" color="#564" width="3" arrowSize="1" />

---
layout: center
class: text-center
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