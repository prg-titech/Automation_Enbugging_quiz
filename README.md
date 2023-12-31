# Automation_Enbugging_quiz
## 概要

これはエラー生成クイズの問題作成自動化に関する実装です。

### 実装
- エラーを維持したコードの縮小: /code_minimize

- 変更箇所設定時の別解調査: /alternative_search

- 問題の難易度の数値化: /difficulty_check

各フォルダ内のmainで始まるファイルが、機能を使用するのに利用できます。

なお、code_minimizeとalternative_searchで行っているScalaコードのコンパイルにはscala-cliを使用しています。Scala-cliは起動に少し時間がかかるため、まず一度scala-cliを使用してから各機能を使用し始めてください。(もしくはuse_cliを換えることで、お好みの環境を使用することもできます。)

またalternative_searchとdifficulty_checkでは、EBNF解析のためにPythonのライブラリであるLarkを使用しています。
