# tribox CFOP 手順表 B-1.0

Metro Notationの手順データです。[tribox CFOP 手順表 B-1.0](https://store.tribox.com/products/detail.php?product_id=3973)の写真から転記しています。

2025年6月初版。

## データ

| 分類 | 件数 | ファイル |
| --- | ---: | --- |
| F2L | 41 | [f2l.md](f2l.md) |
| OLL | 57 | [oll.md](oll.md) |
| PLL | 21 | [pll.md](pll.md) |
| F2Lの識別図 | 41 | [f2l-patterns.md](f2l-patterns.md) |
| OLLの上面 | 57 | [oll-patterns.md](oll-patterns.md) |

## 記録形式

手順は原紙の大文字・小文字、回転方向、手数を保持します。プライムの字形はASCIIの `'` に統一しています。

- `r` と `R`、`l` と `L`を区別します。
- `U2'`、`R3`をそのまま記録します。
- `<br>`は原紙の改行です。表示上の区切りは[learning.py](../src/metronotation/learning.py)で扱います。
- `P3:U`は3手目のUに付くプッシュ、`T3:U`はトリガーの注記です。
- `REGRIP→n`はn手目の直前の持ち替えです。左手の指定も記録します。
- 若葉マークはLearn firstの選定に使います。

指使いの青・橙117か所、持ち替え26か所、若葉18件を原写真と照合済みです。
持ち替え位置は図の区切りに反映します。指使いの色は資料として保持し、図中の路線色・イディオム色には流用しません。
灰色の指図は注記として保持し、具体的な指の名称へ置き換える推測はしていません。
F2Lは写真の配色、OLL上面は写真のマスクを使い、OLL側面とPLLは手順から逆算した状態を描画します。

## 写真

2026年9月20日にP1〜P4、21日にP5・P6を受領。原画像とSHA-256を保存しています。

| 資料ID | ファイル | 内容 | SHA-256 |
| --- | --- | --- | --- |
| P1 | [photos/oll.png](photos/oll.png) | OLL面。左下端が一部切れている | `7edac9fa7de3aa06dd586bf862ffe9c32f8e5f2107fe6733599ab851a655f361` |
| P2 | [photos/f2l-pll.png](photos/f2l-pll.png) | F2L・PLL面。下端・右端の切れ、PLL下段の反射あり | `237892a299469b7270060b8cbe7f5f358fedd1d120558da648041e25558cf85c` |
| P3 | [photos/oll-supplement.png](photos/oll-supplement.png) | OLL面の追加写真。OLL 35の下段を含む | `9bb104d1eb2908626acf8c1ea5bd3080067e42d47ef3f7303f29d5de1fc38d72` |
| P4 | [photos/f2l-pll-supplement.png](photos/f2l-pll-supplement.png) | F2L・PLL面の追加写真。下端・右端まで写っている | `ea491aa38d5da423d4ba41bb7aa83dbaba9dbc68961499aeda1ef87b5254ad54` |
| P5 | [photos/f2l-pll-closeup-left.png](photos/f2l-pll-closeup-left.png) | 左半分の接写 | `6095322a6437bc46624088cab98360ae21259b1b0ed3bc97974806696b89068e` |
| P6 | [photos/f2l-pll-closeup-right.png](photos/f2l-pll-closeup-right.png) | 右半分の接写 | `9f6782560e2efae35aaafe374bd5af6bb36e87ca8a5dfdd7b5ca5d1fe6054be8` |

## 照合記録

2026年9月21日、全119手順・1,208手・持ち替え26か所を確認しました。
写真から転記したF2Lの配色41件とOLL上面57件を、キューブの回転計算と照合しています。
[cubing.js](https://js.cubing.net/cubing/kpuzzle/) 0.63.6による独立した計算でも、各手の途中状態と全119件の開始状態の54面が一致しました。実機での全手順の指使い評価は未実施です。

| 箇所 | 照合で確定した内容 |
| --- | --- |
| F2L 26 | 3手目は`r'`。初回の`R'`をP2で訂正 |
| OLL 35 | P1で切れていた2行目をP3で補完 |
| PLL T・Y | 2行目をP2の拡大表示で照合 |
| PLL Gc・Nb・Rb | P4で全文を照合。Rbの1行目末尾は`D R` |

更新時の検査は[CONTRIBUTING.md](../CONTRIBUTING.md)を参照してください。
原紙・写真はソフトウェアのMITライセンスの対象外です。
