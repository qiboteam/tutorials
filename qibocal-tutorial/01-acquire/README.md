# Data acquisition using `Qibocal`

Let's assume that we want to acquire data for a specific protocol, the [single shot classification](https://github.com/qiboteam/qibocal/blob/main/src/qibocal/protocols/characterization/classification.py).

To execute the protocol we need to prepare the corresponding `yaml` file.

```yaml
platform: <platform_name>

qubits: [0]

actions:
  - id: single shot classification
    priority: 0
    operation: single_shot_classification
    parameters:
        nshots: 5000
```

We are now ready to execute the protocol using `qq acquire`.

```sh
qq acquire <path_to_yaml> -o <output_folder>
```

The `<output_folder>` will have the following structure:

```sh
<output_folder>/
    data/
        single_shot_classification_0/
            data.npz
            data.json
    platform/
        parameters.json
    runcard.yml
    meta.json
```

To produce an HTML report with the acquired data it is possible to use the
`qq report` command.

```sh
qq report <output_folder>
```

We will now find an `index.html` file inside output folder.