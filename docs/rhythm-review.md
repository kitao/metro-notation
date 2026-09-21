# 手順の区切り

路線の区切りと、各手順に含まれる定番動作の一覧です。

## 規則

- 原紙の持ち替え26か所を必ず区切ります。
- 4手のトリガー内部に3＋1の字間を入れません。
- スーン系は7手の単位を保ち、図形では3＋4に分けます。
- 取り出し・挿入・準備と復帰のまとまりを優先します。
- 同じ辺の往復や交差を避けるため、図形を分割する場合があります。

原紙にない区切りは、読みやすくするための分割です。定番動作の文字色はオレンジに統一しています。

## 個別の指定

| 対象 | 採用したまとまりと理由 |
| --- | --- |
| F2L 9・10 | 最初の4手でペアを取り出し、最後の3手で挿入。3＋1の字間も挟みません。 |
| F2L 23 | U2の準備、4手、4手、最後の3手。途中にU'だけを取り残しません。 |
| OLL 3・4・11・12 | 前半、後半4手、最後のU/M系の復帰。末尾の中層操作を長い連結へ埋め込みません。 |
| OLL 23 | R2' D'の準備、R U2 R' D、最後のR U2 R。R U2 R'を途中で切りません。 |
| OLL 24 | U'の準備と4＋4。r U R' U'を維持します。 |
| OLL 25・37 | 4＋4のリズムを優先。8手を一つの図形に押し込みません。 |
| OLL 28 | 最初のr U R' U'は4手を維持。続くR r'は同じ辺を往復するため別図形にし、元の文字列を保持します。最後の逆セクシー4手も維持します。 |
| OLL 17・19 | S層の準備・復帰を含む6手は連続した図形を維持。手数だけを理由に分割しません。 |
| PLL E | D/D'で終わる4手を4回、最後にR2。末尾R2を直前の閉路に重ねません。 |
| PLL T | 4＋4＋2＋4。末尾のJトリガーを維持し、間の2手は独立させます。 |
| PLL Ra | 冒頭Uの後の持ち替えを維持。その後は4＋4＋4＋3。 |
| PLL Ub | R3を原紙どおり保持。R'への短縮を理由に区切りを変えません。 |


