# デダック De:Duck

<img src="duck.png">

## 目次
1. [チーム名](#anchor1)
1. [製作背景](#anchor2)
1. [使い方](#anchor3)
1. [リンク](#anchor4)
1. [特徴](#anchor5)
1. [解決できること](#anchor6)
1. [今後の展望](#anchor7)
1. [注力したこと](#anchor8)
1. [開発技術](#anchor9)


<a id="anchor1"></a>
## チーム名
### チームメンバー
- 中尾龍矢　　　　　 :アルゴリズム担当
- 伊地知翔也　　　　 :UI兼サーバー構築
- パニアグアカルロス :UI担当

## 製品概要
### Debug × Tech
<a id="anchor2"></a>
### 製作背景
以前、友人にプログラム（学校の課題）の相談を持ち掛けた際、コロナ対策として直接会うことを避け、LINEを用いて手伝ってもらいました。しかしなかなか解決に至らず、友人の時間を長く取ってしまった事に申し訳なくなった経験があります。
これをきっかけに「強化版ラバーダック・デバッグを作ってみたらどうだろう」と思い、このアイデアを提案、開発に至りました。
「ラバーダック・デバッグ」とはソフトウェア工学の一つの手法で、ゴム製アヒル人形にコードの説明を一行ずつを行い、その過程で解決策を得るというものです。  
この手法のメリットは、プログラマが自身のコードについて、達成したい目的と意図を言語化する過程にあります。（アヒル人形をプログラム初心者として捉え、）相手が正しく理解できるように様々な表現や着眼点を模索することで、新たな解決策と深い理解へ繋がることができます。
しかし、単純な「ラバーダック・デバッグ」は話しかけながら自らの頭の中で整理していくので、本人の理解力が直接効率に影響してしまいます。 ~~なので音声認識や自然言語処理を施すことにより、利用者のサポートできるのではないかと考えました。~~
  
本製品をもちいることで、実際にユーザが話したアルゴリズムの動作や変数、関数といった関係をAIが解析し、わかりやすく表示します。これにより、理解を助けるとともに、意図していた説明との食い違いや、わかりずらい抽象的な単語を避け、わかりやすい説明と明快な理解を促します。  
''''
ラバーダックデバッグという、**史上最強のデバッグ手法**モノにプログラムの処理内容を話しかけて、机上でデバッグする手法があります。
ラバーダックデバッグは、人に説明するように考えながらで話すため、アルゴリズムや処理内容を熟知する必要があります。
そのため、アルゴリズムや処理内容が間違っている場合、気づくことができます。
また、人に説明するように話すため、わかりやすい説明にすることができます。
しかし、間違いに気づくことは100%完璧ではありません。
また、わかりやすい説明も客観的に見て必ずわかりやすい説明になっているとは限りません。
そこで、ユーザが話したことをまとめ（要約）、わかりやすい説明かどうかを独自開発のAIが解析し、結果を返却。
ラバーダックデバッグをより簡単で強力なものに変えます。
''''
<a id="anchor3"></a>
### 使い方

<a id="anchor4"></a>
### リンク
<a href="http://jphacks-2020.app.idichi.tk/#"> デモサイト </a>

<a id="anchor5"></a>
### 特長
#### 1. 特長1  
音声での入力（説明）の中で、抽象的、複雑な単語（主に技術用語）を検知し、その部分の具体的な説明を推奨する。
#### 2. 特長2
実際にメモを取ることなく、画面と常に向かい合って作業ができるので、スムーズに説明と考察を繰り返せる。
#### 3. 特長3
入力された説明に対し、自動的に要点をかいつまみ、「アルゴリズムの動作」と「変数などの要素」に分類し表示する。

<a id="anchor6"></a>
### 解決出来ること
「ラバーダック・デバッグ」は、説明を聞かせる対象が無機物なので、誰の手を煩わせることもなく、コロナ禍の中でも目的が達成できます。
特徴1の機能によって、再度説明をしたときに理解のしやすい説明になり、利用者を深い理解に誘導しやすくなります。
また、特徴3の機能によってユーザの認識と、実際に話した説明が食い違いを見つけやすくする。また、説明はできるが具体的にどんな実装をすればよいのかを納得しきれていないときに、判断の指標としてリスト化しておけます。

<a id="anchor7"></a>
### 今後の展望
- 要点を抽出する処理において、文節の親子関係を推測する事が技術的に間に合わなかったことを解決したいです。
- UIがばぐってること
注力したこと（こだわり等）
利用者が入力した音声データから複雑な単語、要点を抽出する機能
チャット風のUIに仕上げたことで親密感を上げたこと
Intro.jsを導入したことによりチュートリアルを実装したこと

<a id="anchor8"></a>
### 注力したこと（こだわり等）
- 利用者が入力した音声データから複雑な単語、要点を抽出する機能
- チャット風のUIに仕上げたことで親密感を上げたこと
- Intro.jsを導入したことによりチュートリアルを実装したこと
''''
- 自然言語処理（ユーザが話した言葉を解析する処理）
''''

<a id="anchor9"></a>
## 開発技術
### 活用した技術
#### フレームワーク・ライブラリ・モジュール
- さくらインタネットサーバー
- CaboCha/南瓜
- MeCab
- Flask
### 独自技術
#### ハッカソンで開発した独自機能・技術
- 利用者が入力した音声データから複雑な単語、要点を抽出する機能
- 音声をwebAPIに通した後に読点、句読点のように文を分ける機能

#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
- 自然言語処理の知見と独自研究
 
