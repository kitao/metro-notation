# PLL: 21ケース

資料: [P2](photos/f2l-pll.png)、[P4](photos/f2l-pll-supplement.png)。[記録形式](README.md#記録形式)を参照してください。

P2で読めなかったGc・Nb・RbはP4で補完し、P5/P6の接写でも照合しています。

紙面の配置です。F2Lの30・29などが間に入りますが、ここではPLLだけを示します。

```text
Ua Ub E       Ja Jb
Aa Ab F V  Ga Gb Ra Rb
T  Y  H Z  Gc Gd Na Nb
```

| ID | 手順（紙面の改行を保持） | 指使いの色 | 注記 | 回転列の状態 |
| --- | --- | --- | --- | --- |
| Aa | `l' U R' D2`<br>`R U' R' D2 R l` | — | 左手REGRIP→1; 若葉 | 転記済 |
| Ab | `l' R' D2`<br>`R U R' D2 R U' l` | — | 左手REGRIP→1; 若葉 | 転記済 |
| E | `R' U' R' D' R U' R' D`<br>`R U R' D' R U R' D R2` | P4:D'; P12:D' | REGRIP→1 | 転記済 |
| F | `R' U' F' R U R' U'`<br>`R' F R2 U' R' U' R U R' U R` | P5:U; P15:U | — | 転記済 |
| Ga | `R2 U R' U R' U' R U' R2`<br>`U' D R' U R D'` | P2:U; P15:D' | REGRIP→1 | 転記済 |
| Gb | `R' U' R U D'`<br>`R2 U R' U R U' R U' R2' D` | P7:U | 図の右側に指図とR | 転記済 |
| Gc | `R2' U' R U' R U R' U`<br>`R2 U D' R U' R' D` | P6:U | REGRIP→9; 図の右側に指図とU'・U; P4で補完 | 転記済 |
| Gd | `R U R' U' D R2 U'`<br>`R U' R' U R' U R2 D'` | — | REGRIP→1; 図の右側に指図とR・U・D' | 転記済 |
| H | `M2' U' M2' U2' M2' U' M2'` | — | 若葉; 「Mが左手なら U'→U」; P4で色も再照合 | 転記済 |
| Ja | `r R2' F R F'`<br>`R U2' r' U r U2' r'` | — | — | 転記済 |
| Jb | `R U R' F' R U R' U'`<br>`R' F R2 U' R'` | P2:U; P6:U | — | 転記済 |
| Na | `R U R' U R U R' F' R U R'`<br>`U' R' F R2 U' R' U2 R U' R'` | P2:U; P6:U; P10:U | — | 転記済 |
| Nb | `R' U R U' R' F' U' F`<br>`R U R' U' R U' f R f'` | P2:U; P6:F'; T17:f' | REGRIP→15; P4で末尾を補完 | 転記済 |
| Ra | `U R U' R' U' R U R D`<br>`R' U' R D' R' U2 R'` | P13:D' | REGRIP→2 | 転記済 |
| Rb | `R' U2 R' D' R U' R' D R`<br>`U R U' R' U' R` | P4:D' | REGRIP→1; P4で1行目末尾のD Rを補完 | 転記済 |
| T | `R U R' U' R' F R2 U' R' U'`<br>`R U R' F'` | P2:U; P12:U | 若葉; 下端の4手を拡大照合 | 転記済 |
| Ua | `R U R' U R' U'`<br>`R2 U' R' U R' U R` | P2:U | 若葉; 図の右側に指図とU | 転記済 |
| Ub | `R' U R' U' R3 U'`<br>`R' U R U R2'` | P10:U | REGRIP→1; 若葉 | 転記済 |
| V | `R' U R U' R' f' U'`<br>`R U2 R' U' R U' R' f R` | P2:U; P6:f' | — | 転記済 |
| Y | `F R U' R' U' R U R' F'`<br>`R U R' U' R' F R F'` | T9:F'; T17:F' | REGRIP→1; REGRIP→13; 若葉; 下段を拡大照合 | 転記済 |
| Z | `M' U' M2' U' M2'`<br>`U' M' U2' M2'` | — | 若葉; 「Mが左手なら U'→U」; 補足の小図あり; P4で色も再照合 | 転記済 |

## 追加写真で解消した箇所

| ID | P2での問題 | P4で確認できた内容 |
| --- | --- | --- |
| Gc | 下段の反射で文字のつながり・プライムが追い切れない | 全文とREGRIPの位置を再照合。2行目は `R2 U D' R U' R' D` |
| Nb | 2行目のREGRIP以降が右端にかかる | 末尾は `f R f'`。最後の `f'` は青 |
| Rb | 1行目の末尾が写真の右端にかかる | 末尾は `D R`。`D` だけで行が終わると推測しなくて正解だった |

T・Yは当初要確認でしたが、P2を3倍で表示して下段の回転記号とプライムを照合できたため、転記済に更新しました。

T・Y・H・ZもP4で再照合しました。

## 記法上の重要な点

- **Ubの `R3` は原写真通り**です。向きと指づかいを失う `R'` への簡約をしません。
- Vの `f` とJaの `r` は小文字です。
- H・Zの `U'→U` は条件付きの補足であり、基準の回転列を上書きしません。
- 図の右の「指図＋U/R/D'」は注記です。アルゴリズムに回転を追加しません。
- 指使いの青・橙26か所、持ち替え12か所、若葉8件をP4/P5/P6で照合しました。Aa・Abの持ち替えは左手です。
- 識別図は回転列から逆算して描きます。原紙の交換矢印は転記していません。