参考：[Common Triggers](https://bradleykh.github.io/CubeTools/triggers.html)、CubeSkillsの[F2L](https://www.cubeskills.com/uploads/pdf/tutorials/f2l.pdf)・[OLL](https://www.cubeskills.com/uploads/pdf/tutorials/oll-algorithms.pdf)・[PLL](https://www.cubeskills.com/uploads/pdf/tutorials/pll-algorithms.pdf)。

## 全119件

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
| F2L-09 | `L' U L U` ／ `L' U' L` | — | — |
| F2L-10 | `R U' R' U'` ／ `R U R'` | — | — |
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
| F2L-23 | `U2` ／ `R U' R' U'` ／ `R U' R' U` ／ `R U' R'` | Reverse sexy move | あり |
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
| OLL-03 | `r'` ／ `R2 U R'` ／ `U r U2' r'` ／ `U M'` | — | あり |
| OLL-04 | `l` ／ `L2' U' L` ／ `U' l' U2 l` ／ `U' M'` | — | あり |
| OLL-05 | `l' U2 L` ／ `U L' U l` | Wide Anti-Sune (mirrored) | — |
| OLL-06 | `r U2' R'` ／ `U' R U' r'` | Wide Anti-Sune | — |
| OLL-07 | `r U R'` ／ `U R U2' r'` | Wide Sune | — |
| OLL-08 | `l' U' L` ／ `U' L' U2 l` | Wide Sune (mirrored) | — |
| OLL-09 | `R U R' U'` ／ `R' F R2` ／ `U R' U' F'` | Sexy move | — |
| OLL-10 | `U'` ／ `R U R' U` ／ `R' F R F'` ／ `R U2' R'` | Half Sune, Sledgehammer | — |
| OLL-11 | `U r'` ／ `R2 U R'` ／ `U R U2' R'` ／ `U M'` | — | あり |
| OLL-12 | `U' l` ／ `L2' U' L` ／ `U' L' U2 L` ／ `U' M'` | — | あり |
| OLL-13 | `F U R U'` ／ `R2' F' R` ／ `U R U' R'` | Sexy move (inverse) | — |
| OLL-14 | `R' F R` ／ `U R' F' R` ／ `F U' F'` | — | あり |
| OLL-15 | `r' U' M'` ／ `U' R U` ／ `r' U r` | — | あり |
| OLL-16 | `U2` ／ `r U r'` ／ `R U R' U'` ／ `r U' r'` | Sexy move | — |
| OLL-17 | `F R' F' R` ／ `U S' R U' R' S` | Hedgeslammer | — |
| OLL-18 | `r U' r'` ／ `F U F U'` ／ `R U R' U'` ／ `F'` | Sexy move | あり |
| OLL-19 | `S' R U R' S U'` ／ `R' F R F'` | Sledgehammer | — |
| OLL-20 | `S R' U'` ／ `R U R` ／ `U R U' R'` ／ `S'` | Sexy move (inverse) | — |
| OLL-21 | `R U R' U` ／ `R U' R' U` ／ `R U2' R'` | Half Sune, Reverse sexy move | あり |
| OLL-22 | `R U2' R2'` ／ `U' R2 U' R2'` ／ `U2' R` | — | あり |
| OLL-23 | `R2' D'` ／ `R U2 R' D` ／ `R U2 R` | — | あり |
| OLL-24 | `U'` ／ `r U R' U'` ／ `r' F R F'` | — | あり |
| OLL-25 | `F R' F' r` ／ `U R U' r'` | — | あり |
| OLL-26 | `L' U' L` ／ `U' L' U2 L` | Sune (mirrored) | — |
| OLL-27 | `R U R'` ／ `U R U2' R'` | Sune | — |
| OLL-28 | `r U R' U'` ／ `R` ／ `r'` ／ `U R U' R'` | Sexy move (inverse) | あり |
| OLL-29 | `U' l D l' U` ／ `l D' l'` ／ `R' F R U'` ／ `R' F' R` | — | — |
| OLL-30 | `F R' F R2 U'` ／ `R' U'` ／ `R U R' F2` | — | — |
| OLL-31 | `R' U' F` ／ `U R U' R'` ／ `F' R` | Sexy move (inverse) | — |
| OLL-32 | `S` ／ `R U R' U'` ／ `R' F R f'` | Sexy move | — |
| OLL-33 | `R U R' U'` ／ `R' F R F'` | Sexy move, Sledgehammer | — |
| OLL-34 | `U' R U R2'` ／ `U' R' F R` ／ `U R U' F'` | — | あり |
| OLL-35 | `R U2' R2'` ／ `F R F'` ／ `R U2' R'` | — | あり |
| OLL-36 | `R U R2'` ／ `F' U' F` ／ `U R2 U2' R'` | — | あり |
| OLL-37 | `F R' F' R` ／ `U R U' R'` | Hedgeslammer, Sexy move (inverse) | — |
| OLL-38 | `R U R' U` ／ `R U' R' U'` ／ `R' F R F'` | Half Sune, Sledgehammer | あり |
| OLL-39 | `f' L F L'` ／ `U' L' U L` ／ `S` | Sexy move (inverse mirrored) | — |
| OLL-40 | `f R' F' R` ／ `U R U' R'` ／ `S'` | Sexy move (inverse) | — |
| OLL-41 | `R U R' U` ／ `R U2'` ／ `R' F` ／ `R U R' U'` ／ `F'` | Half Sune, Sexy move | — |
| OLL-42 | `U'` ／ `F R' F' R` ／ `U2 R' U'` ／ `R2 U' R2' U2' R` | Hedgeslammer | — |
| OLL-43 | `U R' U' F' U` ／ `F R` | — | — |
| OLL-44 | `F` ／ `U R U' R'` ／ `F'` | Sexy move (inverse) | — |
| OLL-45 | `F` ／ `R U R' U'` ／ `F'` | Sexy move | — |
| OLL-46 | `R' U'` ／ `R' F R F'` ／ `U R` | Sledgehammer | — |
| OLL-47 | `F R' F' R` ／ `U2` ／ `R U' R' U` ／ `R U2' R'` | Hedgeslammer, Reverse sexy move | — |
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
| PLL-E | `R' U' R' D'` ／ `R U' R' D` ／ `R U R' D'` ／ `R U R' D` ／ `R2` | — | あり |
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
