# Data acquisition using `Qibocal`

`Qibocal` provides the infrastucture to perform a sequence of routines following
the dependencies defined by the user.
It is possible to define the tree dependencies directly in the runcard using the
keywords `priority` and `next`.

`priority` is an integer. The `Executor` in `Qibocal` runs all the routines in the
runcard in an increasing order of priority. It's mandatory that the starting routine
has priority zero.

The `next` keyword defines all routines to be executed after the current one.

If we want to perform a single shot classification after a qubit spettroscopy
the runcard will look like this:

```yaml
platform: dummy

qubits: [0]

actions:

  - id: qubit spectroscopy
    priority: 0
    operation: qubit_spectroscopy
    next: single shot classification
    parameters:
      drive_amplitude: 0.001
      drive_duration: 1000
      freq_width: 2_000_000
      freq_step: 500_000
      nshots: 10

  - id: single shot classification
    priority: 10
    operation: single_shot_classification
    parameters:
        nshots: 5000
```

We are now ready to execute the protocol using `qq acquire`.

```sh
qq acquire <path_to_yaml> -o <output_folder>
```
This command is the same as running sequentially [`qq acquire`](../01-acquire/README.md),
[`qq fit`](../02-fit/README.md), [`qq report`](../00-cli/README.md)
