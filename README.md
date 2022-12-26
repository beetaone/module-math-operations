# Math Operations

|                |                                       |
| -------------- | ------------------------------------- |
| Name           | Math Operations                           |
| Version        | v1.0.0                                |
| DockerHub | [weevenetwork/math-operations](https://hub.docker.com/r/weevenetwork/math-operations) |
| Authors        | Jakub Grzelak                   |

- [Math Operations](#math-operations)
  - [Description](#description)
  - [Supported Operations](#supported-operations)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)

## Description

This module enables performing math operations on the data. Supported operations: + - * / % ^ ceil abs floor sqrt sin cos tan exp. Negative numbers must be put in brackets, i.e. (-9) or (-1.34). If you want to use received data, then refer to them in your calculations formula by placing their label in double curly brackets, i.e. if your data is { 'temperature': 12, 'volume': 3 } and want to use temperature in your calculations then refer to it as {{temperature}}

Sample calculations:

* `{{temperature}} * 9 / 5 + 32`
* `1/2 + (2 + 3) / (sin((-9) - 2)^2 - 6/7) - cos(1) + {{temperature}}`
* `{{temperature}} * {{volume}} / (-12)`

## Supported Operations

| Operand             | Description               |
| -------------------- | ------------------------- |
| `+` | Sum of two numbers. |
| `-` | Subtraction of two numbers. |
| `*` | Multiplication of two numbers. |
| `/` | Division of two numbers. |
| `%` | Modulus. |
| `^` | Power. |
| `ceil(x)` | Return the ceiling of x, the smallest integer greater than or equal to x. |
| `abs(x)` | Return the absolute value of x. |
| `floor(x)` | Return the floor of x, the largest integer less than or equal to x. |
| `sqrt(x)` | Return the square root of x. |
| `sin(x)` | Return the sine of x radians. |
| `cos(x)` | Return the cosine of x radians. |
| `tan(x)` | Return the tangent of x radians. |
| `exp(x)` | Return e raised to the power x, where e = 2.718281… is the base of natural logarithms. |

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Name                 | Environment Variables     | type     | Description                                              |
| -------------------- | ------------------------- | -------- | -------------------------------------------------------- |
| Formula    | FORMULA         | string   | Build a mathematics formula using supported operations. To use data in your calculations refer to their labels in double curly brackets {{...}}.            |
| Result Label    | RESULT_LABEL         | string  | Assign calculations results to this label.            |
| Action on Result    | NEW_RESULT         | string  | What to do with the calculated results? Update result label? Output as stand alone data? Options: `update` or `stand-alone`. If selected `update` then calculated value will update value assigned to `Result Label` or append to the data object received by the module if `Result Label` is not present. If selected `stand-alone` then data received by the module will be disregarded and the module will output a new JSON object holding calculated value and assigned to `Result Label`             |


### Set by the weeve Agent on the edge-node

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

| Environment Variables | type   | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| MODULE_NAME           | string | Name of the module                             |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output)  |
| EGRESS_URLS            | string | HTTP ReST endpoints for the next module         |
| INGRESS_HOST          | string | Host to which data will be received            |
| INGRESS_PORT          | string | Port to which data will be received            |

## Dependencies

```txt
bottle
requests
```

## Input

Input to this module is:

* JSON body single object, example:

```json
{
    "temperature": 12,
    "volume": 3
}
```

* array of JSON body objects, example:

```json
[
    {
        "temperature": 12,
        "volume": 3
    },
    {
        "temperature": 10,
        "volume": 4
    },
    {
        "temperature": 1.3234,
        "volume": 3
    }
]
```

## Output

If the following module configuration is provided `FORMULA = {{temperature}} * 9/5 + 32`, `RESULT_LABEL = temperatureFahrenheit`, `NEW_RESULT = update` then output of this module to the above input data will be:

* JSON body single object, example:

```json
{
    "temperature": 12,
    "volume": 3,
    "temperatureFahrenheit": 53.6
}
```

* array of JSON body objects, example:

```json
[
    {
        "temperature": 12,
        "volume": 3,
        "temperatureFahrenheit": 53.6
    },
    {
        "temperature": 10,
        "volume": 4,
        "temperatureFahrenheit": 50
    },
    {
        "temperature": 1.3234,
        "volume": 3,
        "temperatureFahrenheit": 34.38212
    }
]
```
