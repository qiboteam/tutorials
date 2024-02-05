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
#layout: image-left
---

# Qibolab

Getting started tutorial

---
clicks: 3
---

# `qibolab_hello_world.py`

*Instead of contents...*

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {all|5|7-9|11-12}
from qibolab import create_platform
from qibolab.pulses import PulseSequence
from qibolab.execution_parameters import ExecutionParameters

platform = create_platform("myplatform")

sequence = PulseSequence()
ro_pulse = platform.create_MZ_pulse(qubit=0, start=0)
sequence.add(ro_pulse)

options = ExecutionParameters(nshots=1000)
results = platform.execute_pulse_sequence(sequence, options)
```

</div>

<div flex="~ col justify-center">

`Platform` represents the lab configuration, containing all information about the available qubits and orchestrating the instruments.

`PulseSequence` contains the pulses to be executed.
Pulses can be constructed manually through the pulse API,
or via the `platform`.

The experiment is deployed using the `Platform`.

</div>

</div>

---
clicks: 3
---

# Pulse API

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {all|9|10|0}
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

`PulseSequence` is a list of pulses

```py
sequence = PulseSequence()
sequence.add(Pulse(...))
```

</div>

<div flex="~ col justify-center" v="full" p="t-10">

Pulse waveforms can have different shapes

- `Rectangular`
- `Exponential`
- `Gaussian`
- `GaussianSquare`
- `Drag`

Pulses can have different types

- `PulseType.READOUT`
- `PulseType.DRIVE`
- `PulseType.FLUX`

</div>

</div>

---
clicks: 4
---

# Platform

<div h="full" flex="~ row">

<div flex="~ col">

```py {1-5|7-9|11-|1-5}
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

```py {all|5-8}
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

---
clicks: 4
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
        port=instrument.ports("i1", output=False)
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

Instantiate instrument objects.

Create channels and connect them to instruments.

Create qubits and connect them to channels.

Instantiate platform with all the information.

</div>

</div>

---
clicks: 2
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

<div v-if="$clicks == 0">

We can register characterization and native gate parameters when creating qubits.

However these are parameters that are usually *calibrated*.

It is useful to store such parameters in an external *database*.

For simplicity we are providing tools (`qibolab.serialize`) that parse these parameters from YAML (or JSON).

</div>

<div v-if="$clicks >= 1">

```yaml
native_gates:
    single_qubit:
        0:
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

*Let's now put it all together...*

</div>

</div>

</div>

---
clicks: 4
---

# Creating platforms

using `qibolab.serialize`

<div h="full" flex="~ row">

<div flex="~ col">

```sh {all|3|4|5|all}
qibolab_platforms/
    myplatform/
        platform.py
        parameters.yml  # -> parameters.json
        kernels.npz # (optional)
```

<br>

<v-clicks at="0">

- `platform.py`: Contains the `create` method that initializes the `Platform`.
- `parameters.yml`: Contains parameters that are updated during calibration.
- other files (integration weights, etc.) can also be provided and loaded in `create`.

</v-clicks>

<br>

```sh
export QIBOLAB_PLATFORMS=./qibolab_platforms
```

</div>

<div flex="~ col">

```py {all|8-10|8-10|all}{at:1}
FOLDER = Path(__file__).parent

def create():
    instrument = DummyInstrument("myinstr", "0.0.0.0:0")

    channels = ChannelMap()
    channels |= ...

    runcard = load_runcard(FOLDER)
    qubits, couplers, pairs = load_qubits(runcard)

    qubits[0].readout = channels["readout"]
    qubits[0].feedback = channels["feedback"]
    qubits[0].drive = channels["drive"]

    return Platform(
        "myplatform",
        qubits,
        pairs,
        instruments={instrument.name: instrument},
    )
```

</div>

</div>

---
clicks: 2
---

# Acquiring results

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {all|16-18|10-11}{at:0}

platform = create_platform("myplatform")

sequence = PulseSequence()
ro_pulse = platform.create_MZ_pulse(qubit=0, start=0)
sequence.add(ro_pulse)

options = ExecutionParameters(
    nshots=1000,
    relaxation_time=100000,
    acquisition_type=AcquisitionType.DISCRIMINATION,
    averaging_mode=AveragingMode.SINGLESHOT

)
results = platform.execute_pulse_sequence(sequence, options)

print(results[ro_pulse.serial].samples)
print(results[0].samples)
```

`results` is a `dict` from `pulse.serial` to a results object.

</div>

<div flex="~ col justify-center" v="full" p="t-10">

Acquisition types:
- `RAW`: (I, Q) waveform
- `INTEGRATION`: (I, Q) voltage
- `DISCRIMINATION`: samples

Averaging modes:
- `SEQUENTIAL` *(not recommended)*
- `CYCLIC`
- `SINGLESHOT`

</div>

</div>

---
clicks: 1
---

# Real-time sweeps

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {7-12|14-20}
platform = create_platform("myplatform")

sequence = PulseSequence()
ro_pulse = platform.create_MZ_pulse(qubit=0, start=0)
sequence.add(ro_pulse)

sweeper = Sweeper(
    parameter=Parameter.frequency,
    values=np.arange(-2e8, +2e8, 1e6),
    pulses=[ro_pulse],
    type=SweeperType.OFFSET,
)

options = ExecutionParameters(
    nshots=1000,
    relaxation_time=1000,
    acquisition_type=AcquisitionType.INTEGRATION,
    averaging_mode=AveragingMode.CYCLIC
)
results = platform.sweep(sequence, options, sweeper)
```

</div>

<div flex="~ col justify-center" v="full" p="t-10">

Executing sweeps in real time is usually faster because
it requires less communication with the instruments.

</div>

</div>

---
clicks: 1
---

# Sequence unrolling

<div h="full" flex="~ row" gap="lg" p="sm b-20">

<div flex="~ col" p="t-5">

```py {3-9|11-17}
platform = create_platform("myplatform")

nsequences = 20
sequences = []
for _ in range(nsequences):
    sequence = PulseSequence()
    sequence.add(platform.create_MZ_pulse(qubit=0, start=sequence.finish))
    sequences.append(sequence)

options = ExecutionParameters(
    nshots=1000,
    relaxation_time=100000,
    acquisition_type=AcquisitionType.DISCRIMINATION,
    averaging_mode=AveragingMode.SINGLESHOT,
)
results = platform.execute_pulse_sequences(sequences, options)
```

</div>

<div flex="~ col justify-center" v="full" p="t-10">

Passing multiple sequences in a single call is usually faster because
it requires less communication with the instruments.

Sometimes sequences need to be *batched* in order to fit in the instruments
memory (WIP).

</div>

</div>

---
layout: center
---

# Thanks
