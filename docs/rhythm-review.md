# 手順のまとまりの確認 — Metro Notation 1.0

119手順の現行の分割を記録します。元手順のトークンは変更していません。持ち替え26か所を必須の区切りとして保持しています。

短いトリガーと、スーン系の7手の手順を区別します。4手のトリガー内部に3＋1の字間を入れず、スーン系は7手の名称を保ちつつ図形は3＋4に分けています。長い連結は反復・挿入・セットアップと復帰のまとまりを確認して分割しています。すべての指使いを実演検証したという意味ではなく、追加した表示上の区切りは持ち替えを指示するものではありません。

参照: [Cube Tools — Common Triggers](https://bradleykh.github.io/CubeTools/triggers.html)、[CubeSkills — OLL](https://www.cubeskills.com/uploads/pdf/tutorials/oll-algorithms.pdf)、[CubeRoot — Triggers](https://www.cuberoot.me/wp-content/uploads/2019/11/119-Triggers.pdf)。照合に使い、写真の手順を別の手順に置き換えていません。

色: 定番手順の文字はすべて同じオレンジです。名前は図形・回転記号に付く補助情報としてHTMLに保持します。

| ケース | 路線の区切り | 検出した定番手順 | 個別に区切りを指定 |
|---|---|---|---|
| F2L-01 | `U R U' R'` | Sexy move (inverse) | — |
| F2L-02 | `U' L' U L` | Sexy move (inverse mirrored) | — |
| F2L-03 | `U L' U' L` | — | — |
| F2L-04 | `U' R U R'` | — | — |
| F2L-05 | `U2 R U R'` ／ `U2 R U' R'` | — | あり |
| F2L-06 | `U2 L' U' L` ／ `U2' L' U L` | — | — |
| F2L-07 | `U R U2' R'` ／ `U2 R U' R'` | — | — |
| F2L-08 | `U' L' U2 L` ／ `U2' L' U L` | — | — |
| F2L-09 | `L' U L` ／ `U L' U' L` | — | — |
| F2L-10 | `R U' R'` ／ `U' R U R'` | — | — |
| F2L-11 | `U' L' U L` ／ `U' L' U L` ／ `U2' L' U L` | Sexy move (inverse mirrored) | — |
| F2L-12 | `U R U' R'` ／ `U R U' R'` ／ `U2 R U' R'` | Sexy move (inverse) | — |
| F2L-13 | `U` ／ `L' U L U'` ／ `L' U' L` | Reverse sexy move (mirrored) | — |
| F2L-14 | `U'` ／ `R U' R' U` ／ `R U R'` | Reverse sexy move | — |
| F2L-15 | `U R U R' U2` ／ `R U' R' U` ／ `R U' R'` | Reverse sexy move | — |
| F2L-16 | `U' L' U' L U2'` ／ `L' U L U'` ／ `L' U L` | Reverse sexy move (mirrored) | — |
| F2L-17 | `R U2' R'` ／ `U' R U R'` | — | — |
| F2L-18 | `L' U2 L` ／ `U L' U' L` | — | — |
| F2L-19 | `R U2' R'` ／ `U R U' R'` | Sexy move (inverse) | — |
| F2L-20 | `L' U2 L` ／ `U' L' U L` | Sexy move (inverse mirrored) | — |
| F2L-21 | `R U R'` ／ `U R U' R'` | Sexy move (inverse) | — |
| F2L-22 | `L' U' L` ／ `U' L' U L` | Sexy move (inverse mirrored) | — |
| F2L-23 | `U2 R U' R'` ／ `U'` ／ `R U' R' U` ／ `R U' R'` | Reverse sexy move | — |
| F2L-24 | `U2 L' U L U` ／ `L' U L U'` ／ `L' U L` | Reverse sexy move (mirrored) | — |
| F2L-25 | `U' F'` ／ `R U R' U'` ／ `R' F R` | Sexy move | — |
| F2L-26 | `r U r' U'` ／ `r' F r F'` | — | — |
| F2L-27 | `R U' R' U` ／ `R U' R'` | Reverse sexy move | — |
| F2L-28 | `L' U L U'` ／ `L' U L` | Reverse sexy move (mirrored) | — |
| F2L-29 | `L' U' L U` ／ `L' U' L` | Sexy move (mirrored) | — |
| F2L-30 | `R U R' U'` ／ `R U R'` | Sexy move | — |
| F2L-31 | `U'` ／ `R' F R F'` ／ `R U' R'` | Sledgehammer | — |
| F2L-32 | `U R U' R'` ／ `U R U' R'` ／ `U R U' R'` | Sexy move (inverse) | — |
| F2L-33 | `U' R U' R'` ／ `U2 R U' R'` | — | — |
| F2L-34 | `U R' D'` ／ `R U' R'` ／ `D R` | — | あり |
| F2L-35 | `U' R U R' U` ／ `y'` ／ `R' U' R` | — | — |
| F2L-36 | `U` ／ `F' U' F` ／ `U' R U R'` | — | — |
| F2L-37 | `R' F R F'` ／ `R U' R' U` ／ `R U' R' U2` ／ `R U' R'` | Sledgehammer, Reverse sexy move | — |
| F2L-38 | `R U' R'` ／ `U' R U R'` ／ `U2 R U' R'` | — | あり |
| F2L-39 | `R U' R' U` ／ `R U2' R'` ／ `U R U' R'` | Reverse sexy move, Sexy move (inverse) | — |
| F2L-40 | `r U' r'` ／ `U2 r U r'` ／ `R U R'` | — | あり |
| F2L-41 | `R U' R'` ／ `r U' r'` ／ `U2 r U r'` | — | あり |
| OLL-01 | `R U2' R2' F` ／ `R F' U2'` ／ `R' F R F'` | Sledgehammer | — |
| OLL-02 | `R' F' r U2'` ／ `L' U2 l U2'` ／ `R' F R` | — | あり |
| OLL-03 | `r'` ／ `R2 U R'` ／ `U r U2' r' U M'` | — | — |
| OLL-04 | `l` ／ `L2' U' L` ／ `U' l' U2 l U' M'` | — | — |
| OLL-05 | `l' U2 L` ／ `U L' U l` | Wide Anti-Sune (mirrored) | — |
| OLL-06 | `r U2' R'` ／ `U' R U' r'` | Wide Anti-Sune | — |
| OLL-07 | `r U R'` ／ `U R U2' r'` | Wide Sune | — |
| OLL-08 | `l' U' L` ／ `U' L' U2 l` | Wide Sune (mirrored) | — |
| OLL-09 | `R U R' U'` ／ `R' F R2` ／ `U R' U' F'` | Sexy move | — |
| OLL-10 | `U'` ／ `R U R' U` ／ `R' F R F'` ／ `R U2' R'` | Half Sune, Sledgehammer | — |
| OLL-11 | `U r'` ／ `R2 U R'` ／ `U R U2' R' U M'` | — | — |
| OLL-12 | `U' l` ／ `L2' U' L` ／ `U' L' U2 L U' M'` | — | — |
| OLL-13 | `F U R U'` ／ `R2' F' R` ／ `U R U' R'` | Sexy move (inverse) | — |
| OLL-14 | `R' F R` ／ `U R' F' R` ／ `F U' F'` | — | あり |
| OLL-15 | `r' U' M'` ／ `U' R U` ／ `r' U r` | — | あり |
| OLL-16 | `U2` ／ `r U r'` ／ `R U R' U'` ／ `r U' r'` | Sexy move | — |
| OLL-17 | `F R' F' R` ／ `U S' R U' R' S` | Hedgehammer | — |
| OLL-18 | `r U' r'` ／ `F U F U'` ／ `R U R' U'` ／ `F'` | Sexy move | あり |
| OLL-19 | `S' R U R' S U'` ／ `R' F R F'` | Sledgehammer | — |
| OLL-20 | `S R' U'` ／ `R U R` ／ `U R U' R'` ／ `S'` | Sexy move (inverse) | — |
| OLL-21 | `R U R' U` ／ `R U' R' U` ／ `R U2' R'` | Half Sune, Reverse sexy move | あり |
| OLL-22 | `R U2' R2'` ／ `U' R2 U' R2'` ／ `U2' R` | — | あり |
| OLL-23 | `R2' D' R U2 R' D` ／ `R U2 R` | — | — |
| OLL-24 | `U' r U R'` ／ `U' r' F R F'` | — | — |
| OLL-25 | `F R' F' r` ／ `U R U' r'` | — | あり |
| OLL-26 | `L' U' L` ／ `U' L' U2 L` | Sune (mirrored) | — |
| OLL-27 | `R U R'` ／ `U R U2' R'` | Sune | — |
| OLL-28 | `r U R'` ／ `U' R` ／ `r'` ／ `U R U' R'` | Sexy move (inverse) | — |
| OLL-29 | `U' l D l' U` ／ `l D' l'` ／ `R' F R U'` ／ `R' F' R` | — | — |
| OLL-30 | `F R' F R2 U'` ／ `R' U'` ／ `R U R' F2` | — | — |
| OLL-31 | `R' U' F` ／ `U R U' R'` ／ `F' R` | Sexy move (inverse) | — |
| OLL-32 | `S` ／ `R U R' U'` ／ `R' F R f'` | Sexy move | — |
| OLL-33 | `R U R' U'` ／ `R' F R F'` | Sexy move, Sledgehammer | — |
| OLL-34 | `U' R U R2'` ／ `U' R' F R` ／ `U R U' F'` | — | あり |
| OLL-35 | `R U2' R2'` ／ `F R F'` ／ `R U2' R'` | — | あり |
| OLL-36 | `R U R2'` ／ `F' U' F` ／ `U R2 U2' R'` | — | あり |
| OLL-37 | `F R' F' R` ／ `U R U' R'` | Hedgehammer, Sexy move (inverse) | — |
| OLL-38 | `R U R' U` ／ `R U' R' U'` ／ `R' F R F'` | Half Sune, Sledgehammer | あり |
| OLL-39 | `f' L F L'` ／ `U' L' U L` ／ `S` | Sexy move (inverse mirrored) | — |
| OLL-40 | `f R' F' R` ／ `U R U' R'` ／ `S'` | Sexy move (inverse) | — |
| OLL-41 | `R U R' U` ／ `R U2'` ／ `R' F` ／ `R U R' U'` ／ `F'` | Half Sune, Sexy move | — |
| OLL-42 | `U'` ／ `F R' F' R` ／ `U2 R' U'` ／ `R2 U' R2' U2' R` | Hedgehammer | — |
| OLL-43 | `U R' U' F' U` ／ `F R` | — | — |
| OLL-44 | `F` ／ `U R U' R'` ／ `F'` | Sexy move (inverse) | — |
| OLL-45 | `F` ／ `R U R' U'` ／ `F'` | Sexy move | — |
| OLL-46 | `R' U'` ／ `R' F R F'` ／ `U R` | Sledgehammer | — |
| OLL-47 | `F R' F' R` ／ `U2` ／ `R U' R' U` ／ `R U2' R'` | Hedgehammer, Reverse sexy move | — |
| OLL-48 | `F` ／ `R U R' U'` ／ `R U R' U'` ／ `F'` | Sexy move | — |
| OLL-49 | `U' l` ／ `U' l2' U l2` ／ `U l2' U' l` | — | — |
| OLL-50 | `l' U l2 U'` ／ `l2' U'` ／ `l2 U l'` | — | — |
| OLL-51 | `F` ／ `U R U' R'` ／ `U R U' R'` ／ `F'` | Sexy move (inverse) | — |
| OLL-52 | `R' F' U' F` ／ `U' R U R'` ／ `U R` | — | あり |
| OLL-53 | `l' U' L` ／ `U' L' U L` ／ `U' L' U2 l` | Sexy move (inverse mirrored) | — |
| OLL-54 | `U r U R'` ／ `U R U' R'` ／ `U R U2' r'` | Sexy move (inverse) | — |
| OLL-55 | `R' F R` ／ `U R U'` ／ `R2' F' R2` ／ `U' R' U` ／ `R U R'` | — | あり |
| OLL-56 | `r U r'` ／ `U R U' R'` ／ `U R U' R'` ／ `r U' r'` | Sexy move (inverse) | — |
| OLL-57 | `R U R' U'` ／ `M' U R U' r'` | Sexy move | — |
| PLL-Aa | `l' U R' D2` ／ `R U' R' D2` ／ `R` ／ `l` | — | あり |
| PLL-Ab | `l'` ／ `R' D2 R U` ／ `R' D2 R U' l` | — | — |
| PLL-E | `R' U' R' D'` ／ `R U' R' D R U` ／ `R' D' R` ／ `U R' D R2` | — | — |
| PLL-F | `R' U' F'` ／ `R U R' U'` ／ `R' F R2` ／ `U' R'` ／ `U' R U R'` ／ `U R` | Sexy move | あり |
| PLL-Ga | `R2 U R' U` ／ `R' U' R U'` ／ `R2 U'` ／ `D R' U R D'` | Half Anti-Sune | あり |
| PLL-Gb | `R' U' R U` ／ `D' R2 U R' U` ／ `R U' R U'` ／ `R2' D` | — | あり |
| PLL-Gc | `R2' U' R U'` ／ `R U R' U` ／ `R2 U` ／ `D' R U' R' D` | Half Sune | — |
| PLL-Gd | `R U R' U'` ／ `D R2 U'` ／ `R U' R' U` ／ `R' U R2 D'` | Sexy move, Reverse sexy move | あり |
| PLL-H | `M2' U' M2' U2'` ／ `M2' U' M2'` | — | — |
| PLL-Ja | `r` ／ `R2' F R F'` ／ `R U2' r' U r` ／ `U2' r'` | — | — |
| PLL-Jb | `R U R' F'` ／ `R U R' U'` ／ `R' F R2` ／ `U' R'` | J trigger, Sexy move | — |
| PLL-Na | `R U R' U` ／ `R U R' F'` ／ `R U R' U'` ／ `R' F R2 U'` ／ `R' U2 R U' R'` | Half Sune, J trigger, Sexy move | — |
| PLL-Nb | `R'` ／ `U R U' R'` ／ `F' U' F` ／ `R U R' U'` ／ `R U'` ／ `f R f'` | Sexy move (inverse), Sexy move | — |
| PLL-Ra | `U` ／ `R U' R' U'` ／ `R U R D` ／ `R' U' R D'` ／ `R' U2 R'` | — | あり |
| PLL-Rb | `R' U2 R' D'` ／ `R U' R' D R` ／ `U R U' R'` ／ `U' R` | Sexy move (inverse) | あり |
| PLL-T | `R U R' U'` ／ `R' F R2 U'` ／ `R' U'` ／ `R U R' F'` | Sexy move, J trigger | — |
| PLL-Ua | `R U R' U` ／ `R' U' R2 U'` ／ `R' U R' U R` | Half Sune | あり |
| PLL-Ub | `R' U R' U'` ／ `R3 U' R' U` ／ `R U R2'` | — | — |
| PLL-V | `R'` ／ `U R U' R'` ／ `f' U'` ／ `R U2 R'` ／ `U' R U' R'` ／ `f R` | Sexy move (inverse), Anti-Sune | あり |
| PLL-Y | `F R U' R' U'` ／ `R U R' F'` ／ `R U R'` ／ `U'` ／ `R' F R F'` | J trigger, Sledgehammer | — |
| PLL-Z | `M' U' M2' U'` ／ `M2' U'` ／ `M' U2' M2'` | — | — |
