# metro-notation

Visualize the Rubik's cube algorithms in a notation like a train route map that I call **"Metro notation"**.<br>
**"Metro notation"** is a notation that focuses on the direction in which the force of each finger is applied.

ルービックキューブのアルゴリズムを、私が **「メトロ記法」** と呼んでいる、電車の路線図のような表記法で可視化します。<br>
**「メトロ記法」** は各指の力を加える方向に注目した表記法です。


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

<img src="images/pll.png">
