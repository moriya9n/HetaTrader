# HetaTrader
Generate Japanese stock trading signal using panrolling chart gallery. Heta trade means poor trade :p

無保証。
バグってると思うが、自分用なので、そのうちバグは取れるかも。

インストール
============

Windows 10 32bit 版でのみ確認。

1. [チャートギャラリー](https://px.a8.net/svt/ejp?a8mat=1TV37J+5AIUZM+2I+HUD03&a8ejpredirect=http%3A%2F%2Fwww.tradersshop.com%2Fbin%2Fshowprod%3Fc%3D9784939103070)をインストールする。Version 4 でも OK。
2. python 3.6 をインストールする。インストール時に、PATH に追加すること。
3. [pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/)をインストールする。

USAGE
=====

1. PanMenu でデータを更新する。
2. コマンドプロンプトを開いて、HetaTrader ディレクトリに CD し、python kabudb.py を実行する。
   (エクスプローラからダブルクリックでも実行可能かも。)初回はデータを全部取り込むので少し時間がかかる。
3. python kabubot.py を実行すると、52週の高値更新銘柄と、終値が過去21日の1sigma を超えた銘柄を表示。
   (見づらいが)

NOTE
====

HetaTrader.py はまだ実装中。

