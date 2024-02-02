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
layout: image-left
---

# Qibolab

Presentation slides for developers

---

# `qibolab_hello_world.py`

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {all|5|7-9|11-12}
from qibolab import create_platform
from qibolab.pulses import PulseSequence
from qibolab.execution_parameters import ExecutionParameters

platform = create_platform("myplatform")

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

<p v-click="3">

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
- `GaussianSquare`
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

# Platform

<div h="full" flex="~ row">

<div flex="~ col">

```py
@dataclass
class Platform:
    qubits: QubitMap
    pairs: QubitPairMap
    instruments: InstrumentMap

    def connect(self):

    def disconnect(self):

    def execute_pulse_sequence(
        self, 
        sequences: PulseSequence, 
        options: ExecutionParameters
    ):

    def sweep(
        self, 
        sequence: PulseSequence, 
        options: ExecutionParameters, 
        *sweepers: Sweeper
    ):

```

</div>

<div flex="~ col">

Platform contains information about

- `qubits`: characterization and native single-qubit gates
- `pairs`: connectivity and native two-qubit gates
- `instruments`: used to deploy pulses *(drivers)*

<div v-click="1">

```py
@dataclass
class Qubit:
    readout_frequency: int
    drive_frequency: int

    readout: Optional[Channel]
    feedback: Optional[Channel]
    drive: Optional[Channel]

    native_gates: SingleQubitNatives
```

Qubits are connected to instruments via channels.

</div>

</div>

</div>

---

# Creating platforms

<div h="full" flex="~ row">

<div flex="~ col">

```py {all|2|4-12|14-16|18-23}
def create():
    instrument = DummyInstrument("myinstr", "0.0.0.0:0")

    channels = ChannelMap()
    channels |= Channel(
        "readout", 
        port=instrument.ports("o1")
    )
    channels |= Channel(
        "feedback", 
        port=instrument.ports("o2", output=False)
    )

    qubit = Qubit(0)
    qubit.readout = channels["readout"]
    qubit.feedback = channels["feedback"]

    return Platform(
        "myplatform", 
        qubits={qubit.name: qubit}, 
        pairs={}, 
        instruments={instrument.name: instrument},
    )
```

</div>

<div flex="~ col" v="full" p="t-10">

<p v-click="1">Instantiate instrument objects.</p>

<p v-click="2">Create channels and connect them to instruments.</p>

<p v-click="3">Create qubits and connect them to channels.</p>

<p v-click="4">Instantiate platform with all the information.</p>

</div>

</div>

---

# Qubit parameters

<div h="full" flex="~ row">

<div flex="~ col">

```py
native_gates = SingleQubitNatives(
    MZ=NativePulse(
        name="MZ",
        duration=1000,
        amplitude=0.005,
        shape="Rectangular()",
        pulse_type=PulseType.READOUT,
        qubit=qubit,
        frequency=int(7e9),
    ),
    RX=NativePulse(
        ...
    ),
)

qubit = Qubit(
    name=0,
    readout_frequency=7e9,
    drive_frequency=4.5e9,
    native_gates=native_gates,
)
```

</div>

<div flex="~ col justify-center">

We can register characterization and native gate parameters when creating qubits.

However these are parameters that are usually *calibrated*.

It is useful to store such parameters in an external *database*.

For simplicity we are using YAML (or JSON).

</div>

</div>

---

# Qubit parameters

<div h="full" flex="~ row">

<div flex="~ col">

```py
native_gates = SingleQubitNatives(
    MZ=NativePulse(
        name="MZ",
        duration=1000,
        amplitude=0.005,
        shape="Rectangular()",
        pulse_type=PulseType.READOUT,
        qubit=qubit,
        frequency=int(7e9),
    ),
    RX=NativePulse(
        ...
    ),
)

qubit = Qubit(
    name=0,
    readout_frequency=7e9,
    drive_frequency=4.5e9,
    native_gates=native_gates,
)
```

</div>

<div flex="~ col">

```yaml
native_gates:
    single_qubit:
        0: # qubit number
            MZ:
                duration: 1000
                amplitude: 0.005
                frequency: 7_000_000_000
                shape: Rectangular()
                type: ro # readout
                start: 0
                phase: 0
            RX:
                ...

characterization:
    single_qubit:
        0:
            readout_frequency: 7_000_000_000
            drive_frequency: 4_500_000_000

```

</div>

</div>

---

# Creating platform (using `qibolab.serialize`)

<div h="full" flex="~ row">

<div flex="~ col">

```sh
qibolab_platforms/
    myplatform/
        platform.py
        parameters.yml  # -> parameters.json
        kernels.npz # (optional)
```

<br>

- `platform.py`: Contains the `create` method that initializes the `Platform`.
- `parameters.yml`: Contains parameters that are updated during calibration.
- other files (integration weights, etc.) can also be provided and loaded in `create`.

<br>

```sh
export QIBOLAB_PLATFORMS=./qibolab_platforms 
```

</div>

<div flex="~ col">

```py {8-10}
FOLDER = Path(__file__).parent

def create():
    instrument = DummyInstrument("myinstr", "0.0.0.0:0")

    channels = ChannelMap()
    channels |= ...
    
    runcard = load_runcard(FOLDER)
    qubits, couplers, pairs = load_qubits(runcard)

    qubits[0].readout = channels["readout"]
    qubits[0].feedback = channels["feedback"]
    qubits[0].drive = channels[f"ch{q + 2}"]

    return Platform(
        "myplatform", 
        qubits, 
        pairs, 
        instruments={instrument.name: instrument}, 
    )
```

</div>

</div>
