# metro-notation

Visualize the Rubik's cube algorithms in a notation like a train route map that I call **"Metro notation (メトロ記法)"**.

**"Metro notation"** focuses on the direction in which the force of each finger is applied.

## Installation

```sh
pip3 install metro-notation
```

or

```sh
pip install metro-notation
```

## Usage

```sh
metro-notation [filename]
```

## Algorithm notation format

- ``#`` ignores up to the end of the line as a comment
- ``[name]`` specifies the name of the following algorithm
- ``RMLUDFBw2xy'`` can be used to describe the algorithm
- ``whitespace`` splits the algorithm into triggers
- ``----`` splits the following description into separate columns

```
#
# PLL algorithms
#

[Ua Perm]
RU'RU RU RU'R'U' R2

[Z Perm]
M2'U'M2'U' M'U2' M2'U2'M'

----

[Ra Perm]
y RU'R'U' RURD R'U'RD' R'U2R'

[Gb Perm]
F'U'F R2UwR'U RU'RUw' R2'
```

## Output examples

**PLL algorithms**

<img src="images/pll-algorithms.png">
